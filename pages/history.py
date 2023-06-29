import flet as ft

def init_history(page: ft.Page):
    page.appbar = ft.AppBar(
        title=ft.Text('Click test'),
        center_title=False,
        bgcolor=ft.colors.GREEN_100,
    )

    page.add(ft.Text('Test'))