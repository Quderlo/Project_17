import json
from http.client import HTTPConnection, HTTPResponse
from typing import Dict, Union


class CameraClient:
    def __init__(self, host: str, port: int):
        # Указываем хост и порт сервиса камер
        self.host = host
        self.port = port

    async def _send_request(self, method: str, path: str) -> HTTPResponse:
        """
        Функция для выполнения HTTP запроса.
        Возвращает объект ответа HTTPConnection.
        """
        connection = HTTPConnection(self.host, self.port)
        connection.request(method, path, headers={"Accept": "application/json"})

        response = connection.getresponse()

        # Проверяем статус ответа
        if response.status != 200:
            print(f"Ошибка HTTP-запроса: {response.status}")
            connection.close()
            raise Exception(f"Ошибка HTTP-запроса: {response.status}")

        return response

    async def _decode_response(self, response: HTTPResponse) -> Union[Dict, str]:
        """
        Метод для декодирования ответа в JSON.
        """
        data = response.read().decode("utf-8")
        response_data = json.loads(data)

        return response_data
