from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from recognition.models import Camera, CameraAuth

# Представления для Camera
class CameraListView(ListView):
    model = Camera
    context_object_name = "cameras"

class CameraDetailView(DetailView):
    model = Camera

class CameraCreateView(CreateView):
    model = Camera
    fields = ['name', 'ip_address', 'port']

# Представления для CameraAuth
class CameraAuthListView(ListView):
    model = CameraAuth

class CameraAuthDetailView(DetailView):
    model = CameraAuth

class CameraAuthCreateView(CreateView):
    model = CameraAuth
    fields = ['name', 'username', 'password']



