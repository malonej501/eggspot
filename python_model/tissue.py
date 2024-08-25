import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
from cell import Cell


class Tissue:
    def __init__(self, n_cell):
        self.n_cell = n_cell
        self.cells = np.empty(self.n_cell, dtype=object)

        self.initialise_cell_placement_gaussian()

    def initialise_cell_placement_gaussian(self):
        center = 0
        stdev = (
            self.n_cell / 20
        )  # set the stdev of the gaussian to 1/4 the number of cells to be initialised
        occupied_positions = set()
        while len(occupied_positions) < self.n_cell:
            x, y = np.random.normal(loc=0, scale=self.n_cell / 4, size=2)
            x, y = np.round(x).astype(int), np.round(y).astype(int)
            if (x, y) not in occupied_positions:
                occupied_positions.add((x, y))
                self.cells[len(occupied_positions) - 1] = Cell(x, y)

    def get_cell_neighbourhood(self, cell, occupied_positions, nbhd_dist):
        """get coords of other cells within nbhd_dist radius efficiently with KDTree"""
        # Convert the positions to a list of coordinates
        pos_list = list(occupied_positions)

        # Build a k-d tree
        tree = KDTree(pos_list)

        # Query the tree for neighbours within the given distance
        indices = tree.query_ball_point([cell.x, cell.y], nbhd_dist)

        # Extract the corresponding positions
        nbhd = [pos_list[i] for i in indices if pos_list[i] != (cell.x, cell.y)]

        return nbhd

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
            nbhd = self.get_cell_neighbourhood(cell, occupied_positions, cell.nbhd_dist)
            prop_x, prop_y = cell.diffuse()
            prop_x, prop_y = cell.find_best_move(prop_x, prop_y, nbhd)

            # only one cell can occupy each coordinate at any timepoint
            if (prop_x, prop_y) not in nbhd:
                occupied_positions.remove((cell.x, cell.y))
                cell.x = prop_x
                cell.y = prop_y
                occupied_positions.add((cell.x, cell.y))

            new_x, new_y = cell.divide()

            if new_x and new_y and (new_x, new_y) not in nbhd:
                self.cells = np.append(self.cells, Cell(new_x, new_y))
                occupied_positions.add((new_x, new_y))
                self.n_cell += 1
