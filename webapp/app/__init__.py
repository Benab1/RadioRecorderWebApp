from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from app.json_encoder import AlchemyEncoder
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.json_encoder = AlchemyEncoder

from app import views, models
