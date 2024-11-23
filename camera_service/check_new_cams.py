from typing import List, Tuple

from camera_service.CameraClient import CameraClient


def check_new_cams(connected_cameras: List) -> Tuple[bool, List[str]]:
    """
    Проверяем, появились ли новые камеры, которые необходимо подключить.
    :param connected_cameras: Список объектов камер, которые уже были подключены.
    :return: Кортеж (список новых камер, bool, указывающий, были ли ошибки при чтении).
    """

    new_cameras_links = []
    read_successful = True

    try:
        # Запрос на получение камер через CameraClient
        client = CameraClient(host="127.0.0.1", port=8000)  # Указывайте ваш хост и порт
        new_cameras_links = client.get_camera_links()
    except Exception as e:
        print(f"Произошла ошибка при подключении к API: {e}")
        read_successful = False

    connected_paths = [cam.link for cam in connected_cameras]  # assuming `connected_cameras` has `link` field

    # Фильтрация новых камер
    new_cameras_links = [link for link in new_cameras_links if link not in connected_paths]

    return read_successful, new_cameras_links