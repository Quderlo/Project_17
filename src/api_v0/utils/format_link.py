from config import User_Config_Settings as UC_settings

def format_rtsp_link(rtsp_link: str) -> str:
    """
    Проверка ссылки на содержание данных для авторизации
    Иначе добавляет их
    :param rtsp_link: RTSP ссылка на камеру
    :return: Ссылка с данными для авторизации
    """
    if not rtsp_link:
        return ''

    if "@" in rtsp_link:
        return rtsp_link

    user = UC_settings.user
    password = UC_settings.password

    # Проверяем, чтобы пользователь и пароль были заданы
    if not user or not password:
        raise ValueError("Не указаны пользователь или пароль для RTSP-ссылки.")

    # Форматируем ссылку
    parts = rtsp_link.split("rtsp://", 1)
    if len(parts) == 2:
        formatted_link = f"rtsp://{user}:{password}@{parts[1]}"
        return formatted_link
    else:
        raise ValueError(f"Некорректный формат RTSP-ссылки: {rtsp_link}")
