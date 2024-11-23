import cv2
import dlib
import numpy as np
import os
from scipy.spatial import distance
from django.apps import apps
from project.settings import face_threshold


class FaceEncoder:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        models_dir = os.path.join(base_dir, 'cv_dlib_models')

        shape_predictor_path = os.path.join(models_dir, "shape_predictor_68_face_landmarks.dat")
        face_rec_model_path = os.path.join(models_dir, "dlib_face_recognition_resnet_model_v1.dat")

        # Загрузка моделей
        self.shape_predictor = dlib.shape_predictor(shape_predictor_path)
        self.face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)

    def get_face_encoding(self, photo: np.ndarray) -> bytes:
        """
        Получение face encoding для переданного изображения.
        :param photo: Обрезанное фото лица в формате NumPy массива.
        :return: Кодировка лица в виде байтов.
        """
        try:
            # Преобразование фото в BGR, если оно было в RGB
            if photo.shape[2] == 3:
                bgr_photo = cv2.cvtColor(photo, cv2.COLOR_RGB2BGR)
            else:
                raise ValueError("Некорректный формат фото для обработки.")

            landmarks = self.shape_predictor(
                bgr_photo,
                dlib.rectangle(0, 0, photo.shape[1], photo.shape[0])
            )

            encoding = np.array(self.face_rec_model.compute_face_descriptor(bgr_photo, landmarks))

            # Проверка на существование в базе
            if self.is_face_in_database(encoding):
                raise ValueError("Лицо уже есть в базе.")

            return encoding.tobytes()

        except Exception as e:
            raise ValueError(f"Не удалось сгенерировать кодировку лица. {e}" )

    def is_face_in_database(self, encoding: np.ndarray, threshold=face_threshold) -> bool:
        """
        Проверка, существует ли человек с таким лицом в базе данных.
        :param encoding: Кодировка лица (массив NumPy).
        :param threshold: Пороговое значение для евклидова расстояния.
        :return: True, если лицо найдено, иначе False.
        """
        try:
            # Динамический импорт модели Person
            Person = apps.get_model('people', 'Person')
            people = Person.objects.exclude(face_encoding=None)

            for person in people:
                stored_encoding = np.frombuffer(person.face_encoding, dtype=np.float64)

                distance_between = distance.euclidean(encoding, stored_encoding)

                if distance_between < threshold:
                    return True

            return False
        except Exception as e:
            print(f"Ошибка при проверке лица в базе данных: {e}")
            raise ValueError("Ошибка при поиске лица в базе данных.")
