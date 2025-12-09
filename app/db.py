# db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(BASE_DIR, 'recipe-db.sqlite3')
DEFAULT_DATABASE_URL = f"sqlite:///{DB_PATH}"
DATABASE_URL = os.environ.get('DATABASE_URL', DEFAULT_DATABASE_URL)

# Initialize database after flask has created the app
ENGINE = None
db_session = scoped_session(sessionmaker())

def init_db(app):
    global ENGINE

    database_url = app.config.get('DATABASE_URL')
    ENGINE = create_engine(database_url, echo=app.config.get('SQL_ALCHEMY_ECHO', False))

    db_session.configure(bind=ENGINE)

    # Create tables for local development
    if app.config.get('CREATE_TABLES', False):
        Base.metadata.create_all(ENGINE)