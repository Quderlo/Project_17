from rest_framework import serializers
from recognition.models import Camera, CameraAuth
from api_v0.validators import validate_camera


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = [
            "ip_address",
            "port",
            "name",
            "rtsp_path",
            "auth",
        ]
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "required": "Пожалуйста, введите название для камеры.",
                    "blank": "Пожалуйста, введите название для камеры.",
                },
            },
            "ip_address": {
                "error_messages": {
                    "required": "Пожалуйста, введите IP адрес для камеры.",
                    "blank": "Пожалуйста, введите IP адрес для камеры.",
                    "invalid": "Неверный IP-адрес, или камера не доступна.",
                },
            },

            "port": {
                "error_messages": {
                    "invalid": "Порт неверный или содержит, не только числа.",
                },
            },

            "rtsp_path": {
                "error_messages": {
                    "invalid": "По данному пути не обнаружен RTSP поток."
                }
            }
        }

    def validate(self, data):
        validate_camera(data)
        return data


class CameraAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraAuth
        fields = [
            'name',
            'username',
            'password',
        ]
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "required": "Пожалуйста, введите название.",
                    "blank": "Пожалуйста, введите название.",
                },
            },
            "username": {
                "error_messages": {
                    "required": "Пожалуйста, введите имя пользователя для авторизации.",
                    "blank": "Пожалуйста, введите имя пользователя для авторизации.",
                },
            },

            "password": {
                "error_messages": {
                    "required": "Пожалуйста, введите имя пароль для авторизации.",
                    "blank": "Пожалуйста, введите имя пароль для авторизации.",
                },
            },
        }

