from rest_framework import serializers as s

from post.models import Post
from user.serializers import PublicProfileSerializer


class PostSerializer(s.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'create_date', 'author', 'title',
                  'description', 'is_private', 'like_count')

    author = PublicProfileSerializer(read_only=True)
    like_count = s.IntegerField(source='_like_count')


class PostCreateSerializer(s.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'create_date', 'title', 'description', 'is_private')
        read_only_fields = ('id', 'create_date')


class PostFeedListSerializer(s.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'create_date', 'author', 'title',
                  'description', 'like_count', 'liked')

    author = PublicProfileSerializer(read_only=True)

    liked = s.SerializerMethodField(read_only=True)

    def to_representation(self, instance):
        # limiting description to 100 symbols
        data = super().to_representation(instance)
        data['description'] = data['description'][:97] + '...' \
            if (data['description'] and len(data['description']) > 100) else data['description']
        data['like_count'] = data['like_count'] if data['like_count'] is not None else 0
        return data

    def get_liked(self, obj) -> bool:
        return obj.like_rel.exists()
