from typing import Any
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView


#نسمح بس بالقراءة ومانسمح بالكتابة
class ReadOnly(BasePermission):  
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.method in SAFE_METHODS     #راح يرجع ترو اذا كان قيت ويرجع فولس اذا كان بوست وبما انه ريد اونلي فماراح يسمح بالبوست



#نسمح بس اليوزر يسوي عمليات على البوست حقه واليوزرز الثانيين بس يقرأوا بدون مايسووا شيء
class AuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        if request.method in SAFE_METHODS:    #اول شيء يشيك اذا الريكوست كان قيت علطول يرجع ترو 
            return True
        
        return request.user == obj.author   #لكن اذا الريكوست كان ابديت,ديليت,بوست ذيك الساعة لازم يشيك اذا اليوزر اللي سوا الريكوست هوا نفسه المالك لهذا البوست