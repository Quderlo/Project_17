from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from api_v0.serializers import CameraSerializer, CameraAuthSerializer
from recognition.models import Camera, CameraAuth


class CameraViewSet(viewsets.ModelViewSet):
    serializer_class = CameraSerializer
    queryset = Camera.objects.all()
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CameraAuthViewSet(viewsets.ModelViewSet):
    serializer_class = CameraAuthSerializer
    queryset = CameraAuth.objects.all()
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePeopleViewSet(viewsets.ViewSet):
    serializer_class =
    queryset = None
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    permission_classes = [permissions.AllowAny]