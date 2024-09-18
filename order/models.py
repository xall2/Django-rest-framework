from django.db import models
from operator import mod #باقي القسمة
from django.contrib.auth.models import User
from product.models import Product



#هذا الكلاس زي الخيارات حق الدروب داون ليست
class OrderStatus(models.TextChoices):
    PROCCESSING = 'Proccessing'  #معالجة طلب اليوزر
    SHIPPED   = 'Shipped'   #شحن الطلبية
    DELIVERED = 'Delivered' #تم استلامها العميل


#هذا الكلاس زي الخيارات حق الدروب داون ليست
class PaymentStatus(models.TextChoices):
    PAID = 'Paid'  
    UNPAID   = 'Unpaid'  


class PaymentMode(models.TextChoices):
    COD = 'Code'  #يدفع عند الاستلام
    CARD   = 'Card'  #يدفع اونلاين بالكارد 




class Order(models.Model):
    city = models.CharField(max_length=400, default="",blank=False)
    zip_code = models.CharField(max_length=100, default="",blank=False)
    street = models.CharField(max_length=500, default="",blank=False)
    state = models.CharField(max_length=100, default="",blank=False)
    country = models.CharField(max_length=100, default="",blank=False)
    phoneNo = models.CharField(max_length=500, default="",blank=False)
    total_amount = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=30,choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    payment_mode = models.CharField(max_length=30,choices=PaymentMode.choices, default=PaymentMode.COD)
    order_status = models.CharField(max_length=60,choices=OrderStatus.choices, default=OrderStatus.PROCCESSING)
    user = models.ForeignKey(User ,null=True, on_delete=models.SET_NULL)#عشان اعرف مين اليوزر اللي طلب هذا المنتج
    createAt = models.DateTimeField(auto_now_add=True)


    def __str__(self): 
        return  str(self.id)
    

#المنتج اللي طلبها
class OrderItem(models.Model):
    product = models.ForeignKey(Product ,null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order ,null=True, related_name='orderItems', on_delete=models.CASCADE) #لان لما احذف الطلب الطلبية راح تنحذف
    name = models.CharField(max_length=60,blank=False, default="") #اسم المنتج اللي طلبه
    quantity = models.IntegerField(default=1) #كم العدد اللي طلبه من هذا المنتج
    price = models.DecimalField(max_digits=7, decimal_places=2,blank=False)

    def __str__(self): 
        return self.name




    


