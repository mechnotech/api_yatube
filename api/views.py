from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from api.serializers import CommentSerializer, PostSerializer
from posts.models import Comment, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.auth).user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        post = self.queryset.filter(pk=kwargs['pk']).first()
        if not post:
            request.error = {'error': 'Такой записи не существует!'}
            return Response(request.error, status=status.HTTP_404_NOT_FOUND)

        user = Token.objects.get(key=request.auth).user
        if user != post.author:
            request.error = {'error': 'Можно изменять только свой пост!'}
            return Response(request.error, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(post,
                                         data=request.data,
                                         partial=kwargs['partial']
                                         )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        post = self.queryset.filter(pk=kwargs['pk']).first()
        if not post:
            request.error = {'error': 'Такой записи не существует!'}
            return Response(request.error, status=status.HTTP_404_NOT_FOUND)

        user = Token.objects.get(key=request.auth).user
        if user != post.author:
            request.error = {'error': 'Можно удалить только свой пост!'}
            return Response(request.error, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(post)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        comments = self.queryset.filter(post=kwargs['post_id'])
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user = Token.objects.get(key=request.auth).user
        post = Post.objects.filter(pk=kwargs['post_id']).first()
        if not post:
            request.error = {'error': 'Такой записи не существует!'}
            return Response(request.error, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):

        comment = Comment.objects.filter(pk=kwargs['pk']).first()
        if not comment:
            request.error = {'error': 'Такой записи не существует!'}
            return Response(request.error, status=status.HTTP_404_NOT_FOUND)

        user = Token.objects.get(key=request.auth).user
        if user != comment.author:
            request.error = {'error': 'Можно изменять'
                                      ' только свой комментарий!'
                             }
            return Response(request.error, status=status.HTTP_403_FORBIDDEN)

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
            request.error = {'error': 'Такой записи не существует!'}
            return Response(request.error, status=status.HTTP_404_NOT_FOUND)

        user = Token.objects.get(key=request.auth).user
        if user != comment.author:
            request.error = {'error': 'Можно удалить только свой пост!'}
            return Response(request.error, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)
