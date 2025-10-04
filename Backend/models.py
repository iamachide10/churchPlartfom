from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(30),nullable=False)
    email = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(320),nullable=False)
    is_verified = db.Column(db.Boolean,default=False)
    reset_token = db.relationship("ResetToken",back_populates="user",cascade="all, delete-orphan",lazy="select")
    session_storage = db.relationship("SessionStorage",back_populates="user",cascade="all, delete-orphan",lazy="select")


    def hash_password(self,password):
        self.password = generate_password_hash(password)

    def verify_password(self,input_password):
        return check_password_hash(self.password,input_password)
    
    def __repr__(self):
        return f"<User id={self.id}, name={self.user_name}>"
    
    def to_dic(self):
        return {
            "userName":self.user_name,
            "email":self.email,
            "is_verified":self.is_verified
        }
class ResetToken(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    token = db.Column(db.String(320),nullable=False)
    expires_at = db.Column(db.DateTime,nullable=False)
    user = db.relationship("User",back_populates="reset_token")

    def __repr__(self):
        return f"<ResetToken user_id = {self.user_id}>"

class SessionStorage(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    token = db.Column(db.String(512),nullable=False)
    used = db.Column(db.Boolean,default=False)
    user = db.relationship("User",back_populates="session_storage")

    def set_hash(self,token):
        if not self.token or not self.check_hash(token):
            self.token = generate_password_hash(token,method="pbkdf2:sha256",salt_length=16)

    def check_hash(self,input_token):
        return check_password_hash(self.token,input_token)
    
class AudioStorage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    preacher = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(400), nullable=False)
    time_stamp = db.Column(db.String(15), nullable=False)
    original_filename = db.Column(db.String(50),nullable=False)
    filepath = db.Column(db.String(50),nullable=False)
    storage_name = db.Column(db.String(120),nullable=False)