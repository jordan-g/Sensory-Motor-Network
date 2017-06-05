import numpy as np

class Agent:
    def __init__(self, n_whiskers, whisker_length, total_whiskers_angle, n_sensory_cells):
        self.x                    = 0
        self.n_whiskers           = n_whiskers
        self.whisker_length       = whisker_length
        self.total_whiskers_angle = total_whiskers_angle
        self.n_sensory_cells      = n_sensory_cells

        self.whiskers = Whiskers(self, self.n_whiskers, self.whisker_length, self.total_whiskers_angle)
        self.sensory_cells = SensoryCells(self, self.n_sensory_cells, self.n_whiskers)

    def update_whisker_deflections(self, texture):
        self.whiskers.calculate_deflections(texture)
        self.sensory_cells.calculate_activity(self.whiskers.deflections)

    def move(self, speed):
        self.x += speed
        self.whiskers.origin_x = self.x

class Whiskers:
    def __init__(self, agent, n, whisker_length, total_whiskers_angle):
        # Initialize variables
        self.agent                = agent
        self.n                    = n
        self.total_whiskers_angle = total_whiskers_angle
        self.whisker_length       = whisker_length
        self.origin_x             = agent.x

        self.deflections    = np.zeros(self.n)
        self.whisker_angles = np.linspace((np.pi - total_whiskers_angle)/2, (np.pi + total_whiskers_angle)/2, self.n)

    def calculate_deflections(self, texture):
        y_range = np.linspace(texture.min_value(), texture.max_value(), 100)

        for n in range(self.n):
            whisker_angle = self.whisker_angles[n]
            whisker_x_values = y_range/np.tan(whisker_angle)

            texture_y_values = texture.value(whisker_x_values + self.origin_x)

            whisker_lengths = np.hypot(y_range, whisker_x_values)[y_range >= texture_y_values]

            if len(whisker_lengths) > 0:
                min_whisker_length = np.amin(whisker_lengths)
            else:
                min_whisker_length = self.whisker_length

            deflection = np.maximum(self.whisker_length - min_whisker_length, 0)
            self.deflections[n] = deflection

class SensoryCells:
    def __init__(self, agent, n, n_whiskers):
        self.agent = agent
        self.n = n
        self.activity = np.zeros(self.n)
        self.weights = np.random.normal(size=(self.n, n_whiskers))

    def calculate_activity(self, input):
        self.input = input
        self.activity = np.dot(self.weights, self.input)

    def update_weights(self, target_activity):
        self.weights += 0.01*np.dot((target_activity - self.activity)[:, np.newaxis], self.input[:, np.newaxis].T)