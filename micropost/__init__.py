import os
from flask import Flask
from flask_sqlalchemy import db

app = Flask(__name__)
db = SQLAlchemy(app)

from journal import views
