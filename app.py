from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from instagram_client import InstagramRepostClient
import os
import threading
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instagram_repost.db'
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# نموذج قاعدة البيانات
class RepostTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instagram_username = db.Column(db.String(100), nullable=False)
    target_url = db.Column(db.String(500), nullable=False)
    target_username = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')
    video_count = db.Column(db.Integer, default=0)
    message = db.Column(db.Text, default='')

    def to_dict(self):
        return {
            'id': self.id,
            'instagram_username': self.instagram_username,
            'target_url': self.target_url,
            'target_username': self.target_username,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'video_count': self.video_count,
            'message': self.message
        }

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# API لبدء عملية إعادة النشر
@app.route('/api/start-repost', methods=['POST'])
def start_repost():
    try:
        data = request.json
        instagram_username = data.get('instagram_username', '').strip()
        instagram_password = data.get('instagram_password', '').strip()
        target_url = data.get('target_url', '').strip()
        
        if not all([instagram_username, instagram_password, target_url]):
            return jsonify({'error': 'جميع الحقول مطلوبة'}), 400
        
        # استخراج اسم المستخدم من الرابط
        target_username = extract_username(target_url)
        if not target_username:
            return jsonify({'error': 'رابط حساب غير صحيح'}), 400
        
        # إنشاء مهمة جديدة
        task = RepostTask(
            instagram_username=instagram_username,
            target_url=target_url,
            target_username=target_username,
            status='processing',
            message='جاري المعالجة...'
        )
        db.session.add(task)
        db.session.commit()
        
        # تشغيل العملية في خيط منفصل
        thread = threading.Thread(
            target=process_repost,
            args=(task.id, instagram_username, instagram_password, target_username)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'بدأت عملية إعادة النشر',
            'task_id': task.id
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ: {str(e)}'}), 500

# دالة معالجة إعادة النشر
def process_repost(task_id, username, password, target_username):
    try:
        task = RepostTask.query.get(task_id)
        if not task:
            return
        
        # إنشاء عميل Instagram
        client = InstagramRepostClient()
        
        # تسجيل الدخول
        if not client.login(username, password):
            task.status = 'failed'
            task.message = 'فشل تسجيل الدخول - تحقق من بيانات الدخول'
            db.session.commit()
            return
        
        # إعادة نشر الفيديوهات
        videos = client.repost_videos(target_username, amount=5)
        
        task.video_count = len(videos)
        if len(videos) > 0:
            task.status = 'completed'
            task.message = f'تم نشر {len(videos)} فيديوهات بنجاح'
        else:
            task.status = 'completed'
            task.message = 'لم يتم العثور على فيديوهات'
        
        db.session.commit()
        
    except Exception as e:
        task = RepostTask.query.get(task_id)
        if task:
            task.status = 'failed'
            task.message = f'خطأ: {str(e)}'
            db.session.commit()

# دالة استخراج اسم المستخدم من الرابط
def extract_username(url):
    try:
        # إزالة http/https
        url = url.replace('https://', '').replace('http://', '')
        # إزالة www
        url = url.replace('www.', '')
        # استخراج اسم المستخدم
        if 'instagram.com/' in url:
            username = url.split('instagram.com/')[1].strip('/')
            return username if username else None
        return None
    except:
        return None

# API للحصول على حالة المهمة
@app.route('/api/task-status/<int:task_id>', methods=['GET'])
def get_task_status(task_id):
    task = RepostTask.query.get(task_id)
    if not task:
        return jsonify({'error': 'المهمة غير موجودة'}), 404
    return jsonify(task.to_dict()), 200

# API للحصول على جميع المهام
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = RepostTask.query.order_by(RepostTask.created_at.desc()).all()
    return jsonify([task.to_dict() for task in tasks]), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # إنشاء المجلدات المطلوبة
        os.makedirs('downloads', exist_ok=True)
        os.makedirs('uploads', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
