from django.urls import path
from django.views.generic import TemplateView

from .views import CameraListView, CameraAuthListView, CameraDetailView, CameraAuthDetailView

urlpatterns = [
    # Пути для камер
    path('camera-list/', CameraListView.as_view(), name='camera-list'),
    path('camera-detail/<int:pk>/', CameraDetailView.as_view(), name='camera-detail'),

    # Пути для авторизаций
    # path('camera-auth-list/', CameraAuthListView.as_view(), name='camera-auth-list'),
    # path('camera-auth-detail/<int:pk>/', CameraAuthDetailView.as_view(), name='camera-auth-detail'),

    path('', TemplateView.as_view(template_name='recognition/index.html'), name='index'),

]
