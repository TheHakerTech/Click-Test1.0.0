# -*- coding: utf-8 -*-
import math
class Result: # Class for eval your CPS by clicks and time
    def __init__(
        self,
        clicks: int,
        time: int,
        floorLevel=2
    ):
        # Save variables
        self.clicks: int = clicks
        self.time: int = time
        self.floorLevel = floorLevel
        # Eval cps
        self.cps = math.floor(clicks/time)
