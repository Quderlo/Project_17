# RecognitionServer.py
from typing import Dict

from recognition_service.CameraList import CameraListClient
from config import Camera_Service_Settings as CS_settings
from recognition_service.SearchForFace import SearchForFace


class RecognitionServer:
    def __init__(self):
        self.camera_list_client = CameraListClient(
            host=CS_settings.root_url,
            port=CS_settings.root_port_int
        )
        self.search_services = []
        self.existing_camera_list = []
        self.get_new_cameras()

    def get_new_cameras(self) -> None:
        """
        Метод инициализирует подключение к новым камерам и добавляет только новые камеры.
        """
        new_cameras = self.camera_list_client.fetch_camera_list(self.existing_camera_list)
        self.existing_camera_list.extend(new_cameras)
        self.start_search_services(new_cameras)

    def start_search_services(self, new_cameras: list[Dict]) -> None:
        """
        Инициализирует экземпляры класса SearchForFace для каждой новой камеры.
        :param new_cameras: Список новых камер, для которых необходимо запустить сервисы распознавания лиц.
        """
        for camera in new_cameras:
            # Инициализация SearchForFace для каждой новой камеры
            search_service = SearchForFace(
                host=CS_settings.root_url,
                port=CS_settings.root_port_int,
                url=camera['path'],  # Путь или URL камеры
                index=camera['index']  # Индекс камеры
            )
            # Добавляем инициализированный экземпляр в список сервисов
            self.search_services.append(search_service)

        print("Сервисы распознавания лиц инициализированы для новых камер.")

    def shutdown(self):
        """
        Завершает все сервисы поиска лиц и останавливает потоки.
        """
        for service in self.search_services:
            service.shutdown()
