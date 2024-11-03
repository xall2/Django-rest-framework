from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
#from posts.views import PostViewset
from rest_framework.routers import DefaultRouter


#router = DefaultRouter()
#router.register("", PostViewset, basename="posts")


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('product.urls')),

    path('api/', include('account.urls')),

    path('api/', include('order.urls')),

    path('api/token/', TokenObtainPairView.as_view()),

    path('api/posts/', include('posts.urls')),

    #path('api/posts/', include(router.urls)),
    
] 

#handler404 = 'utils.error_view.handler404' #يروح على مجلد يوتيل على ملف ايرور وياخذ الفنكشن هندلر ويطبقه على الراوت الكبير فالبتالي راح يطبق على كل التطبيقات