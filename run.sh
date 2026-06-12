#!/bin/bash

# إنشاء المجلدات المطلوبة
mkdir -p downloads uploads

# تثبيت المكتبات المطلوبة
echo "📦 تثبيت المكتبات..."
pip install -r requirements.txt

# تشغيل التطبيق
echo "🚀 تشغيل التطبيق..."
python app.py
