import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import messagebox
import random

#Create ODE matrix
def simple_pendulum(t, y, g, L):
    theta, omega = y
    dydt = [omega, -(g / L) * np.sin(theta)]
    return dydt

#Update graph
def update(frame, line, pendulum_params, time_line, angle_line):
    t = pendulum_params['times'][frame]
    angles = pendulum_params['angles']
    line.set_data([0, np.sin(angles[frame])], [0, -np.cos(angles[frame])])

    time_line.set_data(pendulum_params['times'][:frame], angles[:frame])
    angle_line.set_data([t, t], [0, angles[frame]])

    return line, time_line, angle_line

#Recieve value, solve the equation and Create graph
def simulate_simple_pendulum(initial_conditions, total_time, g, L):
    solution = solve_ivp(
        fun=lambda t, y: simple_pendulum(t, y, g, L),
        t_span=(0, total_time),
        y0=initial_conditions,
        t_eval=np.linspace(0, total_time, 500)
    )

    times = solution.t
    angles = solution.y[0]

    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]}, figsize=(10, 8))

    fig.suptitle('Mini Project : Simple Pendulum Simulation', fontsize=18)

    ax1.set_xlim(-1.5, 1.5)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_aspect('equal', adjustable='box')
    ax1.set_xlabel('X-axis')
    ax1.set_ylabel('Y-axis')

    line, = ax1.plot([], [], 'o-', color='g', markersize=8, lw=2)

    pendulum_params = {'times': times, 'angles': angles}

    time_line, = ax2.plot([], [], label='Angular Displacement vs. Time', color='b', lw=2)
    angle_line, = ax2.plot([], [], 'r--', label='Current Angle', lw=2)

    ax2.set_xlim(0, total_time)
    ax2.set_ylim(-max((abs(angles)) + 0.1), max(abs(angles)) + 0.1)  # Adjusted y-axis limits
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Angular Displacement (rad)')
    ax2.legend()

    # Beautify the graphs
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend(loc='upper right')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    ani = FuncAnimation(
        fig, update, frames=len(times),
        fargs=(line, pendulum_params, time_line, angle_line),
        interval=50, blit=True
    )

    plt.show()

#Random values
def randomize_values():
    theta_entry.delete(0, tk.END)
    theta_entry.insert(0, str(random.uniform(0, 90)))
    
    omega_entry.delete(0, tk.END)
    omega_entry.insert(0, str(random.uniform(-5, 5)))
    
    total_time_entry.delete(0, tk.END)
    total_time_entry.insert(0, str(random.uniform(5, 15)))
    
    g_entry.delete(0, tk.END)
    g_entry.insert(0, str(random.uniform(9.5, 10.5)))
    
    L_entry.delete(0, tk.END)
    L_entry.insert(0, str(random.uniform(0.5, 1.5)))

#Sent input values or Error messages
def on_submit():
    try:
        initial_conditions = [np.radians(float(theta_entry.get())), float(omega_entry.get())]
        total_time = float(total_time_entry.get())
        acceleration_due_to_gravity = float(g_entry.get())
        pendulum_length = float(L_entry.get())
            
        simulate_simple_pendulum(initial_conditions, total_time, acceleration_due_to_gravity, pendulum_length)
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numerical values.")

# Create Tkinter GUI window
root = tk.Tk()
root.title("Simple Pendulum Simulation")

# Create input fields and labels
tk.Label(root, text="Initial Angle (degrees):").grid(row=0, column=0, padx=5, pady=5)
theta_entry = tk.Entry(root)
theta_entry.grid(row=0, column=1, padx=5, pady=5)
theta_entry.insert(0, "30")  # Default value

tk.Label(root, text="Initial Angular Velocity (rad/s):").grid(row=1, column=0, padx=5, pady=5)
omega_entry = tk.Entry(root)
omega_entry.grid(row=1, column=1, padx=5, pady=5)
omega_entry.insert(0, "0")  # Default value

tk.Label(root, text="Total Time (s):").grid(row=2, column=0, padx=5, pady=5)
total_time_entry = tk.Entry(root)
total_time_entry.grid(row=2, column=1, padx=5, pady=5)
total_time_entry.insert(0, "10")  # Default value

tk.Label(root, text="Gravity (m/s^2):").grid(row=3, column=0, padx=5, pady=5)
g_entry = tk.Entry(root)
g_entry.grid(row=3, column=1, padx=5, pady=5)
g_entry.insert(0, "9.81")  # Default value

tk.Label(root, text="Pendulum Length (m):").grid(row=4, column=0, padx=5, pady=5)
L_entry = tk.Entry(root)
L_entry.grid(row=4, column=1, padx=5, pady=5)
L_entry.insert(0, "1.0")  # Default value

# Create randomize button
randomize_btn = tk.Button(root, text="Randomize", command=randomize_values)
randomize_btn.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Create submit button
submit_btn = tk.Button(root, text="Submit", command=on_submit)
submit_btn.grid(row=6, column=0, columnspan=2, padx=5, pady=10)

root.mainloop()