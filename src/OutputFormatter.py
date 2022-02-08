import json

from .ParsedChunk import ParsedChunk
from .RollResult import RollResult

class OutputFormatter:
    ## Receives as input_object a list with the needed objects to format the Output
    def __init__(self, input_object):
        for line in input_object:
            if not isinstance(line, RollResult):
                raise ValueError("Can't format because the input insn't well formatted")
        
        self.input_object = input_object
    
    ## Format the file and returns as a JSON string
    # @param compact Defines if the output must be compact or indented (4 spaces)
    def format(self, compact=True):
        to_format = []
        # converts python object to a serializable dict
        for line in self.input_object:
            to_format.append({
                "roll-result": line.roll,
                "roll-min": line.min,
                "roll-max": line.max
            })
        
        if compact:
            format_options = {"separators": (',', ':')}
        else:
            format_options = {"indent": 4}
    
        return json.dumps(to_format, **format_options)


