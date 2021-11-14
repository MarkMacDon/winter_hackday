from datetime import datetime

import numpy as np

from tree_animator import TreeAnimator


class CenterExplodingExample(TreeAnimator):
    def initialize_animation(self):
        self.explode_distance = 0.01

    def calculate_colors(self, xyz_coords, start_time):
        # we have an expanding radius of light, self.explode_distance
        # set any light outside the radius to black, anything inside to color
        # each loop the radius will get bigger

        # calculate the distance from the center
        distance_from_center = np.linalg.norm(xyz_coords, axis=1)
        # normalize the distance into the range 0-1
        distance_from_center /= distance_from_center.max()

        # create an array of colors, and initialize it to black (zeros)
        colors = np.zeros((self.NUM_LIGHTS, 3), dtype=np.uint8)

        # for each light, if it is inside the exploding radius, set its color
        for i in range(self.NUM_LIGHTS):
            if distance_from_center[i] < self.explode_distance:
                # at the edge of the explosion radius, the color is bright, and at the center is dark.
                # calculate how close is this light from the exposions edge, 1 at the edge, 0 at the center
                color_dist = np.clip(distance_from_center[i] / self.explode_distance, 0, 1)
                # color_dist is in the range 0-1, times by 255 to get it back into the color range, remove half the red just because
                colors[i] = np.array([color_dist/2, color_dist, color_dist]) * 255

        # update the exposion distance, so that we have it making a full cycle once every 3 seconds
        num_seconds_since_start = (datetime.now() - start_time).total_seconds()
        self.explode_distance = (num_seconds_since_start / 3) % 1.0

        return colors

if __name__ == "__main__":
    coords_path = "../data/coords.csv"
    anim = CenterExplodingExample(coords_path)

    anim.animation_loop()