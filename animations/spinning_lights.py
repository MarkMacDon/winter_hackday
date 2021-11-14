import math
from datetime import datetime

import numpy as np

from test_animator import TestAnimator
from utils.color import hsv_to_rgb


class RotatingPlaneExample(TestAnimator):
    def initialize_animation(self):
        self.angle = 0

        self.color_A = (255,0,0) # red
        self.color_B = (0,255,0) # green

    def calculate_colors(self, xyz_coords, start_time):
        # the plan here is to have 2 colors rotating around the center of the tree
        # we have the coordinates of each light, xy_coords
        # we can turn any light above the y axis to color_A, and anything below to color_B
        # if we rotate the coordinates of the lights around the center, the lights above the axis will slowly rotate around
        # and so the lights above the Y axis will change

        # rotate the coordinates of the tree
        cos_angle = math.cos(self.angle)
        sin_angle = math.sin(self.angle)

        rotated_coords_x = xyz_coords[:, 0] * cos_angle - xyz_coords[:, 1] * sin_angle
        rotated_coords_y = xyz_coords[:, 0] * sin_angle + xyz_coords[:, 1] * cos_angle

        # create an array of colors, and initialize it to black (zeros)
        colors = np.zeros((self.NUM_LIGHTS, 3), dtype=np.uint8)

        # for each light, check if the rotated position  is currently above the y axis, and set its color accordingly
        for i in range(self.NUM_LIGHTS):
            if rotated_coords_y[i] > 0:
                colors[i] = self.color_A
            else:
                colors[i] = self.color_B

        # update the angle, so that next loop the rotation is incremented slightly
        # rotates 5 radians per second
        num_seconds_since_start = (datetime.now() - start_time).total_seconds()
        self.angle = num_seconds_since_start * 5

        # change the colors of A and B so that they change over time
        # 1 second is 10 degrees around the color wheel
        # color B is 180 degrees out of phase with color A
        hue_degrees = num_seconds_since_start * 10
        self.color_A = hsv_to_rgb(hue_degrees, 1, 1)
        self.color_B = hsv_to_rgb(hue_degrees + 180, 1, 1)

        return colors

if __name__ == "__main__":
    coords_path = "../data/coords.csv"
    anim = RotatingPlaneExample(coords_path)

    anim.animation_loop()