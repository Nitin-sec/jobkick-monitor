from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from monitor.config import Config

Base = declarative_base()

engine = create_engine(
    f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}",
    pool_pre_ping=True
)

SessionLocal = scoped_session(sessionmaker(bind=engine))

def init_db():
    from monitor import models
    Base.metadata.create_all(bind=engine)