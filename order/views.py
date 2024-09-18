from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .serializers import OrderSereializer
from .models import Order,OrderItem
from product.models import Product

# Create your views here.



#Add new order
@api_view(['POST'])
@permission_classes([IsAuthenticated]) #يعني اليوزر مايقدر يطلب الا اذا كان مسوي لوق ان 
def new_order(request):
    user = request.user        #يجيب الاي دي من التوكين حق اليوزر عشان اعرف مين اليوزر اللي طلب
    data = request.data        #البيانات اللي راح تجيني من اليوزر زي العنوان ورقم الهاتف والمنتجات اللي طلبها
    order_items = data['order_Items']    #المنتجات اللي راح يطلبها اليوزر راح تجيني كداتا زي اسم المنتج والعدد والسعلر وهكذا, لكل منتج يطلبه اليوزر راح يكون لها معلومات لذلك راح يرجع ارراي من المنتجات
    
    if order_items and len(order_items) == 0:  #اذا كان المتغير بفولس يعني مارجع شيء وطوله كان بصفر يعني مارجع شيء والارراي طوله بصفر فيعني ما طلب شيء بس ضغط على زر اطلب
        return Response({"error":"No order recieved"},status=status.HTTP_400_BAD_REQUEST)
    else:    #اذا عنده طلب وحط منتجات
        total_amount = sum(item['price']* item['quantity'] for item in order_items) #راح يحسب سعر التوتال حق المنتجات
        order = Order.objects.create(   #راح اضيف الطلب في الداتابيس
            user = user,
            city = data['city'],
            zip_code = data['zip_code'],
            street = data['street'],
            state = data['state'],
            country = data['country'],
            phoneNo = data['phoneNo'],
            total_amount = total_amount,
        )

        for i in order_items: 
            product = Product.objects.get(id=i['productId'])  #هنا راح اخذ الاي دي حق المنتج ات اللي طلبه اليوزر واستخرج المنتج من الداتابيس
            item = OrderItem.objects.create( #راح اخزن في الداتابيس كل منتج انطلب وهوا تابع لاي طلب وايس اسم المنتج والكممية والسعر
                product = product,
                order = order, 
                name = product.name,
                quantity = i['quantity'],
                price = i['price']
            )
            product.stock -= item.quantity   #ستوك يعني في المستودع كم عندنا من هذا المنتج فلما احد يطلب هذا المنتج ننقص قيمة الستوك
            product.save()

        serializer = OrderSereializer(order,many=False)  #فالس لاني راح ارسل طلب حق شخص واحد
        return Response(serializer.data)
    

#get all orders
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllOrder(request):
    orders = Order.objects.all()
    serializer = OrderSereializer(orders,many=True) 
    return Response({'orders':serializer.data})


#get order by id
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request,pk):
    order = get_object_or_404(Order,id=pk)
    serializer = OrderSereializer(order,many=False)  #فالس لاني راح ارسل طلب حق شخص واحد
    return Response({'order':serializer.data})


#Update status of order 
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser]) #مايدخل هذا الروات الا الادمن المسجل
def updateOrder(request,pk):
    order = get_object_or_404(Order,id=pk)
    order.order_status = request.data['status']
    order.save()
    serializer = OrderSereializer(order,many=False)  #فالس لاني راح ارسل طلب حق شخص واحد
    return Response({'order':serializer.data})


#Delete order
@api_view(['DELETE'])
@permission_classes([IsAuthenticated]) #يعني اليوزر مايقدر يحذف شيء الا اذا كان مسوي لوق ان 
def deleteOrder(request, pk):
    order = get_object_or_404(Order,id=pk)
    order.delete()
    return Response({'message':"order is delete"})
        
    





   
    

    

    
