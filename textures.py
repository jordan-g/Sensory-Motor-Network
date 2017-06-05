import numpy as np

class SineTexture:
    def __init__(self, amplitude, y_offset, phase, frequency):
        self.amplitude = amplitude
        self.y_offset  = y_offset
        self.phase     = phase
        self.frequency = frequency

    def value(self, x):
        return self.y_offset + self.amplitude*np.sin(self.frequency*x + self.phase)

    def max_value(self):
        return self.y_offset + self.amplitude

    def min_value(self):
        return self.y_offset - self.amplitude

class SquareTexture:
    def __init__(self, amplitude, y_offset, phase, frequency):
        self.amplitude = amplitude
        self.y_offset  = y_offset
        self.phase     = phase
        self.frequency = frequency
        self.T         = 2*np.pi/self.frequency

    def value(self, x):
        if type(x) == int:
            if (x - self.phase) % self.T < self.T/2:
                y = self.min_value()
            else:
                y = self.max_value()
        else:
            y = 0*x + self.max_value()
            y[(x - self.phase) % self.T < self.T/2] = self.min_value()

        return y

    def max_value(self):
        return self.y_offset + self.amplitude

    def min_value(self):
        return self.y_offset - self.amplitude

class FlatTexture:
    def __init__(self, y):
        self.y  = y

    def value(self, x):
        return 0*x + self.y

    def max_value(self):
        return self.y

    def min_value(self):
        return self.y