def check_new_cams(connected_cameras: list) -> tuple:
    """
    Проверяем, появились ли новые камеры, которые необходимо подключить.
    :param connected_cameras: Список объектов камер, которые уже были подключены.
    :return: Кортеж (список новых камер, bool, указывающий, были ли ошибки при чтении).
    """
    camera_paths = []
    read_successful = True

    try:
        with open('cameras.txt', 'r') as file:
            camera_paths = [line.strip() for line in file]

    except FileNotFoundError:
        print("Ошибка: Файл 'cameras.txt' не найден. Проверьте правильность пути к файлу")
        read_successful = False

    except PermissionError:
        print("Ошибка: Недостаточно прав для доступа к файлу")
        read_successful = False

    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        read_successful = False

    connected_paths = []
    for cam in connected_cameras:
        connected_paths += cam.link

    new_cameras_links = [camera for camera in camera_paths if camera not in connected_paths]

    return read_successful, new_cameras_links
