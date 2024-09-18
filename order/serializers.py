from rest_framework import serializers
from .models import Order,OrderItem



class OrderItemSereializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"




class OrderSereializer(serializers.ModelSerializer):
    #عشان نشوف المنتجات اللي طلبها اليوزر راح تظهر لما نستعرض معلومات الطلبية
    OrderItems = serializers.SerializerMethodField(method_name="get_order_items", read_only=True)


    class Meta:
        model = Order
        fields = "__all__"
    
    def get_order_items(self,obj):
        order_items = obj.orderItems.all() #هذا المتغير اللي كان مع الريلاتيدنيم اللي في جدول الاوردرايتيم عند المتغير اوردر
        serializer = OrderItemSereializer(order_items,many=True)
        return serializer.data


