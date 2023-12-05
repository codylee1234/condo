from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

db = SQLAlchemy()

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(255))
    userid = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.String(100))

class cars(db.Model):
    carsid = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(255))
    model = db.Column(db.String(255))

class request_srv(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    req_dt = db.Column(db.DateTime)
    req_type = db.Column(db.Integer)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    subject = db.Column(db.String(1000))
    details = db.Column(db.String(4000))
    work_type = db.Column(db.String(4000))
    from_dt = db.Column(db.DateTime)
    to_dt = db.Column(db.DateTime)
    v_name = db.Column(db.String(200))
    vehicle_no = db.Column(db.String(100))
    ph_number = db.Column(db.BigInteger)
    id_details = db.Column(db.String(200))
    status = db.Column(db.String(10))
    rating = db.Column(db.Integer)
    feedback = db.Column(db.String(1000))


    # Define the relationship
    user = db.relationship('users', backref=db.backref('request_srv', lazy=True))

class announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_dt = db.Column(db.String(255))
    details = db.Column(db.String(4000))
    userid = db.Column(db.Integer)
