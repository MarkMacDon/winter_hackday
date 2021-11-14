import csv
from datetime import datetime

import numpy as np
import neopixel
import board

from tree_animator.animator import LightsAnimator

pixel_pin = board.D18
ORDER = neopixel.RGB

class NeopixelAnimator(LightsAnimator):
    def __init__(self, coords_path, brightness=1, num_pixels=500):
        # call the parent
        super().__init__(coords_path=coords_path)

        # initiate the neopixel rasberry pi interface
        self.neopixel = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=brightness, auto_write=False, pixel_order=ORDER)

    def _render_colors(self, colors):
        # assign each neopixel to the right color
        for i, color in enumerate(colors):
            pixel_id = self._id_mapping[i]
            self.neopixel[pixel_id] = color

        # broadcast the color changes to the string of LED lights
        self.neopixel.show()