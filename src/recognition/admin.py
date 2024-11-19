from django import forms
from django.contrib import admin
from recognition.models import Camera, CameraAuth

# Админка для модели Camera
@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'name', 'port', 'rtsp_path', 'auth')

    readonly_fields = ('created_at','is_active','rtsp_link', 'web_link',)

    # Разбиение полей на группы для удобства в админке
    fieldsets = (
        ('Заполняемые данные', {
            'fields': (
                'name',
                'ip_address',
                'port',
                'rtsp_path',
                'auth',
                'created_at',
                'is_active',
            )
        }),

        ('Автоматические пути', {
            'fields':
                ('rtsp_link', 'web_link'),
        }),
    )

    # Сортировка в списке объектов по полю `name`
    ordering = ('ip_address',)


# Админка для модели CameraAuth
@admin.register(CameraAuth)
class CameraAuthAdmin(admin.ModelAdmin):
    list_display = ('name', 'username',)

    fieldsets = (
        (None, {
            'fields': ('name',)
        }),

        ("Данные авторизации", {
            'fields': ('username', 'password')
        }),
    )

    ordering = ('name',)
