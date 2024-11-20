from django.urls import path
from django.views.generic import TemplateView

from .views import CameraListView, CameraAuthListView, CameraDetailView, CameraAuthDetailView, CameraCreateView

urlpatterns = [
    # Пути для камер
    path('camera-list/', CameraListView.as_view(), name='camera-list'),
    path('camera-active-list/', CameraListView.as_view(), name='camera-active-list'),
    path('camera-inactive-list/', CameraListView.as_view(), name='camera-inactive-list'),
    path('camera-detail/<int:pk>/', CameraDetailView.as_view(), name='camera-detail'),
    path('camera-create/', CameraCreateView.as_view(), name='camera-create'),

    # Пути для авторизаций
    # path('camera-auth-list/', CameraAuthListView.as_view(), name='camera-auth-list'),
    # path('camera-auth-detail/<int:pk>/', CameraAuthDetailView.as_view(), name='camera-auth-detail'),

    path('', TemplateView.as_view(template_name='recognition/camera/index.html'), name='index'),

]
