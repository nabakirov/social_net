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


class Unique(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'unique'
    default_detail = _('Must be unique.')


class TryLater(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'try_later'
    default_detail = _('Try later.')


class Invalid(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'invalid'
    default_detail = _('Invalid.')
