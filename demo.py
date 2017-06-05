import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection
import matplotlib.animation as animation
from scipy.interpolate import interp1d

import plotting
import textures
import agent

texture_type = input("What type of texture? (sine/spike/square/flat) : ")

# Set parameters
n_whiskers                  = 15
n_sensory_cells             = 100
min_whisker_length          = 1
max_whisker_length          = 3
speed                       = 0.01
total_whiskers_angle        = np.deg2rad(135)
sensory_cells_learning_rate = 0.01
mean_whisking_angle         = np.pi
whisking_angle_amplitude    = np.pi/2
whisking_speed              = 0.05

# Create the texture
if texture_type == "sine" or texture_type == "":
    texture_length = 50
    amplitude      = 0.5
    y_offset       = 1.0
    phase          = 0
    frequency      = 5
    texture = textures.SineTexture(amplitude, y_offset, phase, frequency)
elif texture_type == "spike":
    texture_length = 50
    amplitude      = 0.5
    y_offset       = 1.0
    phase          = 0
    frequency      = 5
    texture = textures.SpikeTexture(amplitude, y_offset, phase, frequency)
elif texture_type == "square":
    texture_length = 50
    amplitude      = 0.5
    y_offset       = 1.0
    phase          = 0
    frequency      = 5
    texture = textures.SquareTexture(amplitude, y_offset, phase, frequency)
elif texture_type == "flat":
    texture_length = 50
    amplitude      = 0
    y_offset       = 1.0
    texture = textures.FlatTexture(y_offset)
else:
    raise ValueError("Invalid texture type provided.")

# Create the agent
agent = agent.Agent(n_whiskers, min_whisker_length, max_whisker_length, total_whiskers_angle, n_sensory_cells, sensory_cells_learning_rate)
agent.update_whisker_deflections(texture)

# Set up the animation plot
animation_plot = plotting.AnimationPlot(0, 0, texture_length, y_offset + amplitude)
animation_plot.create_animation_plot(0, 0, texture_length, y_offset + amplitude)
animation_plot.create_texture(texture, texture_length)
animation_plot.create_whiskers(n_whiskers)
animation_plot.create_whisker_deflection_plot(n_whiskers)
animation_plot.create_sensory_cell_activity_plot(n_sensory_cells)

def update(i):
    # Move the agent & update the whisker deflections
    agent.move(speed)
    if agent.x > texture_length:
        agent.x = 0
    agent.update_whisker_deflections(texture)

    # Update the whisking angle
    whisking_angle = mean_whisking_angle + whisking_angle_amplitude*np.sin(np.sin(whisking_speed*i))
    agent.update_whisking_angle(whisking_angle)

    # Update sensory cell weights to learn to match whisker deflections
    f = interp1d(range(n_whiskers), agent.whiskers.deflections)
    target_cell_activity = f(np.linspace(0, n_whiskers-1, n_sensory_cells))
    agent.sensory_cells.update_weights(target_cell_activity)

    return texture, agent

# Start the animation
animation_plot.animate(update_func=update)