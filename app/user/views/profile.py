from rest_framework import mixins, viewsets

from user.serializers import PrivateProfileSerializer


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = PrivateProfileSerializer

    def get_object(self):
        return self.request.user
