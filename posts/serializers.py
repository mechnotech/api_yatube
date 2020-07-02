from rest_framework import serializers

from .models import Post, User, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'author', 'post')


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'pub_date')
        read_only_fields = ['author']
        serializer_related_field = ['author']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['author'] = instance.author.username
        return ret
