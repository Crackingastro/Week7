import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create output directory (fixed)
os.makedirs('data/output', exist_ok=True)

# Create SQLAlchemy engine (proper connection)
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Tables to export (updated to your actual schemas)
tables = [
    ('fct_messages', 'star_analytics.fct_messages'),
    ('dim_channels', 'star_analytics.dim_channels'),
    ('dim_dates', 'star_analytics.dim_dates'),
    ('stg_telegram_messages', 'star_staging.stg_telegram_messages')
]

# Export each table
for file_name, table_name in tables:
    try:
        # Extract schema and table names
        schema, table = table_name.split('.')
        
        # Read data using SQLAlchemy
        df = pd.read_sql_table(
            table_name=table,
            con=engine,
            schema=schema
        )
        
        # Save to CSV
        output_path = f'data/output/{file_name}.csv'
        df.to_csv(output_path, index=False)
        print(f"✅ Successfully exported {table_name} to {output_path}")
        
        # Show sample
        print(f"Sample data ({len(df)} rows total):")
        print(df.head(2))
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Failed to export {table_name}: {str(e)}")

print("\nAll exports completed!")