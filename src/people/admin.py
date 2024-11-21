from django.contrib import admin

from people.models import Person


# Админка для модели Person
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'created_at', 'photo_preview')
    readonly_fields = ('created_at', 'face_encoding')

    # Разбиение полей на группы для удобства в админке
    fieldsets = (
        ('Основная информация', {
            'fields': ('first_name', 'last_name', 'middle_name', 'photo')
        }),
        ('Дополнительные данные', {
            'fields': ('face_encoding', 'created_at')
        }),
    )

    # Сортировка в списке объектов по полю `last_name`
    ordering = ('last_name',)

    # Функция для отображения миниатюры фото
    def photo_preview(self, obj):
        if obj.photo:
            return f"<img src='{obj.photo.url}' width='50' height='50' style='object-fit: cover; border-radius: 5px;' />"
        return "Нет фото"

    photo_preview.short_description = "Фото"
    photo_preview.allow_tags = True
