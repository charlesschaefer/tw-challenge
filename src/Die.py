import random

class Die:
    sides = 0
    roll_value = 0

    def __init__(self, sides):
        if sides < 3:
            raise AttributeError("Die can't be smaller than 3 sides")
        self.sides = sides
        
    def roll(self):
        self.roll_value = random.randint(1, self.sides)
        return self.roll_value
    
    def __add__(self, other):
        if self.roll_value == 0:
            raise ValueError("Can't sum Dice before rolling")
        
        if isinstance(other, Die):
            return self.roll_value + other.roll_value
        elif isinstance(other, int):
            return self.roll_value + other
        else:
            return self.roll_value
    
    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if self.roll_value == 0:
            raise ValueError("Can't subtract Dice before rolling")
        
        if isinstance(other, Die):
            return self.roll_value - other.roll_value
        elif isinstance(other, int):
            return self.roll_value - other
        else:
            return self.roll_value

    def __rsub__(self, other):
        if self.roll_value == 0:
            raise ValueError("Can't subtract Dice before rolling")
        
        if isinstance(other, Die):
            return  other.roll_value - self.roll_value
        elif isinstance(other, int):
            return other - self.roll_value
        else:
            return self.roll_value