from django.urls import path
from . import views




urlpatterns = [
    path('getAllPosts/', views.getAllPosts, name= 'getAllPosts'),
    path('addNewPost/', views.addNewPost, name='addNewPost'),

]