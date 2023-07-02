import flet as ft
from thread_timer import Timer
import sqlite3
import utils.theme_colors as clr
import utils.settings_setter as wwsettings

Time = 1 # secs
TIMES = [1, 2, 5, 10, 30, 60] # secs

cn = sqlite3.connect('history.db')
cr = cn.cursor()

cr.execute('CREATE TABLE IF NOT EXISTS history (clicks integer, cps integer, time integer)')
cn.commit()

def init_clicker(page: ft.Page):
    def reset(e=None):
        start_button.text = 'Старт'
        start_button.on_click = start_func
        start_button.bgcolor = 'green'
        start_button.data = 0
        start_button.update()

        timer_text.value = f'Времени осталось: {Time}'
        timer_text.update()

        count_text.value = str(start_button.data)
        count_text.update()

        progress_bar.value = 1
        progress_bar.update()

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
            content=ft.Text(f'Твой средний КПС составил {cps} кликов в секунду'),
            actions=[
                ft.TextButton('Ок', on_click=close_dlg)
            ]
        )

        page.dialog = dlg
        page.dialog.open = True
        page.update()

        cn = sqlite3.connect('history.db')
        cr = cn.cursor()

        if not wwsettings.getSetting('history_paused'):
            cr.execute(f'INSERT INTO history VALUES ({start_button.data}, {cps}, {Time})')
            cn.commit()
        
        cr.execute('SELECT MAX(cps) FROM history')
        rec_cps = str(cr.fetchone()[0])
        record_text.value = f'Твой рекорд: {rec_cps if rec_cps != "None" else "0"} среднего кпс'

    def click(e=None):
        start_button.data += 1
        count_text.value = str(start_button.data)
        start_button.update()
        count_text.update()

    def start_func(e):
        if start_button.on_click != click:
            start_button.text = 'Жги!'
            start_button.bgcolor = ft.colors.ORANGE_ACCENT
            start_button.on_click = click
            start_button.data = 0
            start_button.update()

            click()
            timer.start()

    count_text = ft.Text('0', size=50, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.END, width=100)
    timer_text = ft.Text('')

    progress_bar = ft.ProgressBar(width=600, height=10, value=1)
    start_button = ft.FilledButton('Покажи на что способен)', width=370, height=100, on_click=start_func)
    

    timer = Timer(timer_text, progress_bar, Time, end)

    cn = sqlite3.connect('history.db')
    cr = cn.cursor()

    cr.execute('SELECT MAX(cps) FROM history')
    rec_cps = str(cr.fetchone()[0])

    record_text = ft.Text(f'Твой рекорд: {rec_cps if rec_cps != "None" else "0"} среднего кпс', size=30)

    page.add(record_text, timer_text, progress_bar, ft.Row([start_button, count_text]))

    if wwsettings.getSetting('linechart'):
        chart = ft.LineChart(data_series=[
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(0, 0),
                    ft.LineChartDataPoint(1, 4),
                    ft.LineChartDataPoint(2, 8),
                    ft.LineChartDataPoint(3, 6)
                ],
                stroke_width=5,
                color=ft.colors.GREEN,
                curved=True,
                stroke_cap_round=True
            )
        ],
            border=ft.border.all(3, ft.colors.GREEN),
            horizontal_grid_lines=ft.ChartGridLines(interval=1, color=ft.colors.GREY),
            vertical_grid_lines=ft.ChartGridLines(interval=1, color=ft.colors.GREY),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=1,
                        label=ft.Text('1')
                    ),
                    ft.ChartAxisLabel(
                        value=2,
                        label=ft.Text(2)
                    )
                ]
            )
        )

        page.add(chart)

