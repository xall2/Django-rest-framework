from django.urls import path
from . import views




urlpatterns = [
    path('orders/new/', views.new_order, name= 'new_order'),

    path('orders/', views.getAllOrder, name= 'getAllOrder'),

    path('orders/<str:pk>/', views.getOrderById, name= 'getOrderById'),

    path('orders/<str:pk>/process', views.updateOrder, name= 'updateOrder'),

    path('orders/<str:pk>/delete', views.deleteOrder, name= 'deleteOrder'),
    
    ]