from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import User, Post, Comment
from api.serializers import UserSerializer, PostSerializer, CommentSerializer
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
        if not post:
            return Response(request.data, status=404)
        user = Token.objects.get(key=request.auth).user
        if user != post.author:
            return Response(request.data, status=403)
        serializer = self.get_serializer(post,
                                         data=request.data,
                                         partial=kwargs['partial']
                                         )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        post = self.queryset.get(pk=kwargs['pk'])
        if not post:
            return Response(request.data, status=404)
        user = Token.objects.get(key=request.auth).user
        if user != post.author:
            return Response(request.data, status=403)
        self.perform_destroy(post)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(methods=['get', 'post'], detail=True)
    # def comments(self, request, *args, **kwargs):
    #     post = self.queryset.get(pk=kwargs['pk'])
    #
    #     if not post:
    #         return Response(request.data, status=400)
    #
    #     comments = Comment.objects.all() #filter(post=post)
    #     serializer = CommentSerializer(comments)
    #     return Response(serializer.data, status=200)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):

        comments = self.queryset.filter(post=kwargs['post_id'])
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)

    def create(self, request, *args, **kwargs):

        user = Token.objects.get(key=request.auth).user
        if user != request.user:
            return Response(request.data, status=403)
        post = Post.objects.get(pk=kwargs['post_id'])
        if not post:
            return Response(request.data, status=404)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user, post=post)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=kwargs['pk'])
        if not comment:
            return Response(request.data, status=404)
        user = Token.objects.get(key=request.auth).user
        if user != comment.author:
            return Response(request.data, status=403)
        serializer = self.get_serializer(comment,
                                         data=request.data,
                                         partial=kwargs['partial']
                                         )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        comment = self.queryset.get(pk=kwargs['pk'])
        if not comment:
            return Response(request.data, status=404)
        user = Token.objects.get(key=request.auth).user
        if user != comment.author:
            return Response(request.data, status=403)
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)
