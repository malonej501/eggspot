import numpy as np


class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y  # each cell has a coordinate in 2D space
        self.nbhd_dist = 20
        self.Pm = 1  # the probability of movement per time step for each cell

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

    def calculate_energy(self, pos, nbhd):
        """Calculate the energy of a position based on its neighbouring cells"""
        total_energy = 0
        for n in nbhd:
            dist = np.linalg.norm(np.array(pos) - np.array(n))
            if dist > 0:  # Avoid division by zero
                total_energy += 1 * dist  # Energy is proportional to distance
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

            # Find the move with the minimum energy
            best_move = min(energy_for_moves, key=energy_for_moves.get)

            (prop_x, prop_y) = moves[best_move]

        return prop_x, prop_y


class Iridophore(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)

    # def activate(self):
    #     # iridophores diffuse but also attract themselves, therefore need a different movement function
    #     prop_x = self.x
    #     prop_y = self.y


class Xanthophore(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
