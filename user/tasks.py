from celery import shared_task

from user.models import User


@shared_task
def enrich_user_info(user_id):
    user = User.objects.get(id=user_id)
    user.enrich_info()