import numpy
import re
import sys


def default_viability_func(generated_word):
    min_length = 4
    max_length = 10
    max_consonant_string = 2
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']

    unviable = False

    # Ensure there are vowels.
    unviable = unviable or not any(char in vowels for char in generated_word)

    # Ensure the name is long enough but not too long.
    unviable = unviable or len(generated_word) > max_length
    unviable = unviable or len(generated_word) < min_length

    # Ensure there are never too many consonants in a row.
    consonant_strings = re.findall(r'[^aeiou]+', generated_word)
    unviable = unviable or not consonant_strings
    unviable = unviable or len(max(consonant_strings, key=len)) > max_consonant_string

    # Check that no more than 2 sequential characters appear in a row.
    unviable = unviable or re.search(r'(.)\1\1', generated_word)

    return not unviable


class WordGenerator:
    class MarkovElement:
        def __init__(self):
            self.chars = []
            self.probabilities = []

    def __init__(self, input_path, viability_func=default_viability_func):
        self.input_path = input_path
        self.word_is_viable = viability_func
        self._load_table()

    def generate_name(self):
        name = ''
        while not self.word_is_viable(name):
            name = self._generate_raw_name()
        name = name.capitalize()
        return name

    def _generate_raw_name(self):
        name = '^'
        while name[-1] != '$':
            prev_char = name[-1]
            name += self._choose_curr_char(prev_char)
        stripped_name = self._strip_special_chars_from(name)
        return stripped_name

    def _choose_curr_char(self, prev_char):
        ''' Get the next character based on the markov probabilities of the current character. '''
        markov_elem = self.markov_elems[prev_char]
        char = numpy.random.choice(markov_elem.chars, p=markov_elem.probabilities)
        return char

    def _load_table(self):
        self.markov_elems = {}
        with open(self.input_path) as input_file:
            for line in input_file:
                prev_char, curr_char, prob = self._parse_table_line(line)

                if prev_char not in self.markov_elems:
                    self.markov_elems[prev_char] = WordGenerator.MarkovElement()
                self.markov_elems[prev_char].chars.append(curr_char)
                self.markov_elems[prev_char].probabilities.append(float(prob))

    @staticmethod
    def _parse_table_line(line):
        tokens = line.rstrip().split(' ')
        return tokens[0][0], tokens[0][1], tokens[1]

    @staticmethod
    def _strip_special_chars_from(word):
        return word[:-1][1:]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        if len(sys.argv) != 3:
            print('Incorrect number of arguments arguments, expected:\n'
                  'WordGenerator.py <input-table-path>')
            exit(1)

    input_path = sys.argv[1]

    generator = WordGenerator(input_path)
    words = [generator.generate_name() for _ in range(50)]
    print(', '.join(words))
