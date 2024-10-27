from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Post
from .serializers import PostsSerializers




#add post to database
@api_view(['POST'])
def addNewPost(request):
    data = request.data    #اخذ الداتا اللي جاية من اليوزر
    serializers = PostsSerializers(data=data)
    if serializers.is_valid():
        post = Post.objects.create(**data)
        serializers_data = PostsSerializers(post, many=False)
        responce = {
        "message": "Post Created!!", 
        "data":serializers_data.data,
        }
        return Response(responce, status=status.HTTP_200_OK)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)





#get all posts
@api_view(['GET'])
def getAllPosts(request):
    posts = Post.objects.all()
    serializer = PostsSerializers(instance=posts, many=True)
    responce = {
        "message": "Posts Returned!!", 
        "data":serializer.data,
    }
    return Response(responce, status=status.HTTP_200_OK)
