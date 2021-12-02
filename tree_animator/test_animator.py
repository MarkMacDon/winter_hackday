import matplotlib.pyplot as plt

from tree_animator.animator import LightsAnimator


class TestAnimator(LightsAnimator):
    def __init__(self, coords_path=None):
        # call the parent
        super().__init__(coords_path=coords_path)

        # initiate the mat plot lib figure
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection = '3d')
        self.plot_data = self.ax.scatter(self._xyz_coords[:,0], self._xyz_coords[:,1], self._xyz_coords[:,2])

        # make the panes transparent
        self.ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        self.ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        # make the grid lines transparent
        self.ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        self.ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        self.ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)

    def _render_colors(self, colors):
        self.plot_data.set_color(colors/255.0)

        # render the update to the matplotlib window
        plt.pause(1/60.0)

    def finalize_animation(self):
        plt.close()