from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from .models import Post
from .serializers import PostsSerializers
from .permissions import ReadOnly, AuthorOrReadOnly
from rest_framework import viewsets



"""
#using viewset, A viewset is a type of view that allows handling requests for CRUD operations without having to explicitly define each function.*********************************************************************************************************************************************
@permission_classes([IsAuthenticatedOrReadOnly])
class PostViewset(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostsSerializers
"""
    
        


#by using generic model mixins, They allow you to create views that handle specific CRUD operations without having to rewrite the same logic for each view. This is particularly helpful when you don’t need a full ModelViewSet but only a subset of operations. ************************************************************************************
#By using them, you keep your code clean and focused on exactly what each view needs to do.
class PostListCreateView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
        a view for creating and listing posts
    """

    serializer_class = PostsSerializers
    permission_classes = [AuthorOrReadOnly]  #بس اذا كان اليوزر مسزي لوق ان او اذا مو مسوي لوق ان بس يقدر يسترجع بس ما يقدر يسوي اشياء ثانية زي الاضافة او الحذف او التعديل
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)


    #get all posts
    def get(self, request:Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)   #uses self.list() from the ListModelMixin, which returns a serialized list of all Post objects in the queryset.

    #add new post
    def post(self, request:Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)  #self.create() is a method provided by CreateModelMixin, which handles the creation logic, including data validation and saving the object to the database using the specified serializer.


class PostRetriveUpdateDeleteView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """
        a view Retrive, Update and Delete posts
    """

    serializer_class = PostsSerializers
    permission_classes = [AuthorOrReadOnly]
    queryset = Post.objects.all()

    

    #get post by id
    def get(self, request:Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)   #Use self.retrieve() within the get method to retrieve a single post by its ID.

    #update post
    def put(self, request:Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    

    #delete post
    def delete(self, request:Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)   #deletion single post by its ID

#********************************************************************************************************************************










"""
#by using generic APIView
class PostListCreateView(APIView):
    
        #a view for creating and listing posts
    

    serializre_class = PostsSerializers
    

    #get all posts
    def get(self, request:Request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = self.serializre_class(instance=posts, many=True)
        responce = {
            "message": "Posts Returned!!", 
            "data":serializer.data,
        }
        return Response(responce, status=status.HTTP_200_OK)
    

    #add new post to database
    def post(self, request:Request, *args, **kwargs):
        data = request.data    #اخذ الداتا اللي جاية من اليوزر
        serializer = self.serializre_class(data=data)
        if serializer.is_valid():
            serializer.save()
            responce = {
            "message": "Post Created!!", 
            "data":serializer.data,
            }
            return Response(responce, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetriveUpdateDeleteView(APIView):
    
        #a view for Retrive, Update and Delete posts
    

    serializer_class = PostsSerializers

    
    #Retrive post by id
    def get(self, request:Request, post_id:int):
        post = get_object_or_404(Post,pk=post_id)
        serializer = self.serializer_class(instance=post)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    #Update post
    def put(self, request:Request, post_id:int):
        post = get_object_or_404(Post,pk=post_id)
        data = request.data
        serializer = self.serializer_class(instance=post, data=data)  
        if serializer.is_valid():  #اذا الداتا اللي جاته فاليد راح يحدث الداتا ويحفظها
            serializer.save()
            responce = {
            "message": "Post Updated!!", 
            "data":serializer.data,
            }
            return Response(responce, status=status.HTTP_200_OK)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request:Request, post_id:int):
        post = get_object_or_404(Post,pk=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
