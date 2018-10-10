from datetime import datetime
from micropost import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(36), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    entries = db.relationship('Entry', backref='user', lazy=True)

    def __repr__(self):
        return 'User {} {}'.format(self.id, self.username)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String())
    body = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Entry {} {} {} {}'.format(self.id, self.user_id, self.timestamp, self.title)
        