from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user import serializers as s
from user.tasks import enrich_user_info


def get_login_response(user, request):
    refresh = RefreshToken.for_user(user)
    data = {
        "user": s.PrivateProfileSerializer(instance=user, context={'request': request}).data,
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }
    return data


class SignUpView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = s.SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        enrich_user_info.delay(serializer.instance.id)
        return Response(data=get_login_response(serializer.instance, request))


class LoginView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = s.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(data=get_login_response(user, request))
