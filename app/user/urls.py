from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from user import views


router = DefaultRouter()

# router.register('v1/profile', views.ProfileViewSet, 'profile')


urlpatterns = [
    path('v1/login/', views.LoginView.as_view(), name='login'),
    path('v1/signup/', views.SignUpView.as_view(), name='signup'),
    path('v1/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/verify/', jwt_views.token_verify, name='refresh'),
    path('v1/profile/', views.ProfileViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
    }), name='profile'),
] + router.urls
