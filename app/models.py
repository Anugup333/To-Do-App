from app import db
from app import get_indian_time

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(20),nullable= False)
    created_at = db.Column(db.DateTime, default=get_indian_time)
    last_login = db.Column(db.DateTime)

    # one-to-many relationship

    tasks = db.relationship('Task',backref='user',lazy=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100),nullable=False)
    status = db.Column(db.String(20),default="Pending")
    created_at = db.Column(db.DateTime, default=get_indian_time)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
