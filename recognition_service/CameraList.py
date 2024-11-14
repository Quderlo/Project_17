# CameraListClient.py
from typing import Dict, List
from recognition_service.CameraClient import CameraClient
from config import Camera_Service_Settings as CS_settings


class CameraListClient(CameraClient):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)

    def fetch_camera_list(self, existing_cameras: List[Dict]) -> List[Dict]:
        """
        Запрашивает список камер с сервера и возвращает только новые камеры.
        """
        try:
            response = self._send_request("GET", CS_settings.list_cameras)
            camera_list = self._decode_response(response)
            new_cameras = []

            # Собираем пути всех существующих камер
            existing_paths = {cam['path'] for cam in existing_cameras}

            # Проверяем, есть ли текущая камера уже в списке существующих камер
            for camera in camera_list:
                if camera['path'] not in existing_paths:
                    new_cameras.append(camera)

            print("Новые камеры:", new_cameras)
            return new_cameras
        except Exception as e:
            print(f"Ошибка запроса: {e}")
            return []
