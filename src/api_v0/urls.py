from rest_framework.routers import DefaultRouter

from api_v0.views import CameraViewSet, CameraAuthViewSet, PersonAddViewSet

router = DefaultRouter()

router.register(r'camera-add', CameraViewSet, basename='camera-add')
router.register(r'camera-auth-add', CameraAuthViewSet, basename='camera-auth-add')
router.register(r'people-add', PersonAddViewSet, basename='people-add')

urlpatterns = [

]

urlpatterns += router.urls
