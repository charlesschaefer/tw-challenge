import re 
from .ParsedChunk import ParsedChunk

class FileParser:
    file_content = ""
    def __init__(self, file_content):
        if file_content == "":
            raise AttributeError("File content is empty")
        self.file_content = file_content
        
    ## parses a single chunk of a line of the file
    # Examples of a chunk: 1d6, d8, 2d10, 2D10, 1D8, D8
    def parse_chunk(self, chunk):
        qtd = 0
        sides = 0
        value = 0
        try:
            value = int(chunk)
        except:
            # A RegExp pattern to match the chunk pattern
            # this will return a list with each segment of the chunk: 
            #   - a number (optional), the D letter (insensitive) and another number
            match = re.findall("(\d*)(d|D)(\d+)", chunk)
            if len(match) < 1 or len(match[0]) != 3:
                raise ValueError("Can't parse the chunk because it doesn't match the pattern")

            qtd = int(match[0][0] or 1)
            sides = int(match[0][2])
        
        return ParsedChunk(qtd, sides, value)
    
    ## Parses a line of the file and returns a list of ParsedChunk objects
    def parse_line(self, line):
        # A RegExp pattern to match the line pattern
        # this will return a list with each part of line as a chunk
        chunks = re.findall("(\d?[dD]?\d+\s?[-+]?)", line)
        if len(chunks) == 0:
            raise ValueError("Can't parse the line because it doesn't match the pattern")
        
        parsedChunks = []
        # parse each of the chunks
        for value in chunks:
            parts = value.split(" ")
            chunk = parts[0]
            operation = ''
            if len(parts) > 1:
                operation = parts[1]
            
            parsedChunk = self.parse_chunk(chunk)
            parsedChunk.operation = operation
            
            parsedChunks.append(parsedChunk)
        
        return parsedChunks

    ## Parses each line in the file and returns as a list of lists of parsedChunks
    def parse_file(self):
        parsedFile = [self.parse_line(line) for line in self.file_content.split("\n") if line != '']
        return parsedFile

