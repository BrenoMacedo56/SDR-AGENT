from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import Settings

engine = create_engine(Settings.DATABASE_URL, echo=Settings.DEBUG)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)





























