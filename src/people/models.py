import numpy as np
from django.db import models

from cv_dlib_models.face_encoder import FaceEncoder


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

    last_seen = models.DateTimeField(
        auto_now=True,
        verbose_name='Последнее появление.',
        help_text='Последний раз когда человек появлялся на камерах.',
    )

    class Meta:
        verbose_name = "Человек"
        verbose_name_plural = "Люди"

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()

    def get_face_encoding(self, photo: np.ndarray) -> None:
        encoder = FaceEncoder()
        self.face_encoding = encoder.get_face_encoding(photo)



class PersonSighting(models.Model):
    """
    Модель для хранения информации о том, когда и на какой камере был замечен человек.
    """
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name="Человек",
        related_name="sightings"
    )

    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время обнаружения"
    )

    class Meta:
        verbose_name = "Появление на камере"
        verbose_name_plural = "Появления на камере"
        ordering = ["-create_at"]

    def __str__(self):
        return f"{self.person} замечен в {self.create_at:%Y-%m-%d %H:%M:%S}"

    def save(self, *args, **kwargs):
        if self.person:
            self.person.last_seen = self.create_at
            self.person.save(update_fields=['last_seen'])
        super().save(*args, **kwargs)


