import cv2
import numpy as np
import requests
from rest_framework import serializers
from PIL import Image
from recognition.models import Camera


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
    photo = data.get("photo")
    if not photo:
        raise serializers.ValidationError({'photo': "Фото обязательно для загрузки."})

    try:
        # Конвертация фото из файла в массив OpenCV
        image = Image.open(photo).convert('RGB')  # Открываем и конвертируем в RGB
        image_np = np.array(image)  # Преобразуем в массив
        gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)  # Переводим в оттенки серого

        # Загрузка классификатора Haar Cascade
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(cascade_path)

        if face_cascade.empty():
            raise serializers.ValidationError({
                'photo': "Не удалось загрузить классификатор Haar Cascade."
                         " Повторите попытку позже или сообщите в техподдержку."
            })

        # Обнаружение лиц
        faces = face_cascade.detectMultiScale(
            gray_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(faces) == 0:
            raise serializers.ValidationError({'photo': "На фото не обнаружено лиц."})
        if len(faces) > 1:
            raise serializers.ValidationError({'photo': "На фото должно быть только одно лицо."})

        # Получение координат области лица
        face_coordinates = faces[0]  # Берем только первое лицо (x, y, w, h)
        x, y, w, h = face_coordinates
        return {
            "x": x,
            "y": y,
            "width": w,
            "height": h
        }

    except Exception as e:
        raise serializers.ValidationError({'photo': f"Ошибка обработки изображения: {str(e)}"})

def validate_people_add(data):
    custom_validate_first_name(data)
    custom_validate_last_name(data)
    custom_validate_middle_name(data)
    validate_photo(data)
