from rest_framework import status, viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.permission import IsOwnerOrReadOnly
from api.serializers import CommentSerializer, PostSerializer
from posts.models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        post = get_object_or_404(self.queryset, pk=kwargs.get('pk'))
        self.check_object_permissions(request, post)
        serializer = self.get_serializer(post,
                                         data=request.data,
                                         partial=kwargs['partial']
                                         )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        post = get_object_or_404(self.queryset, pk=kwargs.get('pk'))
        self.check_object_permissions(request, post)
        self.perform_destroy(post)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = None
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        self.queryset = post.comments.all()
        return self.queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        comment = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
        self.check_object_permissions(request, comment)
        serializer = self.get_serializer(comment,
                                         data=request.data,
                                         partial=kwargs['partial']
                                         )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        comment = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
        self.check_object_permissions(request, comment)
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)
