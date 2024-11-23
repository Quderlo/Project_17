from google.protobuf.proto import serialize
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from api_v0.serializers import CameraSerializer, CameraAuthSerializer, PersonAddSerializer, PersonSightingSerializer, \
    CameraRegisterSerializer
from people.models import Person, PersonSighting
from recognition.models import Camera, CameraAuth


class CameraViewSet(viewsets.ModelViewSet):
    serializer_class = CameraSerializer
    queryset = Camera.objects.all()
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'camera': 'Камера подключена успешно.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CameraAuthViewSet(viewsets.ModelViewSet):
    serializer_class = CameraAuthSerializer
    queryset = CameraAuth.objects.all()
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonAddSerializer
    queryset = Person.objects.all()
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'person': 'Данные подключены к отслеживанию.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonSightingViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSightingSerializer
    queryset = PersonSighting.objects.none()
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



class CameraRegisteredViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraRegisterSerializer
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Сохраняем данные камеры
            camera = serializer.save()

            # Устанавливаем is_active в True
            camera.is_active = True

            # Генерируем RTSP-ссылку, если она отсутствует
            if not camera.rtsp_link:
                camera.rtsp_link = camera.generate_rtsp_link()

            # Сохраняем изменения в камере
            camera.save()

            # Возвращаем успешный ответ с данными камеры
            return Response(
                {
                    "message": "Камера успешно зарегистрирована.",
                    "camera": {
                        "ip_address": camera.ip_address,
                        "port": camera.port,
                        "name": camera.name,
                        "rtsp_path": camera.rtsp_path,
                        "rtsp_link": camera.rtsp_link,
                        "is_active": camera.is_active,
                    },
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

