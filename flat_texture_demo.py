import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection
import matplotlib.animation as animation

import plotting
import textures
import agent

# Set parameters
n_whiskers           = 50
whisker_length       = 2
speed                = 0.01
total_whiskers_angle = np.deg2rad(160)
texture_length       = 50

# Create the texture
y_offset  = 1.5
texture = textures.FlatTexture(y_offset)

# Create the agent
agent = agent.Agent(n_whiskers, whisker_length, total_whiskers_angle)
agent.update_whisker_deflections(texture)

# Set up the animation plot
animation_plot = plotting.AnimationPlot(0, 0, texture_length, y_offset)
animation_plot.create_texture(texture, texture_length)
animation_plot.create_whiskers(n_whiskers)

def update(i):
    # Move the agent & update the whisker deflections
    agent.move(speed)
    agent.update_whisker_deflections(texture)

    return texture, agent

# Start the animation
animation_plot.animate(update_func=update)