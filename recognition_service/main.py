# main.py
import cv2
import uvicorn
from recognition_service.CameraList import CameraListClient
from datetime import datetime
import pytz
from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager
from config import Recognition_Service_Settings as RS_settings
from RecognitionServer import RecognitionServer

server = RecognitionServer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Сервер запущен {datetime.now(pytz.utc)}")
    yield
    print(f"Сервер завершил работу {datetime.now(pytz.utc)}")
    # Закрываем окна после завершения
    server.shutdown()
    cv2.destroyAllWindows()


# Инициализация FastAPI с использованием lifespan
app = FastAPI(lifespan=lifespan)


@app.post(f"{RS_settings.refresh}")
async def refresh_cameras(background_tasks: BackgroundTasks):
    """
    Эндпоинт для обновления списка подключённых камер.
    """
    background_tasks.add_task(server.get_new_cameras)
    return {"status": "Камеры обновляются"}


if __name__ == '__main__':
    uvicorn.run(app, host=RS_settings.root_url, port=RS_settings.root_port_int)
