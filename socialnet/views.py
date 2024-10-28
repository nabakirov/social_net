from logging import getLogger

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.conf import settings as django_settings

from rest_framework.views import set_rollback
from rest_framework.response import Response
from rest_framework import exceptions, settings, status


logger = getLogger()


def exception_handler(exc, context):
    response = normalize_exception(exc, context)
    return response


_non_field_error_key = settings.api_settings.NON_FIELD_ERRORS_KEY


def normalize_exception(exc, context):
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, dict):
            data = exc.get_full_details()
        else:
            d = exc.get_full_details()
            if not isinstance(d, list):
                d = [d]
            data = {_non_field_error_key: d}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)
    else:
        if django_settings.DEBUG:
            raise exc
        logger.exception(str(exc), exc_info=exc)
        return Response(data={'status': 500},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
