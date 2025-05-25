from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

USER = os.environ.get('DBUSER')
print(USER)
PASSWORD = os.environ.get('DBPASSWORD')
print(PASSWORD)

# tasks is the database name
POSTGRES_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@postgres_db/jasper"
print(POSTGRES_URL)

engine = create_engine(POSTGRES_URL,echo=True,pool_size=20,max_overflow=10)

session = sessionmaker(bind=engine, autoflush=False,)

DeclarativeBase = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

