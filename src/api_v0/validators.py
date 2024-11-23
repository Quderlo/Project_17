import cv2
import dlib
import numpy as np
import requests
from rest_framework import serializers
from recognition.models import Camera
import base64


def validate_ip_address(data):
    ip_address = data.get("ip_address")
    url = f"http://{ip_address}"

    if Camera.objects.filter(ip_address=ip_address).exists():
        raise serializers.ValidationError(
            {"ip_address":
                 f"Адрес {ip_address} уже зарегистрирован.",
             }
        )

    try:
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            raise serializers.ValidationError(
                {"ip_address":
                     f"Не удалось подключиться к IP-адресу {ip_address}. Статус: {response.status_code}",
                }
            )

    except requests.RequestException as e:
        raise serializers.ValidationError(f"Ошибка при подключении к IP-адресу {ip_address}: {str(e)}")


def validate_rtsp(data):
    ip_address = data.get("ip_address")
    rtsp_path = data.get("rtsp_path")
    port = data.get("port")
    auth = data.get("auth")

    if not port:
        port = 554

    if auth:
        rtsp_link = f"rtsp://{auth.username}:{auth.password}@{ip_address}:{port}{rtsp_path}"
    else:
        rtsp_link = f"rtsp://{ip_address}:{port}{rtsp_path}"

    # Проверка доступности RTSP-ссылки
    try:
        cap = cv2.VideoCapture(rtsp_link)
        if not cap.isOpened():
            raise serializers.ValidationError({'rtsp_path':f"Не удалось подключиться к RTSP-ссылке {rtsp_path}."})
        cap.release()  # Закрыть подключение к камере
    except cv2.error as e:
        raise serializers.ValidationError({'rtsp_path':f"Ошибка при подключении к RTSP-ссылке {rtsp_path}: {str(e)}"})




def validate_camera(data):
    validate_ip_address(data)
    validate_rtsp(data)

    return data


def custom_validate_first_name(data):
    first_name = data.get("first_name")
    if not first_name.isalpha():
        raise serializers.ValidationError({'first_name': "Имя должно содержать только буквы."})

def custom_validate_last_name(data):
    last_name = data.get("last_name")
    if not last_name.isalpha():
        raise serializers.ValidationError({'last_name': "Фамилия должна содержать только буквы."})

def custom_validate_middle_name(data):
    middle_name = data.get("middle_name")
    if middle_name and not middle_name.isalpha():
        raise serializers.ValidationError({'middle_name': "Отчество должно содержать только буквы."})

def validate_photo(data):
    photo_base64 = data.get("photo")
    if not photo_base64:
        raise serializers.ValidationError({'photo': "Фото обязательно для загрузки."})

    # Декодируем строку base64 в изображение
    try:
        # Убираем префикс data:image/jpeg;base64, если он есть
        if photo_base64.startswith('data:image/jpeg;base64,'):
            photo_base64 = photo_base64.split('data:image/jpeg;base64,')[1]

        # Декодируем base64 в байты
        img_data = base64.b64decode(photo_base64)
        nparr = np.frombuffer(img_data, np.uint8)

        # Декодируем в изображение
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except Exception as e:
        raise serializers.ValidationError({'photo': f"Ошибка при декодировании изображения: {e}"})

    if img is None:
        raise serializers.ValidationError({'photo': "Неверный формат изображения."})

    # Преобразование в оттенки серого
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    detector = dlib.get_frontal_face_detector()
    # Обнаружение лиц
    faces = detector(gray)

    # Проверка на наличие лиц
    if len(faces) == 0:
        raise serializers.ValidationError({'photo': "На изображении не обнаружено лиц."})

    if len(faces) > 1:
        raise serializers.ValidationError({'photo': 'На фото больше одного человека.'})

    face = faces[0]
    x, y, w, h = face.left(), face.top(), face.width(), face.height()
    cropped_face = img[y:y+h, x:x+w]
    data['photo'] = cropped_face

    return data



def validate_people_add(data):
    custom_validate_first_name(data)
    custom_validate_last_name(data)
    custom_validate_middle_name(data)
    validate_photo(data)


def validate_rtsp_link(data, instance=None):
    """
    Функция для валидации RTSP-ссылки.
    Если ссылка пустая, она будет автоматически сгенерирована.
    """
    rtsp_link = data.get('rtsp_link')

    if not rtsp_link:
        # Если rtsp_link не передан, генерируем его
        if instance:  # Если это уже существующая камера, используем её метод
            return instance.generate_rtsp_link()
        else:
            raise serializers.ValidationError({'rtsp_link': 'Необходимо указать RTSP-ссылку.'})

    # Проверка на корректность RTSP-ссылки
    if not rtsp_link.startswith('rtsp://'):
        raise serializers.ValidationError({'rtsp_link': 'RTSP-ссылка должна начинаться с rtsp://'})

    return rtsp_link
