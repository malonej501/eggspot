import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tissue import Tissue


class Simulation(Tissue):

    def __init__(self, t_max, x_size, y_size):
        self.t_max = t_max
        self.tissue = Tissue(x_size, y_size)  # initialise the tissue already
        # for animating the tissue
        self.frames = np.zeros((self.t_max, 2, self.tissue.n_cell))
        self.fig, self.ax = plt.subplots()
        self.scat = self.ax.scatter([], [])

    def run(self):
        # diffuse the cells for t_max iterations
        for t in range(self.t_max):
            # self.tissue.plot_tissue()
            x_coords, y_coords = self.tissue.get_coords()
            # Store coordinates in 3D array, where each element is a 2D array containing x and y coordinate array for each timepoint
            self.frames[t, 0, :] = x_coords
            self.frames[t, 1, :] = y_coords
            self.tissue.diffuse()

    def update_frame(self, frame):
        x_coords = self.frames[frame, 0, :]
        y_coords = self.frames[frame, 1, :]

        self.scat.set_offsets(np.column_stack((x_coords, y_coords)))

        # Update axis limits to fit data
        self.ax.set_xlim(np.min(x_coords) - 1, np.max(x_coords) + 1)
        self.ax.set_ylim(np.min(y_coords) - 1, np.max(y_coords) + 1)

        return (self.scat,)

    def animate(self):
        ani = animation.FuncAnimation(
            fig=self.fig,
            func=self.update_frame,
            frames=self.t_max,
            interval=100,
        )
        plt.show()


def runsim():
    s1 = Simulation(300, 80, 80)
    s1.run()
    # print(s1.frames)
    s1.animate()


runsim()
