import flet as ft
import json
import utils.theme_colors as clr

settingsPath = 'settings.json'

def __loadSettings():
    with open(settingsPath, 'r', encoding='utf-8') as settingsFile:
        rawJson = settingsFile.read()
    return json.loads(rawJson)

def __writeSettings(settings: dict):
    with open(settingsPath, 'w', encoding='utf-8') as settingsFile:
        settingsFile.write(json.dumps(settings, skipkeys=True))

def init_settings(page: ft.Page):
    page.appbar = ft.AppBar(
        title=ft.Text('Click test'),
        center_title=False,
        bgcolor=clr.appbar(page),
    )
    page.update()

    data = __loadSettings()

    def change_page():
        if light_theme.value:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        light_theme.label = (
            "Светлая тема" if page.theme_mode == ft.ThemeMode.LIGHT else "Темная тема"
        )

    def change_settings(e=None):
        global data
        data = __loadSettings()
        for i in (history_paused, light_theme):
            data[i.data] = i.value

        change_page()
        page.update()
        __writeSettings(data)

    history_paused = ft.Switch(label='Не записывать историю', value=data['history_paused'], on_change=change_settings, data='history_paused')
    light_theme = ft.Switch(label='Светлая тема', value=data['light_theme'], on_change=change_settings, data='light_theme')

    page.add(history_paused, light_theme)
