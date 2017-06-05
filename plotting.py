import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection
import matplotlib.animation as animation

class AnimationPlot:
    def __init__(self, x_min, y_min, x_max, y_max):
        # Create the figure
        self.figure = plt.figure(figsize=((x_max - x_min)/(y_max - y_min), 4))

    def create_texture(self, texture, texture_length):
        # Create texture x values
        self.texture_x = np.linspace(0, texture_length, 100*texture_length)
        
        # Plot the texture
        self.texture_line, = self.animation_axis.plot([], [], color='#5C5C5C', lw=1)

    def create_whiskers(self, n_whiskers):
        # Initialize the list of whisker lines & colors
        # Note: colors are initialized to span the range (0, 1) in order to set the correct max & min for the subsequent animation
        self.whisker_lines = [[(0, 0), (0, 0)]]*n_whiskers
        self.whisker_colors = np.linspace(0, 1, n_whiskers)

        # Create a line collection from the whisker lines & colors
        self.whisker_line_collection = LineCollection(self.whisker_lines, array=self.whisker_colors, cmap=cm.rainbow, lw=0.5)
        self.animation_axis.add_collection(self.whisker_line_collection)

    def create_animation_plot(self, x_min, y_min, x_max, y_max):
        self.animation_axis = plt.Axes(self.figure, [0, 0.66, 1, 0.33])
        self.figure.add_axes(self.animation_axis)
        self.animation_axis.set_axis_off()
        self.animation_axis.set_xlim(x_min, x_max)
        self.animation_axis.set_ylim(x_min - 1, y_max + 1)

    def create_whisker_deflection_plot(self, n_sensory_cells):
        self.whisker_deflection_axis = plt.Axes(self.figure, [0, 0.33, 1, 0.33])
        self.figure.add_axes(self.whisker_deflection_axis)

        self.whisker_deflection_axis.set_axis_off()
        self.whisker_deflection_axis.set_xlim(-0.5, n_sensory_cells - 0.5)
        self.whisker_deflection_axis.set_ylim(0, 1)

        self.whisker_deflection_lines = []

        # Update whisker deflection lines
        for n in range(n_sensory_cells):
            # Set starting x & y coordinates of the whisker deflection line
            x_start = n
            y_start = 0.1

            # Set ending x & y coordinates of the whisker deflection line
            x_end = n
            y_end = 0.9

            self.whisker_deflection_lines.append([(x_start, y_start), (x_end, y_end)])

        # Initialize the list of sensory whisker deflection colors
        self.whisker_deflection_colors = np.linspace(0, 1, n_sensory_cells)

        # Create a line collection from the whisker deflection lines & colors
        self.whisker_deflection_line_collection = LineCollection(self.whisker_deflection_lines, array=self.whisker_deflection_colors, cmap=cm.rainbow, lw=5)
        self.whisker_deflection_axis.add_collection(self.whisker_deflection_line_collection)

    def create_sensory_cell_activity_plot(self, n_sensory_cells):
        self.sensory_cell_activity_axis = plt.Axes(self.figure, [0, 0, 1, 0.33])
        self.figure.add_axes(self.sensory_cell_activity_axis)

        self.sensory_cell_activity_axis.set_axis_off()
        self.sensory_cell_activity_axis.set_xlim(-0.5, n_sensory_cells - 0.5)
        self.sensory_cell_activity_axis.set_ylim(0, 1)

        self.sensory_cell_activity_lines = []

        # Update sensory cell activity lines
        for n in range(n_sensory_cells):
            # Set starting x & y coordinates of the cell activity line
            x_start = n
            y_start = 0.1

            # Set ending x & y coordinates of the cell activity line
            x_end = n
            y_end = 0.9

            self.sensory_cell_activity_lines.append([(x_start, y_start), (x_end, y_end)])

        # Initialize the list of sensory cell activity colors
        self.sensory_cell_activity_colors = np.linspace(0, 1, n_sensory_cells)

        # Create a line collection from the sensory cell activity lines & colors
        self.sensory_cell_activity_line_collection = LineCollection(self.sensory_cell_activity_lines, array=self.sensory_cell_activity_colors, cmap=cm.rainbow, lw=5)
        self.sensory_cell_activity_axis.add_collection(self.sensory_cell_activity_line_collection)

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

        # Update sensory cell activity lines
        for n in range(agent.n_sensory_cells):
            # Get cell activities
            cell_activity = agent.sensory_cells.activity[n]

            # Update the cell activity line color
            self.sensory_cell_activity_colors[n] = cell_activity/np.amax(agent.sensory_cells.activity)

        # Update whisker deflection lines
        for n in range(agent.n_whiskers):
            # Get whisker deflection
            deflection = agent.whiskers.deflections[n]

            # Update the whisker deflection line color
            self.whisker_deflection_colors[n] = deflection/agent.whisker_length

        # Update the whisker line collection
        self.whisker_line_collection.set_array(self.whisker_colors)
        self.whisker_line_collection.set_segments(self.whisker_lines)

        # Update the whisker deflection line collection
        self.whisker_deflection_line_collection.set_array(self.whisker_deflection_colors)

        # Update the cell activation line collection
        self.sensory_cell_activity_line_collection.set_array(self.sensory_cell_activity_colors)

        # Update the texture line data
        self.texture_line.set_data(self.texture_x, texture_y)

        return self.texture_line, self.whisker_line_collection, self.whisker_deflection_line_collection, self.sensory_cell_activity_line_collection

    def animate(self, update_func):
        self.update_func = update_func

        # Create the animation
        anim = animation.FuncAnimation(self.figure, self.update_plot, init_func=lambda:[self.texture_line, self.whisker_line_collection, self.whisker_deflection_line_collection, self.sensory_cell_activity_line_collection], interval=1, blit=True)

        # Show the plot
        plt.show()