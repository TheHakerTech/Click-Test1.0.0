import flet as ft

def __boolean_theme(thememode: ft.ThemeMode):
    return True if thememode == ft.ThemeMode.LIGHT else False

def __return_color(light_color: str, dark_color: str, page: ft.Page):
    return light_color if __boolean_theme(page.theme_mode) else dark_color

def appbar(page: ft.Page):
    return __return_color(ft.colors.GREEN_100, ft.colors.GREEN, page)
