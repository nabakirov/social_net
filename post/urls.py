from rest_framework.routers import DefaultRouter

from post import views


router = DefaultRouter()

router.register('v1/posts', views.PostViewSet, basename='posts')
router.register('v1/feed', views.FeedViewSet, basename='feed')

urlpatterns = router.urls
