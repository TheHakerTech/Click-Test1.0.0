import threading
from typing import Callable
import time
import flet as ft
import math

class Timer:
    def __init__(self, text_object: ft.Text, time: int = 1, on_end: Callable = None) -> None:
        self.endtime = time
        self.stopped = False

        self.text = text_object
        self.text.value = f'Времени осталось: {time}'

        self.on_end = on_end

    def start(self):
        start_time = self.endtime
        for i in range(math.floor(start_time * 10)):
            if not self.stopped:
                time.sleep(0.1)
                self.text.value = f'Времени осталось: {round(self.endtime, 2)}'
                self.endtime -= 0.1
                self.text.update()
            else:
                self.text.value = 'Времени осталось: 0'
                self.text.update()
                break
        else:
            self.text.value = 'Времени осталось: 0'
            self.text.update()
            self.stopped = True

            if self.on_end:
                self.on_end()
    
    def reset(self, text_object: ft.Text, time: int = 1, on_end: Callable = None):
        self.endtime = time
        self.stopped = False

        self.text = text_object
        self.text.value = f'Времени осталось: {time}'

        self.on_end = on_end
