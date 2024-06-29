from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from loadenv import load_env

env_vars = load_env()
POSTGRES_USER = env_vars['POSTGRES_USER']
POSTGRES_PASSWORD = env_vars['POSTGRES_PASSWORD']
POSTGRES_HOST = env_vars['POSTGRES_HOST']
POSTGRES_PORT = env_vars['POSTGRES_PORT']
POSTGRES_DB = env_vars['POSTGRES_DB']

SQLALCHEMY_DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()