import time
from logging import getLogger

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

from abstract.exceptions import AbstractBaseException
from utils import get_abstract_api


logger = getLogger()


class UserManager(BaseUserManager):
    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.save()
        return user

    def create_user(self, *, email, password, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def get_by_natural_key(self, login):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: login})


class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    objects = UserManager()

    create_date = models.DateTimeField(_('create date'), null=False, auto_now_add=True)
    email = models.EmailField(_('email'), unique=True, blank=False, null=False)
    password = models.CharField(_('password'), max_length=128, null=False, blank=False)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    original_ip = models.GenericIPAddressField(_('original ip'), null=True)
    is_active = models.BooleanField(_('is active'), default=True)
    is_superuser = models.BooleanField(_('is superuser'), default=False)

    def __str__(self):
        return f'{self.email}'

    def enrich_info(self):
        if not self.original_ip:
            return
        api = get_abstract_api()
        location = api.ip_info(ip=str(self.original_ip))
        extra_location = location.model_dump()

        # on a free plan, we are receiving 429 status code
        time.sleep(2)
        if location.country_code:
            holiday = api.holiday_info(
                country_code=location.country_code,
                year=self.create_date.year,
                month=self.create_date.month,
                day=self.create_date.day
            )
            extra_holiday = [item.model_dump() for item in holiday]
        else:
            extra_holiday = []
        if hasattr(self, 'extra_info'):
            self.extra_info.country_code = location.country_code
            self.extra_info.location = extra_location
            self.extra_info.holiday = extra_holiday
            self.extra_info.save()
        else:
            UserInfo.objects.create(user_id=self.id, country_code=location.country_code,
                                    location=extra_location, holiday=extra_holiday)


class UserInfo(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, null=False, related_name='extra_info')
    country_code = models.CharField(_('country code'), null=True, max_length=10)
    location = models.JSONField(_('location'), null=True)
    holiday = models.JSONField(_('holiday'), null=True)
