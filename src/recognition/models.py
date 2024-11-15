from django.db import models
from config import User_Config_Settings as US_settings


class Camera(models.Model):
    """
    Модель для хранения информации о камерах.
    """

    name = models.CharField(
        max_length=255,
        verbose_name="Название"
    )

    rtsp_link = models.URLField(
        max_length=500,
        verbose_name="RTSP-ссылка",
        blank=True,
        null=True
    )

    url = models.URLField(
        max_length=500,
        verbose_name="URL-адрес",
        blank=True,
        null=True
    )

    port = models.PositiveIntegerField(
        verbose_name="Порт",
        default=554,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Камера"
        verbose_name_plural = "Камеры"

    def get_http_link(self) -> str:
        """
        Метод для получения HTTP-ссылки на камеру.
        """
        if self.url and self.port:
            return f"http://{self.url}:{self.port}"
        return "Данные отсутствуют"

    def get_rtsp_link(self) -> str:
        """
        Метод для получения RTSP-ссылки на камеру.
        """
        if self.rtsp_link:
            return self.rtsp_link
        if self.url and self.port:
            return f"rtsp://{US_settings.user_password}@{self.url}:{self.port}/live/av0"
        return "Данные отсутствуют"

    def __str__(self):
        return self.name
