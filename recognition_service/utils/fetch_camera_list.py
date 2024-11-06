import httpx
from config import Camera_Service_Settings as CS_settings


async def fetch_camera_list():
    """
    Асинхронная функция для запроса списка камер с сервиса камер.
    """
    print(CS_settings.root_full_path + CS_settings.list_cameras)
    async with httpx.AsyncClient() as client:
        try:
            headers = {
                "Content-Type": "application/json",
            }
            response = await client.get(CS_settings.root_full_path + CS_settings.list_cameras, headers=headers)
            response.raise_for_status()  # Проверяем на ошибки HTTP-запроса

            camera_list = response.json()  # Преобразуем ответ в JSON-формат
            return camera_list
        except httpx.HTTPStatusError as e:
            print(f"Ошибка HTTP-запроса: {e.response.status_code}")
            return {"error": f"Ошибка HTTP-запроса: {e.response.status_code}"}
        except httpx.RequestError as e:
            print(f"Ошибка запроса: {e}")
            return {"error": "Ошибка запроса к серверу камер"}

