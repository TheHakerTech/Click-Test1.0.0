import flet as ft

def main(page: ft.Page):
    page.title = 'Click test'
    page.window_height, page.window_width = 400, 400
    page.window_resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.GREEN,
            primary_container=ft.colors.GREEN_200
        )
    )

    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == ' ':
            start_func
        else:
            page.add(
                ft.Text(
                    f"Key: {e.key}, Shift: {e.shift}, Control: {e.ctrl}, Alt: {e.alt}, Meta: {e.meta}"
                )
            )

    page.on_keyboard_event = on_keyboard

    def click(e):
        start_button.data += 1
        count.value = f'Клики: {start_button.data}'
        start_button.update()
        count.update()

    def start_func(e):
        if start_button.on_click != click:
            start_button.text = 'Кликайте!'
            start_button.on_click = click
            start_button.data = 0
            start_button.update()

    count = ft.Text('Клики: 0')
    start_button = ft.FilledButton('Старт', width=300, height=100, on_click=start_func)

    page.add(count, start_button)

ft.app(main)