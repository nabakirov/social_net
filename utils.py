from django.conf import settings

from abstract.core import AbstractAPI


def get_abstract_api() -> AbstractAPI:
    email_api_key = getattr(settings, 'ABSTRACT_EMAIL_API_KEY', None)
    ip_api_key = getattr(settings, 'ABSTRACT_IP_API_KEY', None)
    holiday_api_key = getattr(settings, 'ABSTRACT_HOLIDAY_API_KEY', None)
    return AbstractAPI(email_api_key=email_api_key,
                       ip_api_key=ip_api_key,
                       holiday_api_key=holiday_api_key)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
