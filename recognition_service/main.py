import asyncio

from recognition_service.CameraList import CameraListClient
from config import Camera_Service_Settings as CS_settings


async def main():
    # Создаем экземпляр клиента камеры
    camera_list_client = CameraListClient(host=CS_settings.root_url, port=CS_settings.root_port_int)

    # Выполняем запрос на получение списка камер
    camera_list = await camera_list_client.fetch_camera_list()
    print(camera_list)


# Запуск основного кода
asyncio.run(main())
