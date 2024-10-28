from django.db.models import Count, Q, Prefetch

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins, response, status
from rest_framework.decorators import action


from post.models import Post, PostLike
from post.serializers import (
    PostSerializer,
    PostCreateSerializer,
    PostFeedListSerializer)
from post.tasks import post_like_sync
from socialnet.mixins import ActionSerializerClassMixin, FilterActiveMixin


class PostViewSet(ActionSerializerClassMixin,
                  FilterActiveMixin,
                  ModelViewSet):
    action_serializer_class = {
        'list': PostSerializer
    }

    serializer_class = PostCreateSerializer

    def get_queryset(self):
        return Post.objects \
            .select_related('author') \
            .annotate(_like_count=Count('liked_users__id'))

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(author_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class FeedViewSet(ActionSerializerClassMixin,
                  FilterActiveMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):

    serializer_class = PostFeedListSerializer

    def get_queryset(self):
        likes_qs = PostLike.objects.filter(user_id=self.request.user.id)
        return Post.objects \
            .select_related('author') \
            .prefetch_related(Prefetch('like_rel', likes_qs))  # to mark user's liked posts

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.filter(is_private=False)
        return queryset

    @action(methods=['POST'], detail=True)
    def like(self, *args, **kwargs):
        post = self.get_object()
        like_rel = list(post.like_rel.all())
        like_instance = like_rel[0] if like_rel else None
        if like_instance:
            like_instance.delete()
        else:
            PostLike.objects.create(post_id=post.id, user_id=self.request.user.id)
        # todo: make queue for syncing "like" count.
        #  For example make queue, where we will put post_id, to sync.
        #  Worker on celery will scheduled on every 5 minutes and sync "like" count on every post in queue
        post_like_sync.delay(post_id=post.id)
        return response.Response(status.HTTP_200_OK)

