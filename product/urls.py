from django.urls import path
from . import views




urlpatterns = [
    path('products/', views.getAllProducts, name= 'products'),

    path('products/<str:pk>/', views.getByIdProduct, name= 'getByID'), #يرجع الداتا على حسب الاي دي

    path('productFilter/', views.filterProduct, name= 'filter'),

    path('pagination/', views.pagination, name= 'pagination'),

    path('addNewProduct/', views.addNewProduct, name= 'addNewProduct'),

    path('updateProduct/<str:pk>/', views.updateProduct, name= 'updateProduct'),

    path('deleteProduct/<str:pk>/', views.deleteProduct, name= 'deleteProduct'),

    path('<str:pk>/addReview/', views.addReview, name= 'addReview'),

    path('<str:pk>/deleteReview/', views.deleteReview, name= 'deleteReview'),
]