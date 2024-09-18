
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password #هذا الهاش حق الباسوورد عشان يشفره
from rest_framework import status #هل انشىء مستخدم او صار فيه خلل خلال انشاء المستخدم او المستخدم موجود
from .serializer import SignUpSerializers, UserSerializers
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone


#register
@api_view(['POST']) #بوست لاني راح اضيف معلومات المستخدم في الداتابيس
def register(request):
    data = request.data #المعلومات اللي راح يدخلها المستخدم اخزنها في ذا المتغير
    user = SignUpSerializers(data = data) #يدخل الداتا هنا عشان يتأكد من الفالديشين

    if user.is_valid():#يعني اذا اليوزر دخل الداتا صح
        if not User.objects.filter(username=data['email']).exists():  #اتاكد انو اليوزر غير موجود مسبقا عن طريق انه يتاكد من الايميل
            user = User.objects.create( #في حال انو اليوزر ماكان موجود مسبقا راح انشيء اليوزر
                username = data['username'], #الداتا راح تجي على شكل ارراي عشان كذا اخذها بذي الصورة
                first_name = data['first_name'], 
                last_name = data['last_name'],
                email = data['email'],
                password = make_password(data['password'])  
            )
            return Response({'message':'Your account registered successfully!'}, status=status.HTTP_201_CREATED)
        
        else: #اذا كان اليوزر موجود
            return Response({'message':'This email already exists!!!'}, status=status.HTTP_400_BAD_REQUEST)
    
    else: #في حال انو اليوزر مادخل مزبوط
        return Response(user.errors) #يرجع الخلل اللي صار
    


#get user
@api_view(['GET']) 
@permission_classes([IsAuthenticated]) #هذا يعني لازم اليوزر يكون مسوي لوق ان ويكون اوثونتيكات
def current_user(request):
    user = UserSerializers(request.user,many=False) #عشان يرجع الداتا على شكل جيسون 
    return Response(user.data)




#Update usr
@api_view(['PUT']) 
@permission_classes([IsAuthenticated]) #هذا يعني لازم اليوزر يكون مسوي لوق ان ويكون اوثونتيكات
def update_user(request):
    user = request.user #الاي دي ينأخذ من التوكين و راح يترسل لما يسوي اليوزر لوق ان
    data = request.data  #لما يسوي لوق ان راح اخذ معلوماته اللي دخلها

    user.username =data['username']
    user.first_name =data['first_name']
    user.last_name =data['last_name']
    user.email =data['email']

    if data['password'] !="":  #يعني اذا اليوزر ارسل المعلومات ومن ضمنها حقل الباسوورد ماكان فاضي فمعناتها يبغى يعدل الباسوورد
        user.password = make_password(data['password'])
    
    user.save()

    serializers = UserSerializers(user,many=False) #عشان يرجع الداتا على شكل جيسون بعد ما تحدثت
    return Response (serializers.data)




#يولد الرابط حق اللي نسيت الرقم السري
def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}//{host}/".format(protocol=protocol, host=host) #كذا انشيء رابط اول شيء احط اتش تيبي وبعدين رابط الهوست



#forgot Password, send lin; to email
@api_view(['POST']) 
def forgotPassword(request):
    data = request.data  #ناخذ المعلومات اللي راح يدخلها اليوزر زي الايميل 
    user = get_object_or_404(User,email=data['email']) #يحاول يجيب اليوزر من الداتابيس من الايميل اللي دخله اليوزر
    token = get_random_string(40) #يولد نصوص عشوائية
    expire_date = datetime.now() + timedelta(minutes = 30)   #الرابط حق نسي الباسوورد مانبغاه يكون موود لفترة طويلة
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()
    host = get_current_host(request)
    link = "http://127.0.0.1:8000/api/reset_password/{token}".format(token=token) #عن طريق هذا الرابط يعدل الباسوورد ونعتمد على التوكين عشان نعرف مين هوا اليوزر
    body = "Your password reset link is: {link}".format(link=link) #عشان تنرسل في الايميل
    send_mail(
        "Password reset from eMarket",
        body,
        "eMarket@gmail.com",
        [data['email']] 
    )
    return Response({"message":"Password reset sent to {email}".format(email=data['email'])})





#reset Password
@api_view(['POST']) 
def resetPassword(request,token):
    data = request.data  #ناخذ المعلومات اللي راح يدخلها اليوزر زي الايميل 
    user = get_object_or_404(User,profile__reset_password_token = token) #التوكين اللي راح ينرسل حق اعادة الباسوورد
    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now(): #اذا مر فترة على الرابط اللي يعيد فيه الباسوورد
        return Response({'error':'Token is expired'}, status=status.HTTP_400_BAD_REQUEST)
    
    if data['password'] != data['confirmPassword']:
        return Response({'error':'Password are not same'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.profile.save()
    user.save()
    return Response({"message":"Password reset done"})
    













