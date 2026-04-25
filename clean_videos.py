import json
import requests
import os

def clean_dead_links():
    file_path = 'videos.json'
    
    if not os.path.exists(file_path):
        print("❌ ملف videos.json غير موجود.")
        return

    # 1. قراءة البيانات
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            videos = json.load(f)
        except:
            print("❌ خطأ في قراءة ملف JSON.")
            return

    original_count = len(videos)
    # 2. تصفية الروابط (نحتفظ فقط بالروابط الشغالة)
    cleaned_videos = []
    
    print(f"🔍 جاري فحص {original_count} فيديو...")

    for v in videos:
        url = v.get('url')
        if not url:
            continue
            
        try:
            # بنستخدم head عشان نسرع العملية ونوفر باقة السيرفر
            response = requests.head(url, timeout=10)
            
            # لو الرابط شغال (200) ضيفه للقائمة الجديدة
            if response.status_code == 200:
                cleaned_videos.append(v)
            else:
                print(f"🗑️ حذف فيديو بايظ: {v.get('id')} - {response.status_code}")
        except:
            # لو حصل خطأ في الاتصال (سيرفر واقع مثلاً) بنخليه احتياطاً أو ممكن تحذفه
            print(f"⚠️ فشل الاتصال بالرابط: {url}")
            cleaned_videos.append(v)

    # 3. حفظ الملف بعد التنظيف
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_videos, f, ensure_ascii=False, indent=2)

    removed_count = original_count - len(cleaned_videos)
    print(f"✅ تم الانتهاء! حذفنا {removed_count} فيديو بايظ.")

if __name__ == "__main__":
    clean_dead_links()
