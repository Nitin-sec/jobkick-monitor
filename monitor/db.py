from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from urllib.parse import quote_plus
from monitor.config import Config

Base = declarative_base()

engine = create_engine(
    f"mysql+pymysql://{quote_plus(Config.DB_USER)}:{quote_plus(Config.DB_PASSWORD)}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}",
    pool_pre_ping=True,
    pool_recycle=1800,
    future=True,
)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
)

def init_db():
    from monitor import models  # noqa: F401
    Base.metadata.create_all(bind=engine)