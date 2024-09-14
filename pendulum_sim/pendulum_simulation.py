# system imports
import math

# library imports
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# dynamic constants
mass = 1 # mass of ball g   
g = 9.81  # gravitational acceleration (m/s^2)
L = 1.0   # length of the pendulum (m)
gamma = 1 # damping coefficient
force_mag = 10
force_frequency = 1

process_noise_variance = 0.01
measurement_noise_variance = 0.01

simulation_time = 10 #s
force_simulation_time = 20 #s
dt = 0.05 # 50 ms
measurement_hz = 1

Q = dt * np.array([[process_noise_variance, 0],
                   [ 0, process_noise_variance]])

# Define the pendulum dynamics function
def pendulum_dynamics(y, t, g, L, gamma, force_mag, force_frequency, external_force=False):

    theta, omega = y
    dtheta_dt = omega

    if not external_force:
        domega_dt = - (g / L) * np.sin(theta) - (gamma/mass) * omega

    else:
        domega_dt = - (g / L) * np.sin(theta) - (gamma/mass) * omega + force_mag * np.cos(2 * np.pi * force_frequency * t)

    return [ dtheta_dt, domega_dt ]


if __name__ == "__main__":

    # Initial conditions
    y0 = [np.pi / 4, 0]  # Initial angle (45 degrees) and initial angular velocity (0)

    # Time array
    t = np.arange(0, simulation_time, dt)

    # Solve the ODE 
    solution = odeint(pendulum_dynamics, y0, t, args=(g, L, gamma, force_mag, force_frequency, True))

    # Extract the results
    theta = solution[:, 0]  # Angle theta
    theta_dot = solution[:, 1]  # Angular velocity

    # Add process noise to the results
    theta_noisy = theta + np.random.normal(0, math.sqrt(process_noise_variance), len(theta))
    theta_dot_noisy = theta_dot + np.random.normal(0, math.sqrt(process_noise_variance), len(theta_dot))

    # Plot the results
    plt.figure(figsize=(12, 6))
    plt.plot(t, theta, label='Theta (angle)')
    plt.plot(t, theta_dot, label='Theta_dot (angular velocity)', linestyle='--')
    plt.xlabel('Time (s)')
    plt.ylabel('Value')
    plt.title('Pendulum: Theta and Theta Dot')
    plt.legend()
    plt.grid()
    plt.show()

    # Convert theta to Cartesian coordinates for animation
    x = L * np.sin(theta)
    y = -L * np.cos(theta)

    # Create figure and axis
    fig, ax = plt.subplots()

    # Set axis limits
    ax.set_xlim(-L - 1, L + 1)
    ax.set_ylim(-L - 1, 1)

    # Create pendulum arm and bob (pre-allocate)
    line, = ax.plot([], [], color='blue', label='Pendulum Arm')  # Line for the arm
    circle = plt.Circle((0, -L), 0.075, color='red', label='Pendulum Ball')  # Circle for the bob
    ax.add_patch(circle)
    ax.legend(loc='upper left')

    # Initialize the plot elements (rod and bob)
    def init():
        line.set_data([], [])
        circle.set_center((0, -L))  # Set initial position of the circle (bob)
        return line, circle

    # Update function for animation
    def update(i):
        line.set_data([0, x[i]], [0, y[i]])  # Update the pendulum arm
        circle.set_center((x[i], y[i]))  # Update the pendulum bob
        return line, circle

    # Create the animation
    ani = FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval=50, repeat=True)

    # Display the animation
    plt.show()
