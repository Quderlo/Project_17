from rest_framework import serializers, viewsets

from cv_dlib_models.face_encoder import FaceEncoder
from people.models import Person, PersonSighting
from recognition.models import Camera, CameraAuth
from api_v0.validators import validate_camera, validate_people_add, validate_rtsp_links


class CameraSerializer(serializers.ModelSerializer):
    auth_details = serializers.SerializerMethodField()
    rtsp_link = serializers.SerializerMethodField()

    class Meta:
        model = Camera
        fields = [
            "ip_address",
            "port",
            "name",
            "rtsp_path",
            "auth",
            "auth_details",
            "rtsp_link",
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

    def get_auth_details(self, obj):
        if obj.auth:
            return {
                "username": obj.auth.username,
                "password": obj.auth.password,
            }
        return None

    def get_rtsp_link(self, obj):
        """
        Возвращает RTSP-ссылку камеры. Если RTSP-ссылка не задана,
        она генерируется автоматически с использованием метода модели.
        """
        return obj.generate_rtsp_link()

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
    photo = serializers.CharField(
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

    def create(self, validated_data):
        cropped_face = validated_data.pop('photo', None)

        face_encoding = None
        if cropped_face is not None:
            try:
                encoder = FaceEncoder()
                face_encoding = encoder.get_face_encoding(cropped_face)
            except Exception as e:
                raise serializers.ValidationError({'photo': [f"{e}"]})

        if face_encoding is None:
            raise serializers.ValidationError({'photo': f'Ошибка сервера. Кодирование не удалось'})

        person = Person.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data.get('middle_name', None),
            face_encoding=face_encoding,
        )

        return person


class PersonSightingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели PersonSighting
    """

    person = serializers.PrimaryKeyRelatedField(
        queryset=Person.objects.all(),
        error_messages={
            "required": "Пожалуйста, укажите человека.",
            "does_not_exist": "Указанный человек не найден.",
            "invalid": "Некорректное значение для поля человека.",
        }
    )

    class Meta:
        model = PersonSighting
        fields = ['person']

    def validate(self, data):
        return data


class CameraRegisterSerializer(serializers.ModelSerializer):
    rtsp_link = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    links = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True,
        error_messages={'blank': 'Список ссылок не может быть пустым.'}
    )

    class Meta:
        model = Camera
        fields = [
            "is_active",
            "rtsp_link",
            "links",
        ]
        extra_kwargs = {
            'is_active': {
                'error_messages': {
                    'required': 'Необходимо указать статус активности камеры.',
                    'blank': 'Статус активности камеры не может быть пустым.',
                }
            }
        }

    def get_rtsp_link(self, obj):
        return obj.generate_rtsp_link()

    def validate(self, data):
        validate_rtsp_links(data)
        return data
