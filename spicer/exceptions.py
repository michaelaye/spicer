class SpicerError(Exception):
    pass


class SpiceError(SpicerError):
    def __init__(self, function):
        self.function = function

    def __str__(self):
        return "SPICE: Calulating {} failed.".format(self.function)


class MissingParameterError(SpicerError):
    def __init__(self, txt):
        self.txt = txt

    def __str__(self):
        return "Parameter missing: {}".format(self.txt)


class SPointNotSetError(SpicerError):
    def __init(self, txt):
        self.txt = txt

    def __str__(self):
        return "Surface point has not been set. {}".format(self.txt)
