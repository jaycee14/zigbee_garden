from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import DATABASE_URL
from models import Base

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={
        "check_same_thread": False
    },
)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine,
                       autoflush=False,
                       autocommit=False,
                       expire_on_commit=False,)