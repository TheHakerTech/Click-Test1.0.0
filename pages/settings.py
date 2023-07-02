import flet as ft
import sqlite3

import utils.theme_colors as clr
import utils.settings_setter as wwsettings

def divider():
    return ft.Divider(visible=True)

def init_settings(page: ft.Page):
    page.appbar = ft.AppBar(
        title=ft.Text('Click test'),
        center_title=False,
        bgcolor=clr.appbar(page),
    )
    page.update()

    data = wwsettings.loadSettings()

    def change_page():
        if light_theme.value:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        light_theme.label = (
            "Светлая тема" if page.theme_mode == ft.ThemeMode.LIGHT else "Темная тема"
        )
        page.appbar = ft.AppBar(
            title=ft.Text('Click test'),
            center_title=False,
            bgcolor=clr.appbar(page),
        )
        page.update()

    def change_settings(e=None):
        global data
        for i in (history_paused, light_theme, linechart):
            data = wwsettings.changeSetting(i.data, i.value)

        change_page()
        page.update()
    
    def reset_history_func(e):
        cn = sqlite3.connect('history.db')
        cr = cn.cursor()

        cr.execute('DELETE FROM history')
        cn.commit()

        page.snack_bar= ft.SnackBar(
            content=ft.Text('История успешно сброшена', color=clr.snackbar_text(page)),
            bgcolor=clr.snackbar(page)
        )
        page.snack_bar.open = True
        page.update()


    history_paused = ft.Switch(label='Не записывать историю', value=data['history_paused'], on_change=change_settings, data='history_paused')
    reset_history = ft.FilledButton(text='Сбросить историю', on_click=reset_history_func)

    light_theme = ft.Switch(label='Светлая тема', value=data['light_theme'], on_change=change_settings, data='light_theme')

    linechart = ft.Switch(label='График (DEV)', value=data['linechart'], on_change=change_settings, data='linechart')

    categories = {
        'История': [
            history_paused,
            reset_history
        ],
        'Персонализация': [
            light_theme,
        ],
        'Для разработчиков': [
            linechart,
        ]
    }

    def get_result():
        res = []
        for name, controls in categories.items():
            res.append(ft.Text(name))
            for i in controls:
                res.append(i)
            res.append(divider())
        return res[:-1]

    page.add(*get_result())
