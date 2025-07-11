import os
import json
import psycopg2
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # Load .env for DB credentials

def load_all_json_to_postgres():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cursor = conn.cursor()
    cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")

    for root, _, files in os.walk("data/raw/telegram_messages"):
        for file in files:
            if file == 'messages.json':
                channel = os.path.basename(root)
                date = os.path.basename(os.path.dirname(root))
                table_name = f"telegram_messages_{channel}"

                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)
                
                # Add metadata
                for record in data:
                    record['_channel'] = channel
                    record['_date'] = date
                    record['_loaded_at'] = datetime.now().isoformat()

                df = pd.DataFrame(data)
                cols = ', '.join([f'"{col}" TEXT' for col in df.columns])
                cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS raw.{table_name} ({cols});
                    TRUNCATE TABLE raw.{table_name};
                """)
                
                for _, row in df.iterrows():
                    cursor.execute(
                        f"INSERT INTO raw.{table_name} ({', '.join([f'\"{c}\"' for c in row.index])}) "
                        f"VALUES ({', '.join(['%s'] * len(row))})",
                        tuple(row)
                    )
                print(f"Loaded {channel} ({len(data)} rows)")
    
    conn.commit()
    cursor.close()

load_all_json_to_postgres()