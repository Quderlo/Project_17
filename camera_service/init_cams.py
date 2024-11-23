import cv2
from camera import Camera
from camera_service.CameraClient import CameraClient
from check_new_cams import check_new_cams

def init_cams(connected_cameras: list) -> list:
    """
    Возвращает список объектов камер и отправляет новые ссылки на сервер.
    :param connected_cameras: Список уже подключенных объектов камер.
    :return: Возвращает список камер, которые были подключены.
    """
    read_successful, cam_paths = check_new_cams(connected_cameras)
    cam_buffer = []

    if read_successful:
        for path in cam_paths:
            cam_buffer.append(Camera(path))

        # Отправка новых камер на сервер через API, если новые камеры есть
        if cam_paths:
            client = CameraClient(host="127.0.0.1", port=8000)  # Указываем ваш хост и порт API
            response = client.post_camera_links(cam_paths)
            if response:
                print(f"Новые камеры успешно отправлены на сервер: {cam_paths}")
            else:
                print("Не удалось отправить новые камеры на сервер.")
    else:
        print("Не удалось прочитать пути к камерам.")

    for cam in cam_buffer:
        if not cam.capture.isOpened():
            print(f'Ошибка! Камера по пути {cam.link} не была подключена.')
            cam.release()

    return cam_buffer
