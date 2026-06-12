from app import db
from datetime import datetime
from app.utils.encryption import encrypt, decrypt

class Account(db.Model):
    """Instagram Account Model - نموذج حسابات Instagram"""
    
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    username = db.Column(db.String(100), nullable=False)
    password_encrypted = db.Column(db.String(255), nullable=False)
    
    is_active = db.Column(db.Boolean, default=True)
    last_used = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password: str):
        """Set encrypted password - تعيين كلمة المرور المشفرة"""
        self.password_encrypted = encrypt(password)
    
    def get_password(self) -> str:
        """Get decrypted password - الحصول على كلمة المرور المفكوكة"""
        return decrypt(self.password_encrypted)
    
    def to_dict(self):
        """Convert to dictionary - تحويل لقاموس"""
        return {
            'id': self.id,
            'username': self.username,
            'is_active': self.is_active,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Account {self.username}>'
