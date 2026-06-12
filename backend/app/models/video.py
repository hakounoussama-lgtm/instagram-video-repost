from app import db
from datetime import datetime

class Video(db.Model):
    """Video Model - نموذج الفيديوهات"""
    
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('repost_tasks.id'), nullable=False, index=True)
    
    instagram_id = db.Column(db.String(100), unique=True, nullable=False)
    source_username = db.Column(db.String(100), nullable=False)
    
    caption = db.Column(db.Text)
    hashtags = db.Column(db.JSON)  # Store as list
    
    media_type = db.Column(db.String(20))  # video, carousel, reel
    duration = db.Column(db.Integer)  # in seconds
    
    # URLs
    download_url = db.Column(db.String(500))
    local_path = db.Column(db.String(500))
    
    # Status
    status = db.Column(db.String(50), default='downloaded')  # downloaded, posted, failed
    posted_at = db.Column(db.DateTime)
    
    # Metadata
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary - تحويل لقاموس"""
        return {
            'id': self.id,
            'instagram_id': self.instagram_id,
            'source_username': self.source_username,
            'caption': self.caption,
            'hashtags': self.hashtags,
            'status': self.status,
            'posted_at': self.posted_at.isoformat() if self.posted_at else None,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Video {self.instagram_id}>'
