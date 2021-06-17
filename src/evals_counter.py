# Copiado de:
#   https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class EvalsCounter(metaclass=Singleton):
    """Para contar el numero de evaluaciones del fitness que llevamos consumidas"""

    def __init__(self):
        self.evals_cons = 0

    def add_evals(self, number_of_evals):
        self.evals_cons += number_of_evals

    def reset(self):
        self.evals_cons = 0

    def get_evals(self):
        return self.evals_cons
