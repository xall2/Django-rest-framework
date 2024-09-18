from django.urls import path
from . import views




urlpatterns = [
    path('register/', views.register, name= 'register'),

    path('userInfo/', views.current_user, name= 'userInfo'),

    path('updateUser/', views.update_user, name= 'updateUser'),

    path('forgotPassword/', views.forgotPassword, name= 'forgotPassword'),

    path('reset_password/<str:token>', views.resetPassword, name= 'resetPassword'),

]