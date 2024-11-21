from django.db import models


class CameraAuth(models.Model):
    """
    Модель для хранения информации об авторизации камер.
    """
    name = models.CharField(
        max_length=255,
        verbose_name='Название для авторизации',
        help_text='Название набора камер с одинаковой системы авторизации',
    )

    username = models.CharField(
        max_length=255,
        verbose_name="Имя пользователя",
        help_text="Имя пользователя для доступа к камере."
    )
    password = models.CharField(
        max_length=255,
        verbose_name="Пароль",
        help_text="Пароль для доступа к камере."
    )

    class Meta:
        verbose_name = "Авторизация камеры"
        verbose_name_plural = "Авторизации камер"

    def __str__(self):
        return f"{self.name}"


class Camera(models.Model):
    """
    Модель для хранения информации о камерах.
    """

    ip_address = models.GenericIPAddressField(
        verbose_name='IP-адрес камеры',
    )

    port = models.PositiveIntegerField(
        verbose_name='Порт камеры',
        help_text='По умолчанию 554',
        default=554,
    )

    name = models.CharField(
        max_length=255,
        verbose_name='Имя для камеры',
        help_text='Названием может быть местоположение камеры.',
    )

    rtsp_link = models.URLField(
        verbose_name='RTSP - ссылка',
        blank=True,
        null=True,
        help_text='Если ссылка не указана, будет автоматически сгенерирована.',
    )

    rtsp_path = models.CharField(
        max_length=255,
        verbose_name='Путь RTSP',
        help_text="Путь RTSP потока. Например, '/live/av0' или 'Streaming/Channels/101'."
    )

    web_link = models.URLField(
        verbose_name='HTTP-ссылка на веб-интерфейс камеры',
        blank=True,
        null=True,
    )

    auth = models.ForeignKey(
        CameraAuth,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Авторизация камеры",
        help_text="Данные авторизации для этой камеры."
    )

    is_active = models.BooleanField(
        default=False,
        verbose_name="Камера активна",
        help_text="Используется ли эта камера в системе."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления",
    )

    def generate_rtsp_link(self) -> str:
        """
        Генерирует RTSP-ссылку с использованием данных авторизации и пути RTSP.
        """
        if self.rtsp_link:
            return self.rtsp_link

        auth_part = f"{self.auth.username}:{self.auth.password}@" if self.auth else ""
        return f"rtsp://{auth_part}{self.ip_address}:{self.port}{self.rtsp_path}"


    def generate_web_link(self) -> str:
        """
        Возвращает HTTP-ссылку для камеры.
        """
        return f"http://{self.ip_address}"

    class Meta:
        verbose_name = "Камера"
        verbose_name_plural = "Камеры"

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        """
        Генерация ссылок в save()
        """
        if not self.rtsp_link:
            self.rtsp_link = self.generate_rtsp_link()
        if not self.web_link:
            self.web_link = self.generate_web_link()
        super().save(*args, **kwargs)