import flet as ft
from pages.clicker import init_clicker
from pages.history import init_history
from pages.settings import init_settings, __loadSettings

def main(page: ft.Page):
    def change(e: ft.ControlEvent):
        page.controls.clear()
        page.update()

        match e.control.selected_index:
            case 0:
                init_clicker(page)
                page.update()
            case 1:
                init_history(page)
                page.update()
            case 2:
                init_settings(page)
                page.update()

    page.navigation_bar = ft.NavigationBar(
        on_change=change,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.MOUSE_OUTLINED, selected_icon=ft.icons.MOUSE, label='Click'),
            ft.NavigationDestination(icon=ft.icons.HISTORY, label='History'),
            ft.NavigationDestination(icon=ft.icons.SETTINGS, label='Settings')
        ],
        selected_index=0
    )
    page.window_height, page.window_width = 400, 400
    page.window_resizable = False
    page.window_maximizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.GREEN,
            primary_container=ft.colors.GREEN_200
        )
    )

    def synthetic_event(page: ft.Page, control: ft.NavigationBar):
        control.on_change(
            ft.ControlEvent(
                target=control.uid,
                name="change",
                data=str(control.selected_index),
                control=control,
                page=page
            )
        )

    page.navigation_bar.did_mount = lambda: synthetic_event(
        page=page, control=page.navigation_bar
    )

    # call the did_mount() once manually if you mess up the order of page.update()
    # page.navigation_bar.did_mount()

    if __loadSettings()['light_theme']:
            page.theme_mode = ft.ThemeMode.LIGHT
    else:
        page.theme_mode = ft.ThemeMode.DARK

    page.update()

    init_clicker(page)
    page.window_center()

    # def on_keyboard(e: ft.KeyboardEvent):
    #     if e.key == 'Arrow Right':
    #         page.navigation_bar.selected_index += 1
    #         page.update()

    # page.on_keyboard_event = on_keyboard

    page.update()

if __name__ == '__main__':
    ft.app(main)
