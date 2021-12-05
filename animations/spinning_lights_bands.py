import math
from datetime import datetime

import numpy as np

from tree_animator import TreeAnimator
from utils.color import hsv_to_rgb


class RotatingPlaneExample(TreeAnimator):

    red = (255,0,0) # red
    green = (0,255,0) # green
    blue = (0,0,255) # blue
    white = (255,255,255) # white 

    def initialize_animation(self):
        coords = self._xyz_coords.copy() # not sure why this is necessary but thank you
        self.angle = 0
        self.z_height = coords[:,2].max() # start at the top and move down
        self.z_bottom = coords[:,2].min()                      
        self.z_top = coords[:,2].max()
        amp_height = self.z_top - self.z_bottom
        self.band_height = amp_height / 10

        self.color_A = self.red
        self.color_B = self.green
        self.color_C = self.blue
        self.color_D = self.white 

    def swap_colors(self):
        if self.color_A == (255,0,0):
            self.color_A = self.blue
            self.color_B = self.white
            self.color_C = self.red
            self.color_D = self.green
        elif self.color_A == self.blue:
            self.color_A = self.red
            self.color_B = self.green
            self.color_C = self.blue
            self.color_D = self.white 

    def calculate_colors(self, xyz_coords, start_time):
        # the plan here is to have 2 colors rotating around the center of the tree
        # and also moving up/down the trunk :)
        # we have the coordinates of each light, xy_coords
        # we can turn any light above the y axis to color_A, and anything below to color_B
        # add in z: anything above color_C, below color_D
        # if we rotate the coordinates of the lights around the center, the lights above the axis will slowly rotate around
        # then also slowly move z down
        # and so the lights above the Y axis will change
        # and swirl down!

        # rotate the coordinates of the tree
        cos_angle = math.cos(self.angle)
        sin_angle = math.sin(self.angle)

        rotated_coords_x = xyz_coords[:, 0] * cos_angle - xyz_coords[:, 1] * sin_angle
        rotated_coords_y = xyz_coords[:, 0] * sin_angle + xyz_coords[:, 1] * cos_angle

        # create an array of colors, and initialize it to black (zeros)
        colors = np.zeros((self.NUM_LIGHTS, 3), dtype=np.uint8)

        # for each light, check if the rotated position  is currently above the y axis, and set its color accordingly
        for i in range(self.NUM_LIGHTS):
            if rotated_coords_y[i] > 0 and xyz_coords[:, 2][i] > self.z_height:
                colors[i] = self.color_A
            elif rotated_coords_y[i] > 0 and xyz_coords[:, 2][i] <= self.z_height:
                colors[i] = self.color_C
            elif rotated_coords_y[i] <= 0 and xyz_coords[:, 2][i] <= self.z_height:
                colors[i] = self.color_D
            else:
                colors[i] = self.color_B

        # update the angle, so that next loop the rotation is incremented slightly
        # rotates 5 radians per second
        num_seconds_since_start = (datetime.now() - start_time).total_seconds()
        self.angle = num_seconds_since_start * 5

        self.z_height = self.z_top - ((int(num_seconds_since_start) % 10) * self.band_height)

        if int(num_seconds_since_start) % 20 == 10:
            if self.color_A == self.red:
                self.swap_colors()
        elif int(num_seconds_since_start) % 20 == 0:
            if self.color_A == self.blue:
                self.swap_colors()

        return colors

if __name__ == "__main__":
    anim = RotatingPlaneExample()

    anim.animation_loop()