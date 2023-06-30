import flet as ft
import sqlite3

def init_history(page: ft.Page):
    page.appbar = ft.AppBar(
        title=ft.Text('Click test'),
        center_title=False,
        bgcolor=ft.colors.GREEN_100,
    )

    def get_history():
        cn = sqlite3.connect('history.db')
        cr = cn.cursor()

        cr.execute('SELECT * FROM history')
        rows = cr.fetchall()
        return rows
    
    rows = get_history()

    datarows = []

    for clicks, cps, time in rows:
        datarows.append(ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(clicks)),
                ft.DataCell(ft.Text(cps)),
                ft.DataCell(ft.Text(time))
            ]
        ))

    page.add(ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('Клики'), numeric=True),
            ft.DataColumn(ft.Text('КПС'), numeric=True),
            ft.DataColumn(ft.Text('Время'), numeric=True)
        ],
        rows=datarows
    ))
