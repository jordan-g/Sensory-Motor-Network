import numpy as np

class Agent:
    def __init__(self, n_whiskers, min_whisker_length, max_whisker_length, total_whiskers_angle, n_sensory_cells, sensory_cells_learning_rate):
        self.x                    = 0
        self.n_whiskers           = n_whiskers
        self.total_whiskers_angle = total_whiskers_angle
        self.n_sensory_cells      = n_sensory_cells

        self.whiskers = Whiskers(self, self.n_whiskers, min_whisker_length, max_whisker_length, self.total_whiskers_angle)
        self.sensory_cells = SensoryCells(self, self.n_sensory_cells, self.n_whiskers, sensory_cells_learning_rate)

    def update_whisker_deflections(self, texture):
        self.whiskers.calculate_deflections(texture)
        self.sensory_cells.calculate_activity(self.whiskers.deflections)

    def move(self, speed):
        self.x += speed
        self.whiskers.origin_x = self.x

    def update_whisking_angle(self, angle):
        self.whiskers.whisking_angle = angle
        self.whiskers.calculate_whisker_angles()

class Whiskers:
    def __init__(self, agent, n, min_whisker_length, max_whisker_length, total_whiskers_angle):
        # Initialize variables
        self.agent                = agent
        self.n                    = n
        self.total_whiskers_angle = total_whiskers_angle
        self.whisker_lengths      = 0.2*np.exp(np.linspace(min_whisker_length, max_whisker_length, n))
        self.origin_x             = agent.x
        self.whisking_angle       = np.pi/2

        self.deflections    = np.zeros(self.n)

        self.calculate_whisker_angles()

    def calculate_whisker_angles(self):
        self.whisker_angles = np.linspace((self.whisking_angle - self.total_whiskers_angle)/2, (self.whisking_angle + self.total_whiskers_angle)/2, self.n)

    def calculate_deflections(self, texture):
        y_range = np.linspace(texture.min_value(), texture.max_value(), 100)

        for n in range(self.n):
            whisker_angle = self.whisker_angles[n]
            if whisker_angle < np.pi:
                tan_whisker_angle = np.tan(whisker_angle)
                if tan_whisker_angle != 0:
                    whisker_x_values = y_range/tan_whisker_angle

                    texture_y_values = texture.value(whisker_x_values + self.origin_x)

                    whisker_lengths = np.hypot(y_range, whisker_x_values)[y_range >= texture_y_values]

                    if len(whisker_lengths) > 0:
                        min_whisker_length = np.amin(whisker_lengths)
                    else:
                        min_whisker_length = self.whisker_lengths[n]

                    deflection = np.maximum(self.whisker_lengths[n] - min_whisker_length, 0)
                    self.deflections[n] = deflection
                else:
                    self.deflections[n] = 0
            else:
                self.deflections[n] = 0

class SensoryCells:
    def __init__(self, agent, n, n_whiskers, learning_rate):
        self.agent         = agent
        self.n             = n
        self.activity      = np.zeros(self.n)
        self.weights       = np.random.normal(size=(self.n, n_whiskers))
        self.learning_rate = learning_rate

    def calculate_activity(self, input):
        self.input = input
        self.activity = np.dot(self.weights, self.input)

    def update_weights(self, target_activity):
        self.weights += self.learning_rate*np.dot((target_activity - self.activity)[:, np.newaxis], self.input[:, np.newaxis].T)