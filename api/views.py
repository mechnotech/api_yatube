from rest_framework import viewsets, status
from rest_framework.response import Response

from posts.models import User, Post
from api.serializers import UserSerializer, PostSerializer
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.auth).user
        if user != request.user:
            return Response(request.data, status=403)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        post = self.queryset.get(pk=kwargs['pk'])
        user = Token.objects.get(key=request.auth).user
        if user != post.author:
            return Response(request.data, status=403)
        serializer = self.get_serializer(post,
                                         data=request.data,
                                         partial=True
                                         )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        post = self.queryset.get(pk=kwargs['pk'])
        user = Token.objects.get(key=request.auth).user
        if user != post.author:
            return Response(request.data, status=403)
        self.perform_destroy(post)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
