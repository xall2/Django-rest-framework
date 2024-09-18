from rest_framework import serializers
from django.contrib.auth.models import User



class SignUpSerializers(serializers.ModelSerializer):
    #من خلال هذا الكلاس اقول ايش الداتا المسموح انها تؤخذ من الدتابيس
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password') #اذا بختار خانات معينة عشان يرجعها على شكل جيسون
        
        #هنا احط معلومات عن الحقول مثلا اذا ريكوايرد وكذا
        extra_kwargs = {
            'username': {'required':True, 'allow_blank':False},
            'first_name': {'required':True, 'allow_blank':False}, 
            'last_name': {'required':True, 'allow_blank':False}, 
            'email': {'required':True, 'allow_blank':False}, 
            'password': {'required':True, 'allow_blank':False, 'min_length':8},
        }


class UserSerializers(serializers.ModelSerializer):
    #من خلال هذا الكلاس اقول ايش الداتا المسموح انها تؤخذ من الدتابيس
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email') #ماحطيت الباسوورد عشان لا يرجعها
        
        