from django.urls import path
from . import views


urlpatterns = [

    #by using generic APIView and model mixins
    path("", views.PostListCreateView.as_view(), name= "listCreatPosts"),
    path("<int:pk>/", views.PostRetriveUpdateDeleteView.as_view(), name='RetriveUpdateDeletePost'),


]