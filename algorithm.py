import pandas as pd
import random

# تحميل البيانات
#باستخدام مكتبة بانداس نستطيع قراءة ملفات ايكسل ونضعها في جداول 
users = pd.read_excel("data/users.xlsx")
products = pd.read_excel("data/products.xlsx")
ratings = pd.read_excel("data/ratings.xlsx")
behavior = pd.read_excel("data/behavior.xlsx")

# دمج البيانات
#نقوم بدمج جدولين السلوكيات والتقييم بناء على رقم المستخدم ورقم المنتج المشترك
# fillna ونحولها الى صفر بعدها باتخدام nan حتى التي لاتحتوي على تقييم وتضيف التقييم بقيمة behavior فائدتها تحافظ على جميع الصفوف في جدول how 
data = behavior.merge(ratings, on=["user_id", "product_id"], how="left")
data = data.fillna(0)

# إعدادات الخوارزمية
POP_SIZE = 10 #عدد الحلول                 
GENS = 5   #عدد الاجيال
REC_SIZE = 5 #عدد المنتجات في كل توصية

#انشاء قائمة بارقام المنتجات ونضعها في متغير
product_ids = products['product_id'].tolist()

# إنشاء حل عشوائي يتكون منتجات بعدد محدد
def create_individual():
    return random.sample(product_ids, REC_SIZE)# rec_size  اختيار ارقام عشوائية من قائمة ارقام المنتجات واختيار عددها نسبة ل

# pop_size إنشاء مجموعة حلول نسبة لعدد الحلول المطلوبة
def create_population():
    return [create_individual() for _ in range(POP_SIZE)]

# دالة التقييم
def fitness(individual, user_id):
    score = 0
    for pid in individual:
        # individual نقوم بالبحث في جدول داتا عن الصف الذي يحوي على رقم السمتخدم المطلوب والمنتج الذي يطابق المنتج المراد من التوصية
        rows = data[(data['user_id'] == user_id) & (data['product_id'] == pid)]
        if not rows.empty:
            # اختيار الصف كامل ووضعه في متغير قاموس للوصول الى كل خانه مطلوبة وتقييمها
            r = rows.iloc[0]
            score += r['clicked'] * 2
            score += r['purchased'] * 5
            score += r['rating']          
    if score == 0:
        score += random.random()
    return score

# اختيار الأفضل
def selection(population, user_id):
    # ترتيب مجموعة الحلول بناء على تقييمها في تابع التقييم من الاكبر للاصغر
    return sorted(population, key=lambda x: fitness(x, user_id), reverse=True)[:POP_SIZE // 2]

# التزاوج
# نقوم باستخدام توصييتين اباء بتوليد توصية جديدة لاضافتها لمجموعة الحلول
def crossover(p1, p2):
    cut = len(p1) // 2 # رقم صحيح يساوي نصف توصية الاب
    child = p1[:cut] + p2[cut:] #توليد التوصية الجديدة بناء على الرقم الصحيح السابق 
    # إزالة التكرار
    child = list(set(child))
    # ضمان 5 عناصر دائمًا
    while len(child) < REC_SIZE:
        new_item = random.choice(product_ids)
        if new_item not in child:
            child.append(new_item)
    return child[:REC_SIZE]
# الطفرة
def mutation(individual):
    if random.random() < 0.3: # شرط يقوم بتوليد رقم بين صفر وواحد 
        # اختيار منتج من توصية واستبداله بمنتج معين بشكل عشوائي
        individual[random.randint(0, len(individual)-1)] = random.choice(product_ids)
    return individual

# تشغيل الخوارزمية
def run_ga(user_id):

    # تحقق من وجود المستخدم
    if user_id not in users["user_id"].values:
        return []

    # إذا المستخدم ما عنده بيانات → توصيات عشوائية
    if data[data['user_id'] == user_id].empty:
        return random.sample(product_ids, REC_SIZE)

    #انشاء مجموعة من التوصيات
    population = create_population()
    for _ in range(GENS):
        # تقييم التوصيات واختيار الافضل ووضعها في متغير وحفظها في متغيير التوصيات الجديدة
        selected = selection(population, user_id)
        new_population = selected.copy()

        while len(new_population) < POP_SIZE:
            # توليد اباء جديدة من التوصيات الافضل
            p1, p2 = random.sample(selected, 2)
            # دمجها وانشاء توصية جديدة ابن
            child = crossover(p1, p2)
            # احداث طفرة في التوصية الابن واضافتها للتوصيات المقيمة
            child = mutation(child)
            new_population.append(child)

        population = new_population
    # باستخدام تابع التقييم score اختيار التوصية الافضل بناء على
    best = max(population, key=lambda x: fitness(x, user_id))
    return best


if __name__ == "__main__":
    user_id = users.iloc[0]['user_id']
    print("Best recommendations:", run_ga(user_id))
