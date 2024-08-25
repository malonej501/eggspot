import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from tissue import Tissue
from cell import Xanthophore, Iridophore, Melanophore, Erythrophore


class Simulation:

    def __init__(self, t_max, n_cell, view="fixed"):
        self.t_max = t_max
        self.tissue = Tissue(n_cell)  # initialise the tissue already
        # for animating the tissue
        self.frames = []
        self.fig, self.ax = plt.subplots()
        self.scat = self.ax.scatter(
            [], [], c=[], s=3
        )  # initialise scatterplot for viewing, set size of points
        self.color_map = {
            Iridophore: "blue",
            Xanthophore: "red",
            Melanophore: "black",
            Erythrophore: "orange",
        }
        self.ax.legend(
            handles=[
                mpatches.Patch(color="blue", label="Iridophore"),
                mpatches.Patch(color="red", label="Xanthophore"),
                mpatches.Patch(color="black", label="Melanophore"),
                mpatches.Patch(color="orange", label="Erythrophore"),
            ],
            loc="upper right",
        )
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
            print(f"Frame: {t}\tn_cell: {self.tissue.n_cell}")
            # self.tissue.plot_tissue()
            x_coords, y_coords, cell_types = self.tissue.get_coords()
            # Store coordinates and cell types in a list of tuples
            self.frames.append((x_coords, y_coords, cell_types))
            self.tissue.update()

    def update_frame(self, frame):
        x_coords, y_coords, cell_types = self.frames[
            frame
        ]  # retrieve coordinates and cell types for current frame

        self.scat.set_offsets(np.column_stack((x_coords, y_coords)))
        self.scat.set_color(
            np.array([self.color_map[cell_type] for cell_type in cell_types])
        )

        if self.view == "tight":
            # Update axis limits to fit data
            self.ax.set_xlim(np.min(x_coords) - 1, np.max(x_coords) + 1)
            self.ax.set_ylim(np.min(y_coords) - 1, np.max(y_coords) + 1)
        if self.view == "fixed":
            self.ax.set_xlim(-200, 200)
            self.ax.set_ylim(-200, 200)

        # Update frame counter text
        self.frame_text.set_text(
            f"Frame: {frame + 1}/{self.t_max}\nNo. cells: {len(cell_types)}"
        )

        return (self.scat, self.frame_text)

    def animate(self):
        ani = animation.FuncAnimation(
            fig=self.fig,
            func=self.update_frame,
            frames=self.t_max,
            interval=100,
        )
        plt.show()
        writer = animation.PillowWriter(
            fps=15, metadata=dict(artist="Me"), bitrate=1800
        )
        ani.save("Frames.gif", writer=writer)


def runsim():
    s1 = Simulation(t_max=200, n_cell=200, view="fixed")
    s1.run()
    # print(s1.frames)
    s1.animate()


runsim()
