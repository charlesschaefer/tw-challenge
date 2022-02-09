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
        min_value = 0
        max_value = 0
        final_roll = 0
        current_operation = "+"
        previous_operation = "+"

        for chunk in line:
            if chunk.value > 0:
                final_roll = self._operate(final_roll, chunk.value, current_operation)
                min_value = self._operate(min_value, chunk.value, current_operation)
                max_value = self._operate(max_value, chunk.value, current_operation)
            else:
                for i in range(chunk.qtd):
                    die = Die(chunk.sides)
                    die.roll()
                    final_roll = self._operate(final_roll, die, current_operation)
                    min_value, max_value = self._calculate_die_min_max(
                        die, 
                        current_operation, 
                        min_value, 
                        max_value
                    )

            previous_operation = current_operation
            current_operation = chunk.operation
            
                
        
        return RollResult(final_roll, min_value, max_value)

    ## Rolls the dice of all the lines
    def roll_all(self):
        result = []
        for line in self.input_object:
            result.append(self.roll(line))
        
        return result

    ## Help method to calculate min/max possible of a die
    def _calculate_die_min_max(self, die, operator, current_min, current_max):
        if operator == "+":
            current_min += 1
            current_max += die.sides
        else:
            current_min -= die.sides
            current_max -= 1
        
        return current_min, current_max

    ## help method to sum/subtract
    def _operate(self, value1, value2, operator):
        if operator == "-":
            return value1 - value2
        return value1 + value2
