import asyncio
from utils.fetch_camera_list import fetch_camera_list


# Запускаем функцию и выводим список камер
async def main():
    camera_list = await fetch_camera_list()
    print("Список камер:", camera_list)


asyncio.run(main())
