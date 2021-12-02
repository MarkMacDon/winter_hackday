import math
from datetime import datetime

import numpy as np

from tree_animator import TreeAnimator

class Sphere():
    def __init__(self, position, velocity, radius, color):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.radius = radius
        self.color = color

    def render(self, light_xyz, light_colors):
        light_distance_from_sphere = np.linalg.norm(light_xyz - self.position, axis=1)
        lights_within_radius = light_distance_from_sphere <= self.radius

        light_colors[lights_within_radius] = self.color


class MovingObjectExample(TreeAnimator):
    def initialize_animation(self):
        self.balls = [
            Sphere(position=[0,150,0], velocity=[0,0,0], radius=100, color=[255,0,0]),
            Sphere(position=[0,70,150], velocity=[0,0,0], radius=100, color=[0,0,255]),
            Sphere(position=[150,0,-75], velocity=[0,0,0], radius=100, color=[0,255,0])
        ]

        self.last_render_t = datetime.now()

    def calculate_colors(self, xyz_coords, start_time):
        delta_t = (datetime.now() - self.last_render_t).total_seconds()
        delta_angle = delta_t * 5
        self.last_render_t = datetime.now()

        cos_angle = math.cos(delta_angle)
        sin_angle = math.sin(delta_angle)

        colors = np.zeros((self.NUM_LIGHTS, 3), dtype=np.uint8)
        for ball in self.balls:
            rotated_coords_x = ball.position[0] * cos_angle - ball.position[1] * sin_angle
            rotated_coords_y = ball.position[0] * sin_angle + ball.position[1] * cos_angle

            ball.position = np.array([rotated_coords_x, rotated_coords_y, ball.position[2]])
            ball.render(xyz_coords, colors)

        return colors

if __name__ == "__main__":
    coords_path = "./coordinates/sample_coords.csv"
    anim = MovingObjectExample(coords_path)

    anim.animation_loop()