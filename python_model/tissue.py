import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y  # each cell has a coordinate in 2D space


class Tissue(Cell):
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.n_cell = (
            x_size * y_size
        )  # initialise as many cells as points on the lattice
        self.lattice = np.empty(self.n_cell, dtype=object)
        self.Pm = 1  # the probability of movement per time step for each cell

        # load coordinates
        for i in range(self.n_cell):
            x = i // self.y_size
            y = i % self.x_size
            self.lattice[i] = Cell(x, y)

    def print_lattice(self):
        disp = np.empty((self.x_size, self.y_size), dtype=object)
        for i, cell in enumerate(self.lattice):
            x = i // self.y_size
            y = i % self.x_size
            disp[x, y] = (cell.x, cell.y)
        print(disp)

    def get_coords(self):
        # Extract coordinates from the lattice
        x_coords = []
        y_coords = []
        for cell in self.lattice:
            x_coords.append(cell.x)
            y_coords.append(cell.y)
        return np.array(x_coords), np.array(y_coords)

    def plot_tissue(self):
        x_coords, y_coords = self.get_coords()
        plt.scatter(x_coords, y_coords)
        plt.show()

    def diffuse(self):
        # keep track of which coordinates are occupied
        occupied_positions = {(cell.x, cell.y) for cell in self.lattice}
        for i, cell in enumerate(self.lattice):
            # Initialise proposal coordinates
            prop_x = cell.x
            prop_y = cell.y
            r1 = np.random.uniform(0, 1)
            # Simulate equal propensity in every direction, in 2D there are 4 possible directions
            # Therefore divide the probability space evenly by 4
            if 0 <= r1 < self.Pm / 4:
                prop_y += 1  # move up
            elif self.Pm / 4 <= r1 < self.Pm / 2:
                prop_x += 1  # move right
            elif self.Pm / 2 <= r1 < self.Pm / 2 + self.Pm / 4:
                prop_y -= 1  # move down
            elif self.Pm / 2 + self.Pm / 4 <= r1 <= 1:
                prop_x -= 1  # move left
            else:
                raise RuntimeError(
                    f"Unexpected condition encountered with r1 = {r1}. Check the probability logic."
                )

            # only one cell can occupy each coordinate at any timepoint
            if (prop_x, prop_y) not in occupied_positions:
                occupied_positions.remove((cell.x, cell.y))
                cell.x = prop_x
                cell.y = prop_y
                occupied_positions.add((cell.x, cell.y))


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
    s1 = Simulation(300, 50, 50)
    s1.run()
    # print(s1.frames)
    s1.animate()


runsim()
