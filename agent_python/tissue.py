import numpy as np
from scipy.spatial import KDTree
import matplotlib.pyplot as plt
from cell import Cell, Iridophore, Xanthophore, Melanophore, Erythrophore


class Tissue:
    def __init__(self, n_cell):
        self.n_cell = n_cell
        self.cells = np.empty(self.n_cell, dtype=object)

        self.initialise_cell_placement_gaussian()

    def pos_occupied(self, occupied_positions, x, y):
        """Check if the position (x, y) is occupied by any cell type."""
        return any(pos[0] == x and pos[1] == y for pos in occupied_positions)

    def initialise_cell_placement_gaussian(self):
        center = 0
        stdev = (
            self.n_cell / 20
        )  # set the stdev of the gaussian to 1/4 the number of cells to be initialised
        occupied_positions = set()
        while len(occupied_positions) < self.n_cell:
            r1 = np.random.uniform(0, 1)  # decide cell type
            x, y = np.random.normal(loc=0, scale=self.n_cell / 4, size=2)
            x, y = np.round(x).astype(int), np.round(y).astype(int)
            if not self.pos_occupied(occupied_positions, x, y):
                if r1 < 0.25:
                    self.cells[len(occupied_positions) - 1] = Iridophore(
                        x, y
                    )  # add iridophores
                    occupied_positions.add((x, y, type(Iridophore)))
                elif 0.25 <= r1 < 0.5:
                    self.cells[len(occupied_positions) - 1] = Xanthophore(x, y)
                    occupied_positions.add((x, y, type(Xanthophore)))
                elif 0.5 <= r1 < 0.75:
                    self.cells[len(occupied_positions) - 1] = Melanophore(x, y)
                    occupied_positions.add((x, y, type(Xanthophore)))
                elif 0.7 <= r1:
                    self.cells[len(occupied_positions) - 1] = Erythrophore(x, y)
                    occupied_positions.add((x, y, type(Xanthophore)))

    def get_cell_neighbourhood(self, cell, occupied_positions, nbhd_dist):
        """get coords of other cells within nbhd_dist radius efficiently with KDTree"""
        # Convert the positions to a list of coordinates
        pos_list = [(x, y) for x, y, _ in occupied_positions]

        # Build a k-d tree
        tree = KDTree(pos_list)

        # Query the tree for neighbours within the given distance
        indices = tree.query_ball_point([cell.x, cell.y], nbhd_dist)

        # Extract the corresponding full tuples from occupied_positions
        nbhd = [
            pos
            for pos in occupied_positions
            if (pos[0], pos[1]) in [pos_list[i] for i in indices]
        ]

        # Exclude the cell itself from its own neighbourhood
        nbhd = [pos for pos in nbhd if (pos[0], pos[1]) != (cell.x, cell.y)]

        return nbhd

    def get_coords(self):
        # Extract coordinates from the cells
        x_coords = []
        y_coords = []
        cell_types = []
        for cell in self.cells:
            x_coords.append(cell.x)
            y_coords.append(cell.y)
            cell_types.append(type(cell))
        return np.array(x_coords), np.array(y_coords), np.array(cell_types)

    def plot_tissue(self):
        x_coords, y_coords = self.get_coords()
        plt.scatter(x_coords, y_coords)
        plt.show()

    def update(self):
        # keep track of which coordinates are occupied
        occupied_positions = {(cell.x, cell.y, type(cell)) for cell in self.cells}
        for i, cell in enumerate(self.cells):
            nbhd = self.get_cell_neighbourhood(cell, occupied_positions, cell.nbhd_dist)
            prop_x, prop_y = cell.diffuse()
            prop_x, prop_y = cell.find_best_move(prop_x, prop_y, nbhd)

            # only move cell if proposed position is unoccupied
            if not self.pos_occupied(nbhd, prop_x, prop_y):
                occupied_positions.remove((cell.x, cell.y, type(cell)))
                cell.x = prop_x
                cell.y = prop_y
                occupied_positions.add((cell.x, cell.y, type(cell)))

            division, new_x, new_y, new_cell_type = cell.divide()

            if division:  # only add cells if a division occurs
                if not self.pos_occupied(
                    nbhd, new_x, new_y
                ):  # only add new cell if the proposed position is unoccupied
                    self.cells = np.append(self.cells, new_cell_type(new_x, new_y))
                    occupied_positions.add((new_x, new_y, new_cell_type))
                    self.n_cell += 1
                # if self.pos_occupied(nbhd, new_x, new_y):

            # adjust cell positions to ensure one cell per site
            # while
