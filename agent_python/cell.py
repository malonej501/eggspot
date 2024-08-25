import numpy as np


class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y  # each cell has a coordinate in 2D space
        self.nbhd_dist = 20
        self.Pm = 1  # the probability of movement per time step for each cell
        self.Pr = 0.007  # the probability of division per time step per cell

    def diffuse(self):
        """Propose new coordinates"""
        # Initialise proposal coordinates
        prop_x = self.x
        prop_y = self.y
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
        return prop_x, prop_y

    def divide(self):
        """Spawn a new cell ajacent with given proability"""
        r1 = np.random.uniform(0, 1)

        new_x, new_y, new_cell_type = None, None, None
        division = False

        if r1 < self.Pr:
            division = True
            if 0 <= r1 < self.Pr / 4:  # spawn up
                new_x = self.x
                new_y = self.y + 1
            elif self.Pr / 4 <= r1 < self.Pr / 2:  # spawn right
                new_x = self.x + 1
                new_y = self.y
            elif self.Pr / 2 <= r1 < self.Pr / 2 + self.Pr / 4:  # spawn down
                new_x = self.x
                new_y = self.y - 1
            elif self.Pr / 2 + self.Pr / 4 <= r1 <= 1:  # spawn left
                new_x = self.x - 1
                new_y = self.y

            new_cell_type = type(
                self
            )  # parent cells can only create cells of the same type

        return division, new_x, new_y, new_cell_type

    def calculate_energy(self, pos, nbhd):
        """Calculate the energy of a position based on its neighbouring cells - default behaviour"""
        total_energy = 0
        return total_energy

    def find_best_move(self, prop_x, prop_y, nbhd):
        """Determine the best move that minimizes energy in a neighborhood."""

        # Only move if there are cells in the neighbourhood
        if nbhd:
            # Possible moves: (dx, dy)
            moves = {
                "up": (prop_x, prop_y + 1),
                "down": (prop_x, prop_y - 1),
                "right": (prop_x + 1, prop_y),
                "left": (prop_x - 1, prop_y),
            }

            # Calculate the energy for each move
            energy_for_moves = {}
            for direction, new_position in moves.items():
                energy_for_moves[direction] = self.calculate_energy(new_position, nbhd)
            # print(energy_for_moves.get)
            if any(
                value != 0 for value in energy_for_moves.values()
            ):  # only move if the calculate energy is greater than 0
                # Find the move with the minimum energy
                best_move = min(energy_for_moves, key=energy_for_moves.get)

                (prop_x, prop_y) = moves[best_move]

        return prop_x, prop_y


class Iridophore(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)

    def calculate_energy(self, pos, nbhd):
        """Calculate the energy of a position based on its neighbouring cells"""
        total_energy = 0
        for n in nbhd:
            if n[2] == type(self):  # only include other iridophores in the calculation
                dist = np.linalg.norm(np.array(pos) - np.array((n[0], n[1])))
                if dist > 0:  # Avoid division by zero
                    total_energy += 1 * dist  # Energy is proportional to distance
        return total_energy


class Xanthophore(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)

    def calculate_energy(self, pos, nbhd):
        """Calculate the energy of a position based on its neighbouring cells"""
        total_energy = 0
        for n in nbhd:
            # if n[2] == Melanophore or n[2] == Erythrophore:  # interacts with M and E
            #     dist = np.linalg.norm(np.array(pos) - np.array((n[0], n[1])))
            #     if dist > 0:  # Avoid division by zero
            #         total_energy += 1 / dist  # Energy is proportional to distance
            if n[2] == Iridophore:  # interacts with I
                dist = np.linalg.norm(np.array(pos) - np.array((n[0], n[1])))
                if dist > 0:  # Avoid division by zero
                    total_energy += 1 * dist  # Energy is proportional to distance
        return total_energy


class Melanophore(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)

    def calculate_energy(self, pos, nbhd):
        total_energy = 0
        for n in nbhd:
            if n[2] == Iridophore:  # interacts with I
                dist = np.linalg.norm(np.array(pos) - np.array((n[0], n[1])))
                if dist > 0:  # Avoid division by zero
                    total_energy += 1 / dist  # Energy is proportional to distance
        return total_energy


class Erythrophore(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)

    def calculate_energy(self, pos, nbhd):
        total_energy = 0
        for n in nbhd:
            if n[2] == Iridophore:
                dist = np.linalg.norm(np.array(pos) - np.array((n[0], n[1])))
                if dist > 0:
                    total_energy += 1 / dist
        return total_energy
