from app import db
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    """Task Status Enum - حالات المهمة"""
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

class RepostTask(db.Model):
    """Repost Task Model - نموذج مهام إعادة النشر"""
    
    __tablename__ = 'repost_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    task_id = db.Column(db.String(36), unique=True, index=True)  # Celery task ID
    
    # Configuration
    target_username = db.Column(db.String(100), nullable=False)
    video_limit = db.Column(db.Integer, default=5)
    include_hashtags = db.Column(db.Boolean, default=True)
    include_captions = db.Column(db.Boolean, default=True)
    
    # Status & Results
    status = db.Column(
        db.Enum(TaskStatus),
        default=TaskStatus.PENDING,
        nullable=False,
        index=True
    )
    videos_found = db.Column(db.Integer, default=0)
    videos_processed = db.Column(db.Integer, default=0)
    videos_posted = db.Column(db.Integer, default=0)
    
    # Error Info
    error_message = db.Column(db.Text)
    error_details = db.Column(db.JSON)
    
    # Progress
    progress_percentage = db.Column(db.Integer, default=0)
    current_step = db.Column(db.String(200))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def update_status(self, status: TaskStatus):
        """Update task status - تحديث حالة الم��مة"""
        self.status = status
        self.updated_at = datetime.utcnow()
        if status == TaskStatus.PROCESSING and not self.started_at:
            self.started_at = datetime.utcnow()
        elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            self.completed_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary - تحويل لقاموس"""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'target_username': self.target_username,
            'status': self.status.value,
            'videos_found': self.videos_found,
            'videos_processed': self.videos_processed,
            'videos_posted': self.videos_posted,
            'progress_percentage': self.progress_percentage,
            'current_step': self.current_step,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    def __repr__(self):
        return f'<RepostTask {self.id} - {self.status.value}>'
