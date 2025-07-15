# Week7 Pipeline & API 🚀

A unified project that scrapes Telegram channels, loads data into Postgres, runs dbt transformations, enriches images with YOLOv8, and exposes analytics via FastAPI and Dagster.

## 📂 Project Structure

```
Week7/
├── .github/
│   └── workflow/                 # CI/CD pipelines and GitHub Actions
├── .tmp_dagster_home_bm0_r_k2/    # local Dagster instance storage (auto-generated)
├── api/                           # FastAPI application code
│   ├── main.py                    # API entrypoint
│   ├── database.py                # DB connection logic
│   ├── crud.py                    # query functions
│   └── schemas.py                 # Pydantic models
├── data/                          # raw and intermediate data storage
│   └── raw/telegram_images/       # scraped Telegram images by date/channel
├── dbt/                           # your dbt project and transformations
├── detected_objects/              # output images annotated by YOLO
├── scripts/                       # ETL and enrichment scripts
│   ├── telegram_scraper.py        # scrape Telegram data
│   ├── load_json_to_postgres.py   # load JSON into Postgres
│   └── image_processing.py        # run YOLO detection and annotate images
├── .gitignore                     # ignored files and folders
├── Dockerfile                     # container build instructions
├── docker-compose.yml             # local multi-service orchestration
├── pipeline.py                    # Dagster job & ops definition
├── workspace.yaml?                # Dagster workspace config (create if needed)
├── readme.md                      # project README (this file)
└── requirement.txt                # Python dependencies list
```

````

## ⚙️ Setup & Run

1. **Clone & install**

   ```bash
   git clone https://github.com/Crackingastro/Week7.git
   cd Week7
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
````

2. **Configure environment**

   * Copy `.env.example` → `.env` and fill in your credentials:

     ```dotenv
     API_ID=
     API_HASH=
     PHONE_NUMBER=

     DB_NAME=""
     DB_USER=""
     DB_PASSWORD=""
     DB_HOST=""
     DB_PORT=""
     ```

3. **Run with Docker Compose**

   ```bash
   docker-compose up --build
   ```

   * FastAPI API: [http://localhost:8000/docs](http://localhost:8000/docs)
   * Dagster UI:   [http://localhost:3000/](http://localhost:3000/)

4. **Manual (non‑Docker)**

   * Scrape data:  `python scripts/telegram_scraper.py`
   * Load DB:     `python scripts/load_json_to_postgres.py`
   * Transform:   `cd dbt && dbt run`
   * Enrich:      `python scripts/image_processing.py`
   * API:         `uvicorn main:app --reload`
   * Dagit UI:    `dagster dev -f pipeline.py`

---

Made with ❤️ by Crackingastro
