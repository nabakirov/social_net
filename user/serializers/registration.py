from logging import getLogger

from rest_framework import serializers as s

from abstract.exceptions import AbstractBaseException
from user import models as m, exceptions as exc
from utils import get_abstract_api, get_client_ip


logger = getLogger()


class PasswordField(s.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})

        kwargs['style']['input_type'] = 'password'
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)


class SignUpSerializer(s.ModelSerializer):
    class Meta:
        model = m.User
        fields = ('id', 'email', 'first_name', 'last_name', 'create_date', 'password')
        read_only_fields = ('create_date',)

    def validate_email(self, email):
        if m.User.objects.filter(email__iexact=email).exists():
            raise exc.Unique()
        api = get_abstract_api()
        try:
            email_validator = api.email_info(email=email)
        except AbstractBaseException as e:
            logger.exception(str(e), exc_info=True)
            raise exc.TryLater()
        if email_validator.deliverability != 'DELIVERABLE':
            raise exc.Invalid()
        return email

    password = PasswordField(required=True)

    def create(self, validated_data):
        return m.User.objects.create_user(
            **validated_data, original_ip=get_client_ip(self.context['request']))


class LoginSerializer(s.Serializer):
    email = s.EmailField(required=True, allow_null=False)
    password = PasswordField(required=True)

    def validate(self, attrs):
        user = m.User.objects.get_by_natural_key(attrs['email'])

        if not user:
            raise s.ValidationError({'email': [exc.DoesNotExist().detail]})
        if not user.check_password(attrs['password']):
            raise s.ValidationError({'password': [s.ValidationError().detail]})
        if not user.is_active:
            raise s.ValidationError()
        attrs['user'] = user
        return attrs
