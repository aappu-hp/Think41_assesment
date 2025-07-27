from app.database import Base, engine
from app import models  # ensures all models are registered

# Create all tables
print("📦 Creating tables in the database...")
Base.metadata.create_all(bind=engine)
print("✅ Done.")
