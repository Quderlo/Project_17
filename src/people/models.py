from django.db import models

class Person(models.Model):
    """
    Модель для хранения информации о человеке и данных его лица.
    """

    first_name = models.CharField(
        max_length=255,
        verbose_name="Имя"
    )

    last_name = models.CharField(
        max_length=255,
        verbose_name="Фамилия"
    )

    middle_name = models.CharField(
        max_length=255,
        verbose_name="Отчество",
        blank=True,
        null=True
    )

    face_encoding = models.BinaryField(
        verbose_name="Кодировка лица",
        help_text="Закодированные данные лица в виде массива (dlib).",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    class Meta:
        verbose_name = "Человек"
        verbose_name_plural = "Люди"

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()
