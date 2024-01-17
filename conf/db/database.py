from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from conf.settings import Settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{Settings.POSTGRES_USER}:{Settings.POSTGRES_PASSWORD}"
    f"@{Settings.POSTGRES_HOST}:{Settings.POSTGRES_PORT}/{Settings.POSTGRES_DB}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()