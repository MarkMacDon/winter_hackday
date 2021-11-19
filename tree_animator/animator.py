import csv
from datetime import datetime

import numpy as np

class LightsAnimator():
    def __init__(self, coords_path):
        self._coords = []
        # read in the coordinates file
        with open(coords_path) as f:
            reader = csv.reader(f)
            for row in reader:
                # convert each row to 0
                id, x, y, z = [int(e) for e in row]
                # z = 0
                self._coords.append((id, x, y, z))

        self.NUM_LIGHTS = len(self._coords)

        # convert the coordinates into a Nx3 array
        self._coords = np.array(self._coords)
        self._id_mapping = self._coords[:,0]
        self._xyz_coords = self._coords[:,1:]

        # center the coordinates
        center = self._xyz_coords.mean(axis=0)
        self._xyz_coords = self._xyz_coords - center

    def _render_colors(self, colors):
        raise NotImplementedError("Looks like you are using the base animator class, make sure to use the neopixel animator")

    def animation_loop(self, n_loops=None, n_time=None):
        self.initialize_animation()
        start_time = datetime.now()

        if n_loops:
            for i in range(n_loops):
                colors = self._safe_calculate_colors(self._xyz_coords.copy(), start_time)
                self._render_colors(colors)
        elif n_time:
            while (datetime.now() - start_time).total_seconds() < n_time:
                colors = self._safe_calculate_colors(self._xyz_coords.copy(), start_time)
                self._render_colors(colors)
        else:
            while True:
                colors = self._safe_calculate_colors(self._xyz_coords.copy(), start_time)
                self._render_colors(colors)

        self.finalize_animation()

    def _safe_calculate_colors(self, xyz_coords, start_time):
        colors = self.calculate_colors(xyz_coords, start_time)

        # check that we have the right number of colors for our number of pixels
        if not (colors.shape[0] == self.NUM_LIGHTS and colors.shape[1] == 3):
            raise Exception(f"number of colors returned ({colors.shape[0]}x{colors.shape[1]}) does not match the expected number of lights ({len(self._id_mapping)}x3")
        if colors.dtype != np.uint8:
            raise Exception("the colors should be of type np.uint8, colors should be in the range 0-255")

        return colors

    def initialize_animation(self):
        pass

    def finalize_animation(self):
        pass

    def calculate_colors(self, xyz_coords, start_time):
        raise NotImplementedError("Looks like you are using the base animator class, make sure to override the calculate_colors method in your extension")