import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tissue import Tissue


class Simulation:

    def __init__(self, t_max, n_cell, view=None):
        self.t_max = t_max
        self.tissue = Tissue(n_cell)  # initialise the tissue already
        # for animating the tissue
        self.frames = np.zeros((self.t_max, 2, self.tissue.n_cell))
        self.fig, self.ax = plt.subplots()
        self.scat = self.ax.scatter(
            [], [], s=3
        )  # initialise scatterplot for viewing, set size of points
        self.frame_text = self.ax.text(
            0.05,
            0.95,
            "",
            transform=self.ax.transAxes,
            fontsize=12,
            verticalalignment="top",
        )
        self.view = view  # fix the axes limits or adapt to spread of cells

    def run(self):
        # diffuse the cells for t_max iterations
        for t in range(self.t_max):
            # self.tissue.plot_tissue()
            x_coords, y_coords = self.tissue.get_coords()
            # Store coordinates in 3D array, where each element is a 2D array containing x and y coordinate array for each timepoint
            self.frames[t, 0, :] = x_coords
            self.frames[t, 1, :] = y_coords
            self.tissue.update()

    def update_frame(self, frame):
        x_coords = self.frames[frame, 0, :]
        y_coords = self.frames[frame, 1, :]

        self.scat.set_offsets(np.column_stack((x_coords, y_coords)))

        if self.view == "tight":
            # Update axis limits to fit data
            self.ax.set_xlim(np.min(x_coords) - 1, np.max(x_coords) + 1)
            self.ax.set_ylim(np.min(y_coords) - 1, np.max(y_coords) + 1)
        if self.view is None:
            self.ax.set_xlim(-500, 500)
            self.ax.set_ylim(-500, 500)

        # Update frame counter text
        self.frame_text.set_text(f"Frame: {frame + 1}/{self.t_max}")

        return (self.scat, self.frame_text)

    def animate(self):
        ani = animation.FuncAnimation(
            fig=self.fig,
            func=self.update_frame,
            frames=self.t_max,
            interval=100,
        )
        plt.show()


def runsim():
    s1 = Simulation(t_max=300, n_cell=300, view="tight")
    s1.run()
    # print(s1.frames)
    s1.animate()


runsim()
