from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination


class MaxLimitOffsetPagination(LimitOffsetPagination):
    rest_framework_settings = getattr(settings, "REST_FRAMEWORK", {})
    max_page_size = rest_framework_settings.get("MAX_PAGE_SIZE", 1000)
    max_limit = max_page_size
