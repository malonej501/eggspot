import numpy as np
import matplotlib.pyplot as plt


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
