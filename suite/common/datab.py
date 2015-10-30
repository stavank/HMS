from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from app import application
import config


# configure Session class with desired options
Session = sessionmaker()

# later, we create the engine
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

# associate it with our custom Session class
Session.configure(bind=engine)

# Base for models for each DB table
BaseForModels = declarative_base()
try:
    db = SQLAlchemy(application)
    BaseForModels = db.Model
except ImportError:
    pass
