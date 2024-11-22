from django.contrib import admin

from people.models import Person


# Админка для модели Person
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'created_at',)
    readonly_fields = ('created_at', 'face_encoding')

    # Разбиение полей на группы для удобства в админке
    fieldsets = (
        ('Основная информация', {
            'fields': ('first_name', 'last_name', 'middle_name',)
        }),
        ('Дополнительные данные', {
            'fields': ('face_encoding', 'created_at')
        }),
    )

    # Сортировка в списке объектов по полю `last_name`
    ordering = ('last_name',)

