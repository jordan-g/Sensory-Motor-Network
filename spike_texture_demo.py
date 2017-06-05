import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection
import matplotlib.animation as animation
from scipy.interpolate import interp1d

import plotting
import textures
import agent

# Set parameters
n_whiskers           = 50
n_sensory_cells      = 200
whisker_length       = 2
speed                = 0.01
total_whiskers_angle = np.deg2rad(160)
texture_length       = 50

# Create the texture
amplitude = 0.5
y_offset  = 1.5
phase     = 0
frequency = 5
texture = textures.SpikeTexture(amplitude, y_offset, phase, frequency)

# Create the agent
agent = agent.Agent(n_whiskers, whisker_length, total_whiskers_angle, n_sensory_cells)
agent.update_whisker_deflections(texture)

# Set up the animation plot
animation_plot = plotting.AnimationPlot(0, 0, texture_length, y_offset + amplitude)
animation_plot.create_animation_plot(0, 0, texture_length, y_offset + amplitude)
animation_plot.create_texture(texture, texture_length)
animation_plot.create_whiskers(n_whiskers)
animation_plot.create_whisker_deflection_plot(n_whiskers)
animation_plot.create_sensory_cell_activity_plot(n_sensory_cells)

def update(i):
    # Update the texture
    # texture.frequency = frequency*np.cos((speed/2)*i)
    # texture.T         = 2*np.pi/texture.frequency

    # Move the agent & update the whisker deflections
    agent.move(speed)
    if agent.x > texture_length:
        agent.x = 0
    agent.update_whisker_deflections(texture)

    # Update sensory cell weights to learn to match whisker deflections
    f = interp1d(range(n_whiskers), agent.whiskers.deflections)
    target_cell_activity = f(np.linspace(0, n_whiskers-1, n_sensory_cells))
    agent.sensory_cells.update_weights(target_cell_activity)

    return texture, agent

# Start the animation
animation_plot.animate(update_func=update)