import os

import cv2
import numpy as np

from init_cams import init_cams


class Server:
    def __init__(self):
        self.connected_cameras = []
        self.get_new_cameras()
        self.display_frames()  # Запуск метода для отображения и сохранения кадров

    def get_new_cameras(self):
        self.connected_cameras += init_cams(self.connected_cameras)

    def display_frames(self):
        """
        Отображает и сохраняет кадры от каждой подключённой камеры в одном окне OpenCV.
        """
        while True:
            frames = []

            # Получаем кадры с каждой камеры и сохраняем в список frames
            for index, cam in enumerate(self.connected_cameras):
                frame = cam.get_frame()  # Получаем последний кадр камеры
                if frame is not None:
                    # Определяем путь к папке для сохранения
                    folder_path = os.path.join("camera_images", f"camera_{index}")
                    os.makedirs(folder_path, exist_ok=True)
                    file_path = os.path.join(folder_path, "current_frame.jpg")
                    cv2.imwrite(file_path, frame)  # Сохраняем кадр

                    # Изменяем размер кадра для общего окна
                    frame_resized = cv2.resize(frame, (320, 240))
                    frames.append(frame_resized)

            # Проверка, есть ли хотя бы один кадр для отображения
            if frames:
                # Рассчитываем сетку для мозаики кадров (количество столбцов зависит от числа камер)
                cols = 2  # Число столбцов в сетке
                rows = (len(frames) + cols - 1) // cols  # Число строк для размещения кадров

                # Дополнение кадров пустыми чёрными изображениями для заполнения сетки
                while len(frames) < rows * cols:
                    frames.append(np.zeros((240, 320, 3), dtype=np.uint8))

                # Объединение кадров в сетку
                mosaic = []
                for i in range(0, len(frames), cols):
                    mosaic.append(np.hstack(frames[i:i + cols]))
                final_frame = np.vstack(mosaic)

                # Отображение мозаики в одном окне
                cv2.imshow("Camera Feeds", final_frame)

            # Устанавливаем частоту обновления в окне (примерно 30 кадров в секунду)
            if cv2.waitKey(33) == 27:  # Выход по клавише ESC
                break

        cv2.destroyAllWindows()

server = Server()

