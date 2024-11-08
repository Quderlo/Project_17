from typing import Dict, Union
from recognition_service.CameraClient import CameraClient


class CameraListClient(CameraClient):
    def __init__(self, host: str, port: int):
        # Инициализация родительского класса CameraClient
        super().__init__(host, port)

    async def fetch_camera_list(self) -> Union[Dict, str]:
        """
        Асинхронная функция для запроса списка камер с сервиса камер.
        """
        try:
            # Выполняем запрос на получение списка камер
            response = await self._send_request("GET", "/cameras")

            # Декодируем ответ
            camera_list = await self._decode_response(response)

            return camera_list
        except Exception as e:
            print(f"Ошибка запроса: {e}")
            return {"error": "Ошибка запроса к серверу камер"}