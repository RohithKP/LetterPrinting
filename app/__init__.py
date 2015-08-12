from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__,static_url_path='')
app.config.from_object('config')
import secretary

db = SQLAlchemy(app)
from app import views, models
