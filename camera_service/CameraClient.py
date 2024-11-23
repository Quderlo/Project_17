# CameraClient.py
import json
from http.client import HTTPConnection, HTTPResponse
from typing import List, Tuple


class CameraClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def _send_request(self, method: str, path: str) -> dict:
        """
        Функция для выполнения HTTP-запроса.
        """
        connection = HTTPConnection(self.host, self.port)
        connection.request(method, path, headers={"Accept": "application/json"})
        response = connection.getresponse()

        if response.status != 200:
            print(f"Ошибка HTTP-запроса: {response.status}")
            connection.close()
            raise Exception(f"Ошибка HTTP-запроса: {response.status}")

        return self._decode_response(response)

    def _decode_response(self, response) -> dict:
        """
        Метод для декодирования ответа в JSON.
        """
        data = response.read().decode("utf-8")
        return json.loads(data)

    def get_camera_links(self) -> List[str]:
        """
        Запрос к API для получения всех ссылок на камеры.
        """
        try:
            response_data = self._send_request('GET', '/api/v0/camera-register/')
            return [camera['rtsp_link'] for camera in response_data]
        except Exception as e:
            print(f"Ошибка при получении ссылок камер: {e}")
            return []
