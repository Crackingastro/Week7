# scripts/image_processing.py

import os
from pathlib import Path
import datetime

import cv2
import psycopg2
from ultralytics import YOLO


def main():
    # ─── Database setup ──────────────────────────────────────────────────────────
    conn = psycopg2.connect(
        dbname   = os.getenv("DB_NAME",     "telegram_analytics"),
        user     = os.getenv("DB_USER",     "telegram_user"),
        password = os.getenv("DB_PASSWORD", "12345678"),
        host     = os.getenv("DB_HOST",     "localhost"),
        port     = os.getenv("DB_PORT",     "5432"),
    )
    cursor = conn.cursor()

    # ─── File‐system setup ───────────────────────────────────────────────────────
    SCRIPT_DIR = Path(__file__).parent
    RAW_ROOT   = SCRIPT_DIR.parent / "data" / "raw" / "telegram_images" / "2025-07-11"
    OUT_ROOT   = SCRIPT_DIR.parent / "detected_objects"
    OUT_ROOT.mkdir(exist_ok=True)

    # ─── Load YOLOv8 ─────────────────────────────────────────────────────────────
    model = YOLO("yolov8n.pt")

    # ─── Process each channel folder ────────────────────────────────────────────
    for channel_dir in RAW_ROOT.iterdir():
        if not channel_dir.is_dir():
            continue

        account = channel_dir.name
        target_channel = OUT_ROOT / account
        target_channel.mkdir(parents=True, exist_ok=True)

        for img_path in channel_dir.glob("*"):
            if img_path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue

            # Extract message_id directly from filename (e.g. "88.jpg" → 88)
            stem = img_path.stem
            try:
                message_id = int(stem)
            except ValueError:
                # skip images without integer stem
                print(f"Skipping {img_path.name}: cannot parse message_id")
                continue

            # Run detection
            results = model(str(img_path))[0]

            # Load for drawing
            img = cv2.imread(str(img_path))
            if img is None:
                print(f"Could not read {img_path}, skipping")
                continue

            date_str = RAW_ROOT.name
            ts       = datetime.datetime.now(datetime.timezone.utc)

            # Draw & insert each detection
            for box, cls_id, conf in zip(
                results.boxes.xyxy.cpu().numpy(),
                results.boxes.cls.cpu().numpy().astype(int),
                results.boxes.conf.cpu().numpy()
            ):
                x1, y1, x2, y2 = box.astype(int)
                cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=4)
                label = model.names.get(cls_id, str(cls_id))
                cv2.putText(
                    img, label, (x1, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA
                )

                # Insert into Postgres
                cursor.execute(
                    """
                    INSERT INTO raw.raw_image_detections (
                        image_path,
                        date,
                        account,
                        detected_object_class,
                        confidence_score,
                        processing_timestamp,
                        message_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT ON CONSTRAINT unique_detection DO NOTHING
                    """,
                    (
                        str(img_path.relative_to(SCRIPT_DIR.parent)),
                        date_str,
                        account,
                        label,
                        float(conf),
                        ts,
                        message_id
                    )
                )

            # Save annotated image and commit
            out_path = target_channel / img_path.name
            cv2.imwrite(str(out_path), img)
            conn.commit()
            print(f"Processed {img_path.name} → {out_path}")

    cursor.close()
    conn.close()
    print("Processing complete.")


if __name__ == "__main__":
    main()
