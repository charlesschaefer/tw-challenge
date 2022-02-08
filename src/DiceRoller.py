from .ParsedChunk import ParsedChunk
from .Die import Die
from .RollResult import RollResult

class DiceRoller:
    def __init__(self, input_object):
        for line in input_object:
            for chunk in line:
                if not isinstance(chunk, ParsedChunk):
                    raise ValueError("Can't format because the input insn't well formatted")
        
        self.input_object = input_object
    
    ## Rolls the dice of a line and return the final value, max and min dice values
    # @param line A single line, represented by a list of ParsedChunk objects
    # @return dict with the keys roll, min and max (all integers)
    def roll(self, line):
        dice = []
        final_roll = 0
        next_operation = "+"
        for chunk in line:
            if chunk.value > 0:
                final_roll = self._operate(final_roll, chunk.value, next_operation)
                # Todo: the integer value should be considered for max/min values?
                dice.append(chunk.value)
            else:
                for i in range(chunk.qtd):
                    die = Die(chunk.sides)
                    dice.append(die.roll())
                    final_roll = self._operate(final_roll, die, next_operation)
                
                next_operation = chunk.operation
        
        return RollResult(final_roll, min(dice), max(dice))

    ## Rolls the dice of all the lines
    def roll_all(self):
        result = []
        for line in self.input_object:
            result.append(self.roll(line))
        
        return result


    ## help method to sum/subtract
    def _operate(self, value1, value2, operator):
        if operator == "-":
            return value1 - value2
        return value1 + value2
