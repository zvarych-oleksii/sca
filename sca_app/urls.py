from rest_framework.routers import DefaultRouter
from .views import SpyCatViewSet, MissionViewSet

router = DefaultRouter()
router.register('cats', SpyCatViewSet, basename='spycat')
router.register('missions', MissionViewSet, basename='mission')

urlpatterns = router.urls
