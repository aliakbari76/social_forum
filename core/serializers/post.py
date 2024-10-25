from rest_framework import serializers
from core.models.post import Post


class PostResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'score', 'score_count', 'created_at', 'updated_at', 'author_user')


class CreatePostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()


class PostListSerializer(serializers.ModelSerializer):
    user_vote = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'score', 'score_count', 'user_vote']
