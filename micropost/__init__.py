import os
from flask import Flask
from flask_sqlalchemy import db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'gantiinidiproduksi')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', None)
db = SQLAlchemy(app)

from micropost import views
