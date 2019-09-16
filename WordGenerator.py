import numpy
import re
import sys


class WordGenerator:
    class ProbabilityElement:
        def __init__(self):
            self.chars = []
            self.probs = []

    @staticmethod
    def _is_viable_name(name):
        min_length = 3
        max_length = 10
        max_consonant_string = 3
        vowels = ['a', 'e', 'i', 'o', 'u', 'y']

        unviable = False

        # Ensure there are vowels.
        unviable = unviable or not any(char in vowels for char in name)

        # Ensure the name is long enough but not too long.
        unviable = unviable or len(name) > max_length
        unviable = unviable or len(name) < min_length

        # Ensure there are never too many consonants in a row.
        consonant_strings = re.findall(r'[^aeiou]+', name)
        unviable = unviable or not consonant_strings
        unviable = unviable or len(max(consonant_strings, key=len)) > max_consonant_string

        return not unviable

    def __init__(self, input_path):
        self.input_path = input_path

        # Load the probability table into a usable data type.
        self.probs = {}
        with open(self.input_path) as input_file:
            for line in input_file:
                tokens = line.rstrip().split(' ')
                prev_char = tokens[0][0]
                curr_char = tokens[0][1]
                prob = tokens[1]

                if prev_char not in self.probs:
                    self.probs[prev_char] = WordGenerator.ProbabilityElement()
                self.probs[prev_char].chars.append(curr_char)
                self.probs[prev_char].probs.append(float(prob))

    def generate_name(self):
        # Generate names until we are within the length range.
        name = ''
        while not self._is_viable_name(name):
            name = '^'
            while name[-1] != '$':
                name += self._get_curr_char(name[-1])
            name = name[:-1][1:]

        name = name.capitalize()
        return name

    def _get_curr_char(self, prev_char):
        # Get the next character based on the given probabilities.
        char = numpy.random.choice(self.probs[prev_char].chars, p=self.probs[prev_char].probs)
        return char


if __name__ == '__main__':
    if len(sys.argv) != 2:
        if len(sys.argv) != 3:
            print('Incorrect number of arguments arguments, expected:\n'
                  'WordGenerator.py <input-table-path>')
            exit(1)

    input_path = sys.argv[1]

    generator = WordGenerator(input_path)
    for _ in range(10):
        print(generator.generate_name())
