from src import Die, FileParser, OutputFormatter, ParsedChunk, DiceRoller, RollResult
import unittest
import random
import json

class DieTest(unittest.TestCase): 

    def test_die_roll(self):
        for i in range(10):
            sides = random.randint(3, 30)
            die = Die(sides)

            roll = die.roll()
            self.assertLessEqual(roll, sides)
            self.assertGreaterEqual(roll, 1)
    
    def test_die_cant_be_smaller_than_3(self):
        with self.assertRaises(AttributeError):
            die = Die(2)

    def test_dice_sum(self):
        die1 = Die(5)
        die2 = Die(3)
        roll1 = die1.roll()
        roll2 = die2.roll()

        self.assertEqual(die1 + die2, roll1 + roll2)
        self.assertEqual(die1 + 2, roll1 + 2)
        self.assertEqual(2 + die2, 2 + roll2)
    
    def test_dice_subtract(self):
        die1 = Die(5)
        die2 = Die(3)
        roll1 = die1.roll()
        roll2 = die2.roll()

        self.assertEqual(die1 - die2, roll1 - roll2)
        self.assertEqual(die1 - 2, roll1 - 2)
        self.assertEqual(2 - die2, 2 - roll2)

class FileParserTest(unittest.TestCase):
    def test_file_content_cant_be_empty(self):
        with self.assertRaises(AttributeError):
            parser = FileParser("")
    
    # test the extraction of chunks of a line
    def test_parse_chunk(self):
        dice = ['d8', 'd10', 'd20', '1d12', '2d10', '4D14', '10D18', '9', '1', '158']
        parsed = [
            {"qtd": 1, "sides": 8, "value": 0},
            {"qtd": 1, "sides": 10, "value": 0},
            {"qtd": 1, "sides": 20, "value": 0},
            {"qtd": 1, "sides": 12, "value": 0},
            {"qtd": 2, "sides": 10, "value": 0},
            {"qtd": 4, "sides": 14, "value": 0},
            {"qtd": 10, "sides": 18, "value": 0},
            {"qtd": 0, "sides": 0, "value": 9},
            {"qtd": 0, "sides": 0, "value": 1},
            {"qtd": 0, "sides": 0, "value": 158},
        ]

        parser = FileParser("\n".join(dice))
        for idx in range(len(dice)):
            parsed_chunk = parser.parse_chunk(dice[idx])
            self.assertEqual(parsed[idx]["qtd"], parsed_chunk.qtd)
            self.assertEqual(parsed[idx]["sides"], parsed_chunk.sides)
            self.assertEqual(parsed[idx]["value"], parsed_chunk.value)
            self.assertEqual(parsed_chunk.operation, '')

    # test the parsing of a line
    def test_parse_line(self):
        lines = self._getLines()
        parsed_sample = self._getParsedSample()
        
        parser = FileParser("\n".join(lines))
        for idx in range(len(lines)):
            parsed_line = parser.parse_line(lines[idx])
            self.assertEqual(len(parsed_line), len(parsed_sample[idx]))
            for i in range(len(parsed_line)):
                self.assertEqual(parsed_line[i].qtd, parsed_sample[idx][i]["qtd"])
                self.assertEqual(parsed_line[i].sides, parsed_sample[idx][i]["sides"])
                self.assertEqual(parsed_line[i].value, parsed_sample[idx][i]["value"])
                self.assertEqual(parsed_line[i].operation, parsed_sample[idx][i]["operation"])

    def test_parse_file(self):
        lines = self._getLines()
        parsed_sample = self._getParsedSample()

        parser = FileParser("\n".join(lines))
        parsed_file = parser.parse_file()
        self.assertEqual(len(parsed_file), len(parsed_sample))
        
        # let's check if each file was correctly parsed
        for idx in range(len(lines)):
            parsed_line = parsed_file[idx]
            for i in range(len(parsed_line)):
                self.assertEqual(parsed_line[i].qtd, parsed_sample[idx][i]["qtd"])
                self.assertEqual(parsed_line[i].sides, parsed_sample[idx][i]["sides"])
                self.assertEqual(parsed_line[i].value, parsed_sample[idx][i]["value"])
                self.assertEqual(parsed_line[i].operation, parsed_sample[idx][i]["operation"])

    ###########################
    # data providers methods
    ###########################
    def _getLines(self):
        return [
            "1d6",
            "1d8 + 3",
            "4D6 - 2 + 1d20",
            "2d6 - 2 - 4D8 + d20"
        ]

    def _getParsedSample(self):
        return [
            [{"qtd": 1, "sides": 6, "value": 0, "operation": ''}],
            [
                {"qtd": 1, "sides": 8, "value": 0, "operation": "+"},
                {"qtd": 0, "sides": 0, "value": 3, "operation": ''}
            ],
            [
                {"qtd": 4, "sides": 6, "value": 0, "operation": "-"},
                {"qtd": 0, "sides": 0, "value": 2, "operation": "+"},
                {"qtd": 1, "sides": 20, "value": 0, "operation": ''}
            ],
            [
                {"qtd": 2, "sides": 6, "value": 0, "operation": "-"},
                {"qtd": 0, "sides": 0, "value": 2, "operation": "-"},
                {"qtd": 4, "sides": 8, "value": 0, "operation": "+"},
                {"qtd": 1, "sides": 20, "value": 0, "operation": ''}
            ]
        ]

class OutputFormatterTest(unittest.TestCase):
    def test_input_type_assertion(self):
        with self.assertRaises(ValueError):
            OutputFormatter([{"roll": 18, "min": 2, "max": 12}])


    def test_format(self):
        ob1 = RollResult(18, 2, 8)
        ob2 = RollResult(25, 5, 12)
        ob3 = RollResult(8, 1, 3)

        formatter = OutputFormatter([ob1, ob2, ob3])
        expected_output = '[{"roll-result":18,"roll-min":2,"roll-max":8},{"roll-result":25,"roll-min":5,"roll-max":12},{"roll-result":8,"roll-min":1,"roll-max":3}]'
        self.assertEqual(formatter.format(), expected_output)

        obj = json.loads(expected_output)
        new_output = json.dumps(obj, indent=4)
        self.assertEqual(formatter.format(compact=False), new_output)

class DiceRollerTest(unittest.TestCase):
    def test_roll(self):
        
        ob1 = ParsedChunk(2, 10, 0) # 2d10
        ob1.operation = "+"

        ob2 = ParsedChunk(0, 0, 10) # 10
        ob2.operation = '-'

        ob3 = ParsedChunk(1, 4, 0) # 1d4

        parsed_file = [[ob1, ob2, ob3]]
        input_object = parsed_file
        roller = DiceRoller(input_object)
        result = roller.roll(parsed_file[0])

        # won't test for roll value because, as the dice are randoms, they are not deterministic
        self.assertIsInstance(result, RollResult)
        
        # minimum of 2d10 + 10 - 1d4 = 8
        self.assertEqual(result.min, 8)
        # minimum of 2d10 + 10 - 1d4 = 19
        self.assertEqual(result.max, 19)
        
        
    
    def test_roll_all(self):
        ob1 = ParsedChunk(2, 10, 0) # 2d10
        ob1.operation = "+"

        ob2 = ParsedChunk(0, 0, 10) # 10
        ob2.operation = '-'

        ob3 = ParsedChunk(1, 4, 0) # 1d4

        parsed_line = [ob1, ob2, ob3]
        parsed_file = [parsed_line, parsed_line, parsed_line]
        input_object = parsed_file
        roller = DiceRoller(input_object)
        results = roller.roll_all()

        for line in results:
            # won't test for roll value because, as the dice are randoms, they are not deterministic
            self.assertIsInstance(line, RollResult)
            # minimum of 2d10 + 10 - 1d4 = 8
            self.assertEqual(line.min, 8)
            # minimum of 2d10 + 10 - 1d4 = 19
            self.assertEqual(line.max, 19)



if __name__ == '__main__':
    unittest.main()
