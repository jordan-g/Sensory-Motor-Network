import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection
import matplotlib.animation as animation

class AnimationPlot:
    def __init__(self, x_min, y_min, x_max, y_max):
        # Create the figure & axis
        self.figure = plt.figure(figsize=((x_max - x_min)/(y_max - y_min), 1))
        self.axis = plt.Axes(self.figure, [0, 0, 1, 1])
        self.figure.add_axes(self.axis)
        self.axis.set_axis_off()
        self.axis.set_xlim(x_min, x_max)
        self.axis.set_ylim(x_min - 1, y_max + 1)

    def create_texture(self, texture, texture_length):
        # Create texture x values
        self.texture_x = np.linspace(0, texture_length, 100*texture_length)
        
        # Plot the texture
        self.texture_line, = self.axis.plot([], [], color='#5C5C5C', lw=1)

    def create_whiskers(self, n_whiskers):
        # Initialize the list of whisker lines & colors
        # Note: colors are initialized to span the range (0, 1) in order to set the correct max & min for the subsequent animation
        self.whisker_lines = [[(0, 0), (0, 0)]]*n_whiskers
        self.whisker_colors = np.linspace(0, 1, n_whiskers)

        # Create a line collection from the whisker lines & colors
        self.whisker_line_collection = LineCollection(self.whisker_lines, array=self.whisker_colors, cmap=cm.rainbow, lw=0.5)
        self.axis.add_collection(self.whisker_line_collection)

    def update_plot(self, i):
        # Call the update function to update the agent and/or texture
        texture, agent = self.update_func(i)

        # Update texture y values
        texture_y = texture.value(self.texture_x)

        # Update whisker lines
        for n in range(agent.n_whiskers):
            # Get the whisker angle & deflection amount
            whisker_angle = agent.whiskers.whisker_angles[n]
            deflection    = agent.whiskers.deflections[n]

            # Set starting x & y coordinates of the whisker
            y_start = 0.2*agent.whisker_length*np.sin(whisker_angle)
            x_start = agent.x + 0.2*agent.whisker_length*np.cos(whisker_angle)

            # Set ending x & y coordinates of the whisker
            x_end = agent.x + (agent.whisker_length - deflection)*np.cos(whisker_angle)
            y_end = (agent.whisker_length - deflection)*np.sin(whisker_angle)

            # Update the whisker color
            self.whisker_colors[n] = deflection/agent.whisker_length

            # Update the whisker line
            self.whisker_lines[n] = [(x_start, y_start), (x_end, y_end)]

        # Update the whisker line collection
        self.whisker_line_collection.set_array(self.whisker_colors)
        self.whisker_line_collection.set_segments(self.whisker_lines)

        # Update the texture line data
        self.texture_line.set_data(self.texture_x, texture_y)

        return self.texture_line, self.whisker_line_collection

    def animate(self, update_func):
        self.update_func = update_func

        # Create the animation
        anim = animation.FuncAnimation(self.figure, self.update_plot, init_func=lambda:[self.texture_line, self.whisker_line_collection], interval=1, blit=True)

        # Show the plot
        plt.show()