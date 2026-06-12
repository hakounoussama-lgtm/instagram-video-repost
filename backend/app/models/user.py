from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import bcrypt

class User(db.Model):
    """User Model - نموذج المستخدم"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    avatar_url = db.Column(db.String(500))
    bio = db.Column(db.Text)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # 2FA
    two_factor_enabled = db.Column(db.Boolean, default=False)
    two_factor_secret = db.Column(db.String(32))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    repost_tasks = db.relationship('RepostTask', backref='user', lazy=True, cascade='all, delete-orphan')
    accounts = db.relationship('Account', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password: str):
        """Set password - تعيين كلمة المرور"""
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt(12)
        ).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Check password - التحقق من كلمة المرور"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
    
    def to_dict(self):
        """Convert to dictionary - تحويل لقاموس"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'avatar_url': self.avatar_url,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
