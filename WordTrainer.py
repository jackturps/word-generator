import sys


class WordTrainer:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

        self.single_counts = {}
        self.pair_counts = {}

    def generate_table(self):
        with open(self.input_path, 'r') as input_file:
            for raw_name in input_file:
                name = raw_name.lower()
                print(name)
                for char_idx, _ in enumerate(name):
                    # Use '^' at the start of words and '$' at the end of words.
                    prev_char = name[char_idx - 1] if char_idx > 0 else '^'
                    curr_char = name[char_idx] if name[char_idx] != '\n' else '$'

                    # Store a count of single characters and pairs.
                    pair = prev_char + curr_char
                    if pair not in self.pair_counts:
                        self.pair_counts[pair] = 0
                    self.pair_counts[pair] += 1
                    if prev_char not in self.single_counts:
                        self.single_counts[prev_char] = 0
                    self.single_counts[prev_char] += 1

            for pair, count in self.pair_counts.items():
                char = pair[0]
                self.pair_counts[pair] = (count / self.single_counts[char])

        with open(self.output_path, 'w') as output_file:
            for pair, prob in self.pair_counts.items():
                output_file.write('%s %s\n' % (pair, prob))

        # print(json.dumps(self.pair_counts, indent=2))
        # print(json.dumps(self.single_counts, indent=2))

        pass


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
