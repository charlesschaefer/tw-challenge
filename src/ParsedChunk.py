
class ParsedChunk(object):
    qtd = 0
    sides = 0
    value = 0
    _operation = ''

    def __init__(self, qtd, sides, value):
        self.qtd = qtd
        self.sides = sides
        self.value = value

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, value):
        if (value not in ['+', '-']) and value != '':
            raise ValueError("Operation can be only '+', '-' or ''. Was " + value)
        
        self._operation = value
        