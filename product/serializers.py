from rest_framework import serializers
from .models import Product,Review



class ProductSerializers(serializers.ModelSerializer):

    #هذا الكود خاص باسترجع الريفيوز
    review = serializers.SerializerMethodField(method_name='get_reviews', read_only=True) #نعطيه اسم الفنكشن اللي سويناه تحت, ريد اونلي يعني مايتم التلاعب بهذا الفنكشن

    #من خلال هذا الكلاس اقول ايش الداتا المسموح انها تؤخذ من الدتابيس
    class Meta:
        model = Product
        fields = "__all__" #['name','price'] اذا بختار خانات معينة عشان يرجعها على شكل جيسون
    
    #فنكشن  يرجع كل الريفيو الخاص ببرودكت معين
    def get_reviews(self,obj):#اوبجكت لانه راح يرجع اوبجكت 
        reviews = obj.reviews.all() #هذا المتغير اللي كان في جدول الريفيو عند المتغير برودكت
        serializer = ReviewSerializers(reviews,many=True) #يحول الريفيو لصيغة جيسون
        return serializer.data




class ReviewSerializers(serializers.ModelSerializer):

    #من خلال هذا الكلاس اقول ايش الداتا المسموح انها تؤخذ من الدتابيس
    class Meta:
        model = Review
        fields = "__all__" 
