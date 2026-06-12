# Instagram Video Repost - نسخة احترافية

🚀 **تطبيق احترافي متقدم لتحميل وإعادة نشر فيديوهات Instagram**

## ✨ المميزات

### الأمان
- ✅ تشفير قوي للبيانات الحساسة (AES-256)
- ✅ JWT Tokens للمصادقة
- ✅ CSRF Protection
- ✅ Rate Limiting
- ✅ Input Validation و Sanitization
- ✅ SQL Injection Prevention

### الأداء
- ✅ Redis Cache للأداء العالي
- ✅ Database Connection Pooling
- ✅ Async Tasks مع Celery
- ✅ Background Processing
- ✅ Optimized Queries

### المعمارية
- ✅ Clean Architecture (MVC Pattern)
- ✅ Design Patterns (Repository, Factory, Singleton)
- ✅ Dependency Injection
- ✅ Middleware System
- ✅ Service Layer

### المراقبة والتسجيل
- ✅ Comprehensive Logging
- ✅ Error Tracking
- ✅ Performance Monitoring
- ✅ Audit Trail
- ✅ Health Checks

### الاختبار
- ✅ Unit Tests
- ✅ Integration Tests
- ✅ API Tests
- ✅ Test Coverage Reports

### DevOps
- ✅ Docker & Docker Compose
- ✅ CI/CD Pipeline (GitHub Actions)
- ✅ Production Ready Configuration
- ✅ Environment Management

### الواجهة الأمامية
- ✅ React Modern UI
- ✅ TypeScript
- ✅ State Management (Redux)
- ✅ Real-time Updates (WebSockets)
- ✅ Responsive Design

## 📋 المتطلبات

- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Redis 6+
- Docker (اختياري)

## 🚀 التثبيت السريع

### 1. استنساخ المشروع
```bash
git clone https://github.com/hakounoussama-lgtm/instagram-video-repost.git
cd instagram-video-repost
```

### 2. استخدام Docker (الأسهل)
```bash
docker-compose up -d
```

ثم افتح: `http://localhost:3000`

### 3. التثبيت اليدوي

#### Backend
```bash
# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # أو venv\Scripts\activate على Windows

# تثبيت المكتبات
pip install -r requirements.txt

# إعداد قاعدة البيانات
alembic upgrade head

# تشغيل Celery
celery -A app.celery worker --loglevel=info

# تشغيل Redis
redis-server

# تشغيل الخادم
python run.py
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## 📖 الاستخدام

### 1. التسجيل
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "username": "myusername"
}
```

### 2. تسجيل الدخول
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

### 3. بدء عملية إعادة النشر
```bash
POST /api/repost/start
Authorization: Bearer YOUR_JWT_TOKEN
Content-Type: application/json

{
  "instagram_username": "your_instagram_username",
  "instagram_password": "your_instagram_password",
  "target_username": "target_account",
  "video_limit": 5,
  "include_hashtags": true
}
```

### 4. متابعة الحالة
```bash
GET /api/repost/status/{task_id}
Authorization: Bearer YOUR_JWT_TOKEN
```

## 🏗️ هيكل المشروع

```
instagram-video-repost/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/           # قوالب قاعدة البيانات
│   │   ├── routes/           # المسارات والـ Endpoints
│   │   ├── services/         # منطق الأعمال
│   │   ├── schemas/          # تحقق من البيانات
│   │   ├── utils/            # أدوات مساعدة
│   │   ├── middleware/       # البرنامج الوسيط
│   │   └── celery_tasks.py   # المهام غير المتزامنة
│   ├── migrations/           # قاعدة البيانات
│   ├── tests/                # الاختبارات
│   ├── config.py             # الإعدادات
│   ├── requirements.txt      # المكتبات
│   └── run.py                # نقطة الدخول
├── frontend/
│   ├── src/
│   │   ├── components/       # مكونات React
│   │   ├── pages/            # الصفحات
│   │   ├── services/         # خدمات API
│   │   ├── redux/            # إدارة الحالة
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
├── docker-compose.yml
├── Dockerfile
└── .github/workflows/         # CI/CD
```

## 🔒 الأمان

### متغيرات البيئة
```bash
# .env
FLASK_ENV=production
SECRET_KEY=your-very-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/instagram_repost
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your-jwt-secret-key

# Instagram API
INSTAGRAM_SESSION_FILE=instagram_session.json
```

### الممارسات الأمنية
1. **استخدم HTTPS** في الإنتاج
2. **لا تخزن كلمات المرور** في ملفات السجل
3. **استخدم بيئات منفصلة** (Development, Staging, Production)
4. **حدّث المكتبات بانتظام**
5. **استخدم Web Application Firewall (WAF)**

## 📊 المراقبة

### عرض السجلات
```bash
# Backend logs
tail -f logs/app.log

# Celery logs
tail -f logs/celery.log
```

### الإحصائيات
- URL: `http://localhost:5000/api/stats`
- Tasks Completed
- Videos Processed
- Errors Count
- Average Processing Time

## 🧪 الاختبار

```bash
# تشغيل جميع الاختبارات
pytest

# اختبارات محددة
pytest tests/test_auth.py -v

# Coverage Report
pytest --cov=app tests/
```

## 🚀 النشر

### على Heroku
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### على AWS
```bash
# استخدم CloudFormation أو Terraform
cd infrastructure/
terraform apply
```

### على DigitalOcean
```bash
# استخدم Docker Compose
docker-compose up -d
```

## 📝 التوثيق

- **Swagger UI**: `http://localhost:5000/api/docs`
- **ReDoc**: `http://localhost:5000/api/redoc`
- **Postman Collection**: `docs/postman_collection.json`

## 🐛 حل المشاكل

### Database Connection Error
```bash
# تحقق من PostgreSQL
psql -U postgres

# تشغيل Migration
alembic upgrade head
```

### Redis Connection Error
```bash
# تحقق من Redis
redis-cli ping

# شغّل Redis
redis-server
```

### Frontend not loading
```bash
cd frontend
npm install
npm start
```

## 📞 الدعم

للمشاكل والاقتراحات:
- GitHub Issues: https://github.com/hakounoussama-lgtm/instagram-video-repost/issues
- Email: support@example.com

## 📄 الترخيص

MIT License - استخدم كما تشاء

---

**آخر تحديث**: 2026
**الإصدار**: 2.0.0
