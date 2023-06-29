import flet as ft
from pages.clicker import init_clicker
from pages.history import init_history

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

    page.navigation_bar = ft.NavigationBar(
        on_change=change,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.MOUSE_OUTLINED, selected_icon=ft.icons.MOUSE, label='Click'),
            ft.NavigationDestination(icon=ft.icons.HISTORY, label='History')
        ]
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
    page.update()

    init_clicker(page)
    page.update()

ft.app(main)