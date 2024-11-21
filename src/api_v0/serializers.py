from cmath import phase

from rest_framework import serializers

from people.models import Person
from recognition.models import Camera, CameraAuth
from api_v0.validators import validate_camera, validate_people_add


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


class PersonAddSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(
        required=True,
        write_only=True,
        error_messages={
            "required": "Пожалуйста, загрузите фотографию.",
            "blank": "Фотография не может быть пустой.",
        },
    )


    class Meta:
        model = Person
        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'photo',
        ]

        extra_kwargs = {
            "first_name": {
                "error_messages": {
                    "required": "Пожалуйста, введите имя.",
                    "blank": "Имя не может быть пустым.",
                },
            },
            "last_name": {
                "error_messages": {
                    "required": "Пожалуйста, введите фамилию.",
                    "blank": "Фамилия не может быть пустой.",
                },
            },
            "photo": {
                "error_messages": {
                    "required": "Пожалуйста, загрузите фотографию.",
                    "blank": "Фотография не может быть пустой.",
                },
            },
        }

        def validate(self, data):
            validate_people_add(data)
            return data

