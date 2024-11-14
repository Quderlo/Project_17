# CameraClient.py
import json
from http.client import HTTPConnection, HTTPResponse
from typing import Dict


class CameraClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def _send_request(self, method: str, path: str) -> HTTPResponse:
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

        return response

    def _decode_response(self, response: HTTPResponse) -> list[Dict, str]:
        """
        Метод для декодирования ответа в JSON.
        """
        data = response.read().decode("utf-8")
        return json.loads(data)
