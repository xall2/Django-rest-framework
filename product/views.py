from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Product, Review
from .serializers import ProductSerializers
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Avg


#get all product
@api_view(['GET'])
def getAllProducts(request):
    products = Product.objects.all() #نرجع كل الداتا
    serializers = ProductSerializers(products,many=True) #عشان يترجم الشيء اللي راح يرجع على شكل جيسون عشان يظهر في بوستمان على شكل جيسون
    return Response({"products":serializers.data})


#get product by id
@api_view(['GET'])
def getByIdProduct(request, pk): #اللي هوا الاي دي اللي راح يتمررpk
    product = get_object_or_404(Product, id=pk) #يعني راح يرجع الاوبجكت على حسب الاي دي واذا مالقاه يرجع ايرور404
    serializers = ProductSerializers(product,many=False) #فالس لانه لانه ماراح يجيب اكثر من برودكت
    return Response({"products":serializers.data})



#filter product 
@api_view(['GET'])
def filterProduct(request):
    filters = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id')) #هذا الكلاس اللي سويناه في ملف الفيلتر ونعطيه هذا البراميتر
    #count = filters.qs.count() #عدد العناصر اللي راح ترجع من الفلتر
    serializers = ProductSerializers(filters.qs,many=True) #ترو لانه لانه راح يجيب اكثر من برودكت
    return Response({"products":serializers.data})



#pagination
@api_view(['GET'])
def pagination(request):
    filters = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id')) #هذا الكلاس اللي سويناه في ملف الفيلتر ونعطيه هذا البراميتر
    #count = filters.qs.count() #عدد العناصر اللي راح ترجع من الفلتر
    paginator = PageNumberPagination() #كلاس نستدعيه
    paginator.page_size = 2 #في كل صفحة كم اوبجكت تبغاه يكون موجود
    queryset = paginator.paginate_queryset(filters.qs, request) #مع الريكويست راح يتمرر عدد الصفحات
    serializers = ProductSerializers(queryset,many=True) 
    return Response({"products":serializers.data})




#Add product to Database
@api_view(['POST'])
@permission_classes([IsAuthenticated]) #يعني اليوزر مايقدر يضيف شيء الا اذا كان مسوي لوق ان 
def addNewProduct(request):
    data = request.data  #البيانات اللي راح تجيني من اليوزر
    serializers = ProductSerializers(data= data) 
    if serializers.is_valid():   #اتحقق اذا اليوزر دخل المعلومات صح
        product = Product.objects.create(**data, user = request.user) 
        res = ProductSerializers(product, many=False)
        return Response({"products":res.data})
    else:
        return Response(serializers.errors)
    


#Update product
@api_view(['PUT'])
@permission_classes([IsAuthenticated]) #يعني اليوزر مايقدر يعدل شيء الا اذا كان مسوي لوق ان 
def updateProduct(request, pk):
    product = get_object_or_404(Product, id=pk)    

    if product.user != request.user:    #اذا اليوزر اللي انشيء البرودكت مو نفس اليوزر اللي راح يجيني انه سوا لوق ان: لان كل واحد يعدل على منتجاته هوا مو غيره
        return Response({"error":"Sorry you can not update this product!!!"},status=status.HTTP_403_FORBIDDEN)
    
    #اما اذا كان اليوزر هوا نفسه حقه البرودكت فيقدر يعدل عليه
    product.name = request.data['name']
    product.description = request.data['description']
    product.price = request.data['price']
    product.brand = request.data['brand']
    product.category = request.data['category']
    product.ratings = request.data['ratings']
    product.stock = request.data['stock']
    product.save()

    serializers = ProductSerializers(product, many=False) #ارسل للمستخدم انه صار تحديث للبيانات واعرضله عن طريق السيرلايز
    return Response({"products":serializers.data})



#Delete product
@api_view(['DELETE'])
@permission_classes([IsAuthenticated]) #يعني اليوزر مايقدر يحذف شيء الا اذا كان مسوي لوق ان 
def deleteProduct(request, pk):
    product = get_object_or_404(Product, id=pk)  

    if product.user != request.user:    #اذا اليوزر اللي انشيء البرودكت مو نفس اليوزر اللي راح يجيني انه سوا لوق ان: لان كل واحد يعدل على منتجاته هوا مو غيره
        return Response({"error":"Sorry you can not update this product!!!"},status=status.HTTP_403_FORBIDDEN)
    
    product.delete() #اذا اليوزر اللي مسوي لوق ان حقه البرودكت راح يقد يحذف
    return Response({"message":"The product is delete"},status=status.HTTP_200_OK)



#Add review
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def addReview(request, pk): #لازم يكون عندي الاي دي حق المنتج عشان يسوي عليه تقييم

    user = request.user  #يجيب الاي دي من التوكين حق اليوزر عشان اعرف مين اللي سوا التقييم
    data = request.data  #يحط الداتا اللي دخلها اليوزر زي الملاحظة والتقييم
    product = get_object_or_404(Product, id=pk)  #يحط البرودكت اللي يبغى اليوزر يقييمه
    
    #راح يرجع الريفيو كلها حق هذا البرودكت وبعدين يسوي فلتر ويجيب الريفيو حق هذا اليوزر اذا قد سوا ريفيو
    review = product.reviews.filter(user = user) #هذا الريفيوز جبناه من الريلاتيد نيم من الاتريبيوت اللي في المودل حق الريفيو عند المتغير برودكت
    
    if data['rating']<=0 or data['rating']>5: #يعني المفروض الريتينق مايكون اقل من صفر ولا اكبر من خمسة
        return Response({"error":"Only from 1 to 5"},status=status.HTTP_400_BAD_REQUEST)
    
    elif review.exists(): #اذا اليوزر هذا قد سوا ريفيو على هذا البرودكت فراح نحدث الريفيو حقه
     new_review = {'rating':data['rating'], 'comment':data['comment']} #اخذ الرايتينق والكومنت اللي كتبه
     review.update(**new_review) #ثم اسوي ابديت بحيث اضيف ذي البيانات

     rating = product.reviews.aggregate(avg_ratings = Avg('rating'))#اجمع كل الريفوز اللي صارت على هذا البرودكت ثم اخذ الافرج 
     product.ratings = rating['avg_ratings']#ثم اخزن الافرج هنا: هذا الرايتينق اللي محطوط مع كل برودكت 
     product.save()#ثم احفظ البرودكت لان عدلنا عليه
     return Response({'message':'Product review updated'})
    
    else:  #اذا هذا اليوزر ما قد قيم على هذا البرودكت فأضيف تقييم جديد
        Review.objects.create(
            user = user,
            product = product,
            rating = data['rating'],
            comment = data['comment'],
        )
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))#اجمع كل الريفوز اللي صارت على هذا البرودكت ثم اخذ الافرج 
        product.ratings = rating['avg_ratings']#ثم اخزن الافرج هنا: هذا الرايتينق اللي محطوط مع كل برودكت 
        product.save()#ثم احفظ البرودكت لان عدلنا عليه
        return Response({'message':'Product review created'})
        




#delete review
@api_view(['DELETE'])
@permission_classes([IsAuthenticated]) 
def deleteReview(request, pk):
    user = request.user
    product = get_object_or_404(Product, id=pk)  #يحط البرودكت اللي يبغى اليوزر يقييمه
    #راح يرجع الريفيو كلها حق هذا البرودكت وبعدين يسوي فلتر ويجيب الريفيو حق هذا اليوزر اذا قد سوا ريفيو
    review = product.reviews.filter(user = user) #هذا الريفيوز جبناه من الريلاتيد نيم من الاتريبيوت اللي في المودل حق الريفيو عند المتغير برودكت
    
    if review.exists(): #اذا اليوزر هذا قد سوا ريفيو على هذا البرودكت فراح نحدث الريفيو حقه
        review.delete()
        #لاني حذف ريفيو فلازم ارجع احسب الافرج 
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))#اجمع كل الريفوز اللي صارت على هذا البرودكت ثم اخذ الافرج 
        if rating['avg_ratings'] is None: #اذا الريفيو اللي حذفته هوا الريفيو الوحيد فأحط الرايتينق حقه بصفر
            rating['avg_ratings'] = 0
            product.ratings = rating['avg_ratings']#ثم اخزن القيمة هنا: هذا الرايتينق اللي محطوط مع كل برودكت 
            product.save()#ثم احفظ البرودكت لان عدلنا عليه
            return Response({'message':'Product review deleted'})
    else:
        return Response({"error":"Review not found"},status=status.HTTP_404_NOT_FOUND)
    

     


