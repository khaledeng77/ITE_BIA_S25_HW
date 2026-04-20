from flask import Flask, render_template,request,url_for,redirect
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
@app.route("/",methods=["GET","POST"])
def select_user():
    if request.method=="POST":
        user_id=int(request.form.get("user_id"))
        #تخزين التوصيات الافضل المعطاة من الخوارزمية داخل متغير
        rec_ids = run_ga(user_id)
        if not rec_ids:
            return render_template("select_user.html",error="User is Not Correct")
        # تحويل رقم المنتج الى مواصفاته المطلوبة وتخزينها كقاموس داخل متغير
        recs = [get_product_info(pid) for pid in rec_ids]
        # لعرضها Html ارسال جميع هذه البيانات الى صفحة 
        return render_template("index.html", recs=recs,user_id=user_id)
    return render_template("select_user.html")

if __name__ == "__main__":
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0")

