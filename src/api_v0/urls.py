from rest_framework.routers import DefaultRouter

from api_v0.views import CameraViewSet, CameraAuthViewSet, PersonViewSet, PersonSightingViewSet, CameraRegisteredViewSet

router = DefaultRouter()

router.register(r'camera', CameraViewSet, basename='camera-api')
router.register(r'camera-auth', CameraAuthViewSet, basename='camera-auth-api')
router.register(r'people', PersonViewSet, basename='people-api')
router.register(r'person-sighting', PersonSightingViewSet, basename='person-sighting-api')
router.register(r'camera-register', CameraRegisteredViewSet, basename='camera-register-api')

urlpatterns = [

]

urlpatterns += router.urls
