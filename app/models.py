from app.extensions import db 
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
class Task(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    task=db.Column(db.String(50))
    status=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    priority=db.Column(db.String,default="Low")
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    
    def to_dict(self):
        return{
            "id":self.id,
            "status":self.status,
            "task":self.task,
            "created_at":self.created_at.isoformat(),
            "priority":self.priority,
            "user_id":self.user_id
            }

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True,nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password_hash=db.Column(db.String(200),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

