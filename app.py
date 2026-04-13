from flask import Flask, render_template
from algorithm import run_ga, products
import os
#انشاء تطبيق الويب وتعريفه على مكان المشروع للوصل الى كافة الملفات
app = Flask(__name__)

# الى معلومات المنتج IDs تحويل 
def get_product_info(pid):
    # المطلوب بمعلوماته الكاملة للمنتج id اختيار المنتج المطابق لل
    row = products[products['product_id'] == pid].iloc[0]
    # مثلا Html وارجاعها كقاموس لتسهيل الوصول اليها وارسالها الى 
    return {        
        "id": pid,
        "category": row['category'],
        "price": row['price']
    }

# تقوم بربط الرابط المعطى بالدالة المطلوب تشغيلها
@app.route("/")
# الدالة الرئيسية
def home():
    #تحديد المستخدم المراد
    user_id = 1
    #تخزين التوصيات الافضل المعطاة من الخوارزمية داخل متغير
    rec_ids = run_ga(user_id)
    # تحويل رقم المنتج الى مواصفاته المطلوبة وتخزينها كقاموس داخل متغير
    recs = [get_product_info(pid) for pid in rec_ids]
    # لعرضها Html ارسال جميع هذه البيانات الى صفحة 
    return render_template("index.html", recs=recs)

if __name__ == "__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0")

# app.run(debug=True)
