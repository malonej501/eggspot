import numpy as np


class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y  # each cell has a coordinate in 2D space
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


# class Iridophore(Cell):
#     def __init__(self, x, y,)
