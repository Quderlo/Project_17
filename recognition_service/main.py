import asyncio
import json
from http.client import HTTPConnection
from typing import Dict, Union


class CameraClient:
    def __init__(self, host: str, port: int):
        # Указываем хост и порт сервиса камер
        self.host = host
        self.port = port

    async def fetch_camera_list(self) -> Union[Dict, str]:
        """
        Асинхронная функция для запроса списка камер с сервиса камер.
        """
        try:
            # Создаём соединение
            connection = HTTPConnection(self.host, self.port)
            connection.request("GET", "/cameras", headers={"Accept": "application/json"})

            # Получаем ответ
            response = connection.getresponse()
            if response.status != 200:
                print(f"Ошибка HTTP-запроса: {response.status}")
                return {"error": f"Ошибка HTTP-запроса: {response.status}"}

            # Читаем и декодируем данные
            data = response.read().decode("utf-8")
            camera_list = json.loads(data)

            return camera_list
        except Exception as e:
            print(f"Ошибка запроса: {e}")
            return {"error": "Ошибка запроса к серверу камер"}
        finally:
            connection.close()  # Закрываем соединение


async def main():
    # Создаем экземпляр клиента камеры
    camera_client = CameraClient(host="127.0.0.1", port=8001)

    # Выполняем запрос на получение списка камер
    camera_list = await camera_client.fetch_camera_list()
    print("Список камер:", camera_list)


# Запуск основного кода
asyncio.run(main())
