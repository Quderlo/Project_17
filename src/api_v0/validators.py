import cv2
import requests
from rest_framework import serializers

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


# TODO: Убрать
if __name__ == '__main__':
    class Auth:
        def __init__(self):
            self.username = 'admin'
            self.password = 'pgZqfq86'

    auth = Auth()

    data = {
        'name': '',
        'ip_address': "192.168.88.91",
        'rtsp_path': "/live/av0",
        'auth': auth,
    }

    validate_camera(data)

