from rest_framework import serializers as s

from user import models as m


class PrivateProfileSerializer(s.ModelSerializer):
    class Meta:
        model = m.User
        fields = ('id', 'create_date', 'email', 'first_name', 'last_name')
        read_only_fields = ('id', 'create_date', 'email')


class PublicProfileSerializer(s.ModelSerializer):
    class Meta:
        model = m.User
        fields = ('id', 'first_name', 'last_name')
