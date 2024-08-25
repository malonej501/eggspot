import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

a = 2.8e-4
b = 5e-3
tau = 0.1
k = -0.005

size = 100  # size of the 2D grid
dx = 2.0 / size  # space step

T = 20.0  # total time
dt = 0.001  # time step
n = int(T / dt)  # number of iterations

U = np.random.rand(size, size)
V = np.random.rand(size, size)

frames = []


def laplacian(Z):
    Ztop = Z[0:-2, 1:-1]
    Zleft = Z[1:-1, 0:-2]
    Zbottom = Z[2:, 1:-1]
    Zright = Z[1:-1, 2:]
    Zcenter = Z[1:-1, 1:-1]
    return (Ztop + Zleft + Zbottom + Zright - 4 * Zcenter) / dx**2


step_plot = n // T
# We simulate the PDE with the finite difference
# method.
for i in range(n):
    # We compute the Laplacian of u and v.
    deltaU = laplacian(U)
    deltaV = laplacian(V)
    # We take the values of u and v inside the grid.
    Uc = U[1:-1, 1:-1]
    Vc = V[1:-1, 1:-1]
    # We update the variables.
    U[1:-1, 1:-1], V[1:-1, 1:-1] = (
        Uc + dt * (a * deltaU + Uc - Uc**3 - Vc + k),
        Vc + dt * (b * deltaV + Uc - Vc) / tau,
    )
    # Neumann conditions: derivatives at the edges
    # are null.
    for Z in (U, V):
        Z[0, :] = Z[1, :]
        Z[-1, :] = Z[-2, :]
        Z[:, 0] = Z[:, 1]
        Z[:, -1] = Z[:, -2]

    # We plot the state of the system at
    # 9 different times.
    if i % step_plot == 0 and i < T * step_plot:
        frames.append(U.copy())


fig, ax = plt.subplots()
cax = ax.matshow(
    U, cmap="viridis"
)  # initialise scatterplot for viewing, set size of points
frame_text = ax.text(
    0.05,
    0.95,
    "",
    transform=ax.transAxes,
    fontsize=12,
    verticalalignment="top",
)


def update_frame(frame):
    cax.set_array(frames[frame])
    frame_text.set_text(f"Frame: {frame + 1}/{len(frames)}")
    return [cax]


ani = animation.FuncAnimation(fig, update_frame, frames=len(frames), interval=100)
plt.show()
