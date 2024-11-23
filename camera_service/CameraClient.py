import json
from http.client import HTTPConnection
from typing import List, Dict


class CameraClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def _send_request(self, method: str, path: str, body: dict = None) -> dict:
        """
        Функция для выполнения HTTP-запроса.
        """
        connection = HTTPConnection(self.host, self.port)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        # Если есть данные для отправки, добавляем их в body
        if body:
            body = json.dumps(body)
            connection.request(method, path, body, headers)
        else:
            connection.request(method, path, headers=headers)

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

    def post_camera_links(self, camera_links: List[str]) -> dict:
        """
        Отправка POST-запроса на сервер с ссылками на камеры.
        """
        body = {
            "links": camera_links
        }
        try:
            response = self._send_request('POST', '/api/v0/camera-register/', body)
            return response
        except Exception as e:
            print(f"Ошибка при отправке POST-запроса: {e}")
            return {}
