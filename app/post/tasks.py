from celery import shared_task

from post.models import Post


@shared_task
def post_like_sync(post_id):
    post = Post.objects.get(id=post_id)
    post.sync_likes()
