import os
from flask import Flask
from flask_sqlalchemy import db
from whitenoise import WhiteNoise

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'gantiinidiproduksi')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.wsgi_app = WhiteNoise(app.wsgi_app, root='/static')
db = SQLAlchemy(app)

from micropost import views
