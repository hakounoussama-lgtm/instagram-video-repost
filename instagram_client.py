from instagrapi import Client
import os
import time

class InstagramRepostClient:
    """عميل Instagram متقدم لإعادة النشر"""
    
    def __init__(self):
        self.client = Client()
        self.logged_in = False
    
    def login(self, username, password):
        """تسجيل الدخول إلى حساب Instagram"""
        try:
            self.client.login(username, password)
            self.logged_in = True
            print(f"✅ تم تسجيل الدخول: {username}")
            return True
        except Exception as e:
            print(f"❌ فشل تسجيل الدخول: {str(e)}")
            self.logged_in = False
            return False
    
    def get_user_info(self, username):
        """الحصول على معلومات المستخدم"""
        try:
            user = self.client.user_info_by_username(username)
            return user
        except Exception as e:
            print(f"❌ خطأ في الحصول على معلومات المستخدم: {str(e)}")
            return None
    
    def get_user_medias(self, user_id, amount=20):
        """الحصول على الفيديوهات من حساب المستخدم"""
        try:
            medias = self.client.user_medias(user_id, amount=amount)
            videos = []
            
            for media in medias:
                # media_type: 1 = صورة، 2 = فيديو، 8 = كاروسيل
                if media.media_type in [2, 8]:
                    videos.append({
                        'id': media.id,
                        'caption': media.caption or '',
                        'media_type': media.media_type,
                        'taken_at': media.taken_at,
                        'pk': media.pk
                    })
            
            print(f"✅ تم جلب {len(videos)} فيديو")
            return videos
        except Exception as e:
            print(f"❌ خطأ في جلب الفيديوهات: {str(e)}")
            return []
    
    def download_video(self, media_pk, filename):
        """تحميل الفيديو"""
        try:
            # إنشاء مجلد التحميل إذا لم يكن موجوداً
            os.makedirs('downloads', exist_ok=True)
            
            filepath = os.path.join('downloads', filename)
            
            media = self.client.media_info(media_pk)
            if media.media_type == 2:  # فيديو
                self.client.video_download(media_pk, filepath)
                print(f"✅ تم تحميل الفيديو: {filename}")
                return filepath
            elif media.media_type == 8:  # كاروسيل
                # محاولة تحميل أول فيديو من الكاروسيل
                if hasattr(media, 'resources') and media.resources:
                    for resource in media.resources:
                        if resource.media_type == 2:
                            self.client.video_download(media_pk, filepath)
                            print(f"✅ تم تحميل الفيديو: {filename}")
                            return filepath
        except Exception as e:
            print(f"❌ خطأ في تحميل الفيديو: {str(e)}")
        
        return None
    
    def upload_video(self, video_path, caption):
        """نشر الفيديو على حسابك"""
        try:
            if not os.path.exists(video_path):
                print(f"❌ الملف غير موجود: {video_path}")
                return None
            
            # إضافة إسناد المصدر إذا لم يكن موجوداً
            if not caption:
                caption = "📹 Reposted Content"
            
            result = self.client.video_upload(
                video_path,
                caption=caption,
                upload_users=[],
                location=None
            )
            
            print(f"✅ تم نشر الفيديو بنجاح")
            return result
        except Exception as e:
            print(f"❌ خطأ في نشر الفيديو: {str(e)}")
            return None
    
    def repost_videos(self, target_username, amount=5):
        """إعادة نشر فيديوهات من حساب معين"""
        try:
            if not self.logged_in:
                print("❌ لم تقم بتسجيل الدخول")
                return []
            
            # الحصول على معلومات الحساب المستهدف
            target_user = self.get_user_info(target_username)
            if not target_user:
                print(f"❌ لم يتم العثور على الحساب: {target_username}")
                return []
            
            print(f"🎯 البدء في استخراج الفيديوهات من: {target_username}")
            
            # جلب الفيديوهات
            videos = self.get_user_medias(target_user.pk, amount=amount)
            
            if not videos:
                print(f"❌ لم يتم العثور على فيديوهات في حساب {target_username}")
                return []
            
            reposted = []
            for i, video in enumerate(videos, 1):
                try:
                    video_filename = f"video_{int(time.time())}_{i}.mp4"
                    
                    print(f"\n📥 تحميل الفيديو {i}/{len(videos)}...")
                    
                    # تحميل الفيديو
                    video_path = self.download_video(video['pk'], video_filename)
                    
                    if video_path and os.path.exists(video_path):
                        print(f"📤 نشر الفيديو {i}/{len(videos)}...")
                        
                        # نشر الفيديو بنفس التعليق والهاشتاغات
                        caption = video['caption']
                        if self.upload_video(video_path, caption):
                            reposted.append(video)
                            print(f"✅ تم نشر الفيديو {i}/{len(videos)} بنجاح")
                        
                        # حذف الملف المحمل
                        try:
                            os.remove(video_path)
                            print(f"🗑️ تم حذف الملف المؤقت")
                        except:
                            pass
                        
                        # انتظر قليلاً بين كل نشر لتجنب التقيد
                        time.sleep(5)
                    
                except Exception as e:
                    print(f"❌ خطأ في معالجة الفيديو {i}: {str(e)}")
                    continue
            
            print(f"\n✅ تم إعادة نشر {len(reposted)} فيديو من أصل {len(videos)}")
            return reposted
        
        except Exception as e:
            print(f"❌ خطأ في عملية إعادة النشر: {str(e)}")
            return []


if __name__ == "__main__":
    # مثال على الاستخدام
    client = InstagramRepostClient()
    
    # تسجيل الدخول
    if client.login("your_username", "your_password"):
        # إعادة نشر الفيديوهات
        client.repost_videos("target_username", amount=5)
