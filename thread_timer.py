from typing import Callable
import time
import flet as ft
import math
import threading
from datetime import datetime

class Timer:
    def __init__(self, text_object: ft.Text, progress_bar: ft.ProgressBar, time: int = 1, on_end: Callable = None) -> None:
        self.endtime = time
        self.stopped = False

        self.text = text_object
        self.text.value = f'Времени осталось: {time}'

        self.progress = progress_bar

        self.on_end = on_end

    def start(self):
        def thread():
            start_time = self.endtime

            for i in range(self.endtime):
                if not self.stopped:
                    time.sleep(1)
                    self.endtime -= 1
                    self.text.value = f'Времени осталось: {round(self.endtime, 2)}'
                    self.progress.value -= 1 / start_time

                    self.text.update()
                    self.progress.update()

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
        th = threading.Thread(target=thread)
        th.start()
    
    def reset(self, text_object: ft.Text, time: int = 1, on_end: Callable = None):
        self.endtime = time
        self.stopped = False

        self.text = text_object
        self.text.value = f'Времени осталось: {time}'

        self.on_end = on_end
