from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import User, Post, Comment
from posts.serializers import UserSerializer, PostSerializer
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
        post = self.serializer_class(data=request.data)
        if post.is_valid():
            post.save(author=user)
            return Response(post.data, status=201)
        return Response(post.data, status=400)
