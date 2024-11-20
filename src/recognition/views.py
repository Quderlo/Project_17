from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from recognition.models import Camera, CameraAuth

# Представления для Camera
class CameraListView(ListView):
    model = Camera
    context_object_name = "cameras"
    template_name = "recognition/camera/camera_list.html"

class CameraDetailView(DetailView):
    model = Camera
    template_name = "recognition/camera/camera_detail.html"

class CameraCreateView(View):
    def get(self, request):
        camera_names = CameraAuth.objects.values('id', 'name')
        return render(
            request,
            'recognition/camera/camera_create.html',
            {'camera_names': camera_names}
        )





# Представления для CameraAuth
class CameraAuthListView(ListView):
    model = CameraAuth
    template_name = "recognition/camera/camera_auth_list.html"

class CameraAuthDetailView(DetailView):
    model = CameraAuth
    template_name = "recognition/camera/camera_detail.html"

class CameraAuthCreateView(CreateView):
    model = CameraAuth
    fields = ['name', 'username', 'password']
    template_name = "recognition/camera/camera_auth_create.html"



