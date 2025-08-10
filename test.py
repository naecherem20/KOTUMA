from sqlalchemy import create_engine

# Paste your DATABASE_URL here
DATABASE_URL = "postgresql+psycopg2://postgres.vhljzmaxuqefptxkseyi:Boz09Kp0pDKT9Fq0@aws-0-eu-north-1.pooler.supabase.com:5432/postgres"

engine = create_engine(DATABASE_URL)

print("⏳ Testing database connection...")
try:
    with engine.connect() as conn:
        print("✅ Connected successfully!")
except Exception as e:
    print("❌ Failed to connect:", e)
