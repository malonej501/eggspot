import numpy as np
import matplotlib.pyplot as plt
from cell import Cell


class Tissue(Cell):
    def __init__(self, n_cell):
        self.n_cell = n_cell
        self.cells = np.empty(self.n_cell, dtype=object)

        self.initialise_cell_placement_gaussian()

    def initialise_cell_placement_gaussian(self):
        center = 0
        stdev = (
            self.n_cell / 10
        )  # set the stdev of the gaussian to 1/4 the number of cells to be initialised
        occupied_positions = set()
        while len(occupied_positions) < self.n_cell:
            x, y = np.random.normal(loc=0, scale=self.n_cell / 4, size=2)
            if (x, y) not in occupied_positions:
                occupied_positions.add((x, y))
                self.cells[len(occupied_positions) - 1] = Cell(x, y)

    def get_coords(self):
        # Extract coordinates from the cells
        x_coords = []
        y_coords = []
        for cell in self.cells:
            x_coords.append(cell.x)
            y_coords.append(cell.y)
        return np.array(x_coords), np.array(y_coords)

    def plot_tissue(self):
        x_coords, y_coords = self.get_coords()
        plt.scatter(x_coords, y_coords)
        plt.show()

    def update(self):
        # keep track of which coordinates are occupied
        occupied_positions = {(cell.x, cell.y) for cell in self.cells}
        for i, cell in enumerate(self.cells):
            prop_x, prop_y = cell.diffuse()
            # # Initialise proposal coordinates
            # prop_x = cell.x
            # prop_y = cell.y
            # r1 = np.random.uniform(0, 1)
            # # Simulate equal propensity in every direction, in 2D there are 4 possible directions
            # # Therefore divide the probability space evenly by 4
            # if 0 <= r1 < self.Pm / 4:
            #     prop_y += 1  # move up
            # elif self.Pm / 4 <= r1 < self.Pm / 2:
            #     prop_x += 1  # move right
            # elif self.Pm / 2 <= r1 < self.Pm / 2 + self.Pm / 4:
            #     prop_y -= 1  # move down
            # elif self.Pm / 2 + self.Pm / 4 <= r1 <= 1:
            #     prop_x -= 1  # move left
            # else:
            #     raise RuntimeError(
            #         f"Unexpected condition encountered with r1 = {r1}. Check the probability logic."
            #     )

            # only one cell can occupy each coordinate at any timepoint
            if (prop_x, prop_y) not in occupied_positions:
                occupied_positions.remove((cell.x, cell.y))
                cell.x = prop_x
                cell.y = prop_y
                occupied_positions.add((cell.x, cell.y))
