import flet as ft
from thread_timer import Timer
import sqlite3
import utils.theme_colors as clr

Time = 1 # secs
TIMES = [1, 2, 5, 10, 30, 60] # secs

cn = sqlite3.connect('history.db')
cr = cn.cursor()

cr.execute('CREATE TABLE IF NOT EXISTS history (clicks integer, cps integer, time integer)')
cn.commit()

def init_clicker(page: ft.Page):
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == ' ':
            start_func()

    page.on_keyboard_event = on_keyboard

    def reset(e=None):
        start_button.text = 'Старт'
        start_button.on_click = start_func
        start_button.bgcolor = 'green'
        start_button.data = 0
        start_button.update()

        timer_text.value = f'Времени осталось: {Time}'
        timer_text.update()

        count_text.value = f'Клики: {start_button.data}'
        count_text.update()

        timer.reset(timer_text, Time, end)
    
    def get_items_for_appbar():
        res = []

        def change_time(e):
            global Time
            Time = e.control.data
            reset()

        for i in TIMES:
            res.append(ft.PopupMenuItem(text=f'{i} секунд', data=i, on_click=change_time))

        return res

    page.appbar = ft.AppBar(
        title=ft.Text('Click test'),
        center_title=False,
        bgcolor=clr.appbar(page),
        actions=[
            ft.PopupMenuButton(
                items=get_items_for_appbar()
            )
        ]
    )

    def end():
        start_button.on_click = reset
        start_button.text = 'Сброс'
        start_button.bgcolor = 'red'

        timer_text.value = 'Время закончилось'
        timer_text.update()
        start_button.update()

        cps = start_button.data / Time

        def close_dlg(e):
            page.dialog.open = False
            page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text('Результат'),
            content=ft.Text(f'Твой КПС составил {cps} кликов в секунду'),
            actions=[
                ft.TextButton('Ок', on_click=close_dlg)
            ]
        )

        page.dialog = dlg
        page.dialog.open = True
        page.update()

        cn = sqlite3.connect('history.db')
        cr = cn.cursor()

        cr.execute(f'INSERT INTO history VALUES ({start_button.data}, {cps}, {Time})')
        cn.commit()

    def click(e=None):
        start_button.data += 1
        count_text.value = f'Клики: {start_button.data}'
        start_button.update()
        count_text.update()

    def start_func(e):
        if start_button.on_click != click:
            start_button.text = 'Кликайте!'
            start_button.on_click = click
            start_button.data = 0
            start_button.update()
            
            timer.start()
            click()


    count_text = ft.Text('Клики: 0')
    timer_text = ft.Text('')
    timer = Timer(timer_text, Time, end)
    start_button = ft.FilledButton('Старт', width=300, height=100, on_click=start_func)

    page.add(count_text, timer_text, start_button)