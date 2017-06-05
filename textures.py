import numpy as np

class SineTexture:
    def __init__(self, amplitude, y_offset, phase, frequency):
        self.amplitude = amplitude
        self.y_offset  = y_offset
        self.phase     = phase
        self.frequency = frequency

    def value(self, x):
        '''
        Return the value of the texture at position x.
        Note: x can be either a scalar position (int/float) or an array of positions.
        '''

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
        '''
        Return the value of the texture at position x.
        Note: x can be either a scalar position (int/float) or an array of positions.
        '''

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

class SpikeTexture:
    def __init__(self, amplitude, y_offset, phase, frequency):
        self.amplitude = amplitude
        self.y_offset  = y_offset
        self.phase     = phase
        self.frequency = frequency
        self.T         = 2*np.pi/self.frequency

    def value(self, x):
        '''
        Return the value of the texture at position x.
        Note: x can be either a scalar position (int/float) or an array of positions.
        '''
        x_mod = (x - self.phase) % self.T
        total_range = self.max_value() - self.min_value()

        if type(x) == int:
            if x_mod < self.T/2:
                y = self.max_value() - total_range*x_mod/(self.T/2)
            else:
                y = self.max_value() - total_range*(1 - (x_mod - self.T/2)/(self.T/2))
        else:
            y = 0*x + self.max_value() - total_range*(1 - (x_mod - self.T/2)/(self.T/2))
            y[x_mod < self.T/2] = self.max_value() - total_range*x_mod[x_mod < self.T/2]/(self.T/2)
        
        return y

    def max_value(self):
        return self.y_offset + self.amplitude

    def min_value(self):
        return self.y_offset - self.amplitude

class FlatTexture:
    def __init__(self, y):
        self.y  = y

    def value(self, x):
        '''
        Return the value of the texture at position x.
        Note: x can be either a scalar position (int/float) or an array of positions.
        '''

        return 0*x + self.y

    def max_value(self):
        return self.y

    def min_value(self):
        return self.y