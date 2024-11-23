from init_cams import init_cams


class CamServer:
    def __init__(self):
        self.connected_cameras = []
        self.get_new_cameras()

    def get_new_cameras(self) -> None:
        """
        Метод инициализирует подключение к новым камерам.
        """
        self.connected_cameras += init_cams(self.connected_cameras)
        print(self.connected_cameras)

    def get_camera_list(self):
        """
        Возвращает список камер с их индексами и путями.
        """
        return [{"index": idx, "path": cam.link} for idx, cam in enumerate(self.connected_cameras)]

    def shutdown(self):
        for cam in self.connected_cameras:
            cam.capture.release()
        self.connected_cameras = []
