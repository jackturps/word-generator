import sys


class WordTrainer:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

        ''' 
        TODO: Could these be fixed sized lists where we use the character's index in the
        alphabet to access it? That might help to improve performance. 
        '''
        self.single_counts = {}
        self.pair_counts = {}
        self.pair_probabilities = {}

    def generate_table(self):
        with open(self.input_path, 'r') as input_file:
            for raw_sample_word in input_file:
                sample_word = raw_sample_word.lower()
                self._count_char_pairs_in(sample_word)

            self._normalise_char_counts()
        self._output_table()

    def _count_char_pairs_in(self, sample_word):
        for char_idx, _ in enumerate(sample_word):
            prev_char = self._get_prev_char(sample_word, char_idx)
            curr_char = self._get_curr_char(sample_word, char_idx)

            pair = prev_char + curr_char
            if pair not in self.pair_counts:
                self.pair_counts[pair] = 0
            self.pair_counts[pair] += 1

            if prev_char not in self.single_counts:
                self.single_counts[prev_char] = 0
            self.single_counts[prev_char] += 1

    def _normalise_char_counts(self):
        for pair, count in self.pair_counts.items():
            char = pair[0]
            self.pair_probabilities[pair] = (count / self.single_counts[char])

    def _output_table(self):
        with open(self.output_path, 'w') as output_file:
            for pair, prob in self.pair_probabilities.items():
                output_file.write('%s %s\n' % (pair, prob))

    @staticmethod
    def _get_prev_char(sample_word, char_idx):
        ''' Use '^' as a special character to represent the beginning of a sample word. '''
        return sample_word[char_idx - 1] if char_idx > 0 else '^'

    @staticmethod
    def _get_curr_char(sample_word, char_idx):
        ''' Use '$' as a special character to represent the end of a sample word. '''
        return sample_word[char_idx] if sample_word[char_idx] != '\n' else '$'


def main():
    if len(sys.argv) != 3:
        print('Incorrect number of arguments arguments, expected:\n'
              'WordTrainer.py <sample-words-path> <output-table-path>')
        exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    trainer = WordTrainer(input_path, output_path)
    trainer.generate_table()


if __name__ == '__main__':
    main()
