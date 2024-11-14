import cv2
import dlib
import numpy as np

from recognition_service.CameraClient import CameraClient
from config import Camera_Service_Settings as CS_settings
from concurrent.futures import ThreadPoolExecutor


class SearchForFace(CameraClient):
    def __init__(self, host: str, port: int, url: str, index: int):
        super().__init__(host, port)
        self.camera_index = index
        self.camera_url = url
        self.detector = dlib.get_frontal_face_detector()

        # Запускаем обработку изображений в отдельном потоке
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.executor.submit(self.get_image)

    def get_image(self) -> None:
        """
        Метод для получения изображения с камеры, поиска лиц, обрезки и сохранения их в self.last_faces.
        """
        while True:
            try:
                # Получаем изображение в бинарном формате с сервера
                response = self._send_request(
                    method="GET",
                    path=CS_settings.image + f"{self.camera_index}",
                )

                image_data = response.read()
                np_arr = np.frombuffer(image_data, np.uint8)
                image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                if image is not None:
                    # Обнаружение лиц на изображении
                    faces = self.detector(image, 1)
                    last_faces = []  # Очищаем список для новых лиц

                    for face in faces:
                        # Обрезка изображения по координатам найденного лица
                        cropped_face = image[face.top():face.bottom(), face.left():face.right()]
                        last_faces.append(cropped_face)  # Сохраняем обрезанное лицо


            except Exception as e:
                print(f"Ошибка получения или обработки изображения: {e}")
                break

    def shutdown(self):
        """
        Метод завершает работу потока и закрывает executor.
        """
        self.executor.shutdown(wait=True)
