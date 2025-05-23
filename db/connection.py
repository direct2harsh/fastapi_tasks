from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# TODO move the creds to the env file
# tasks is the database name
POSTGRES_URL = "postgresql+psycopg2://root:root@postgres_db/jasper"

engine = create_engine(POSTGRES_URL,echo=True,pool_size=20,max_overflow=10)

session = sessionmaker(bind=engine, autoflush=False,)

DeclarativeBase = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

