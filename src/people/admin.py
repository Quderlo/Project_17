from django.contrib import admin
from people.models import PersonSighting
from people.models import Person


# Админка для модели Person
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'last_seen', 'created_at',)
    readonly_fields = ('last_seen', 'created_at', 'face_encoding')

    # Разбиение полей на группы для удобства в админке
    fieldsets = (
        ('Основная информация', {
            'fields': ('first_name', 'last_name', 'middle_name', 'last_seen',)
        }),
        ('Дополнительные данные', {
            'fields': ('face_encoding', 'created_at')
        }),
    )

    # Сортировка в списке объектов по полю `last_name`
    ordering = ('last_name',)

    def has_add_permission(self, request):
        return False



# Админка для модели PersonSightings
@admin.register(PersonSighting)
class PersonSightingsAdmin(admin.ModelAdmin):
    list_display = ('person', 'create_at',)  # Поля для отображения в списке
    readonly_fields = ('person', 'create_at',)  # Все поля только для чтения

    # Разбиение полей на группы для удобства
    fieldsets = (
        ('Информация о появлении', {
            'fields': ('person', 'create_at',)
        }),
    )

    # Сортировка в списке объектов
    ordering = ('-create_at',)

    # Запрет на создание или изменение записей
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
