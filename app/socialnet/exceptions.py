from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException
from rest_framework import status


class AlreadyExist(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'exist'
    default_detail = _('Already exist.')


class DoesNotExist(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'does_not_exist'
    default_detail = _('Does not exist.')