# Word Generator

This project is a tool that procedurally generates words that are similar in structure to a set 
of sample words. This is especially useful for name generation.

The project consists of two portions - a trainer and a generator.

The trainer is fed a text file containing sample words(e.g. first names) and outputs a 
file containing a probability table that will be used by the generator.

The generator is fed the probability table produced by the trainer and will output
words that approximate the structure of the sample words.

## Using the Trainer

The trainer is used by providing a path to an input file and a path to
an output file. The input file is a regular text file of words each 
seperated by a new line. The trainer has only been tested on 
files that contain alphabetical characters. The output file that is
produced is a table representing a markov chain that will be used by
the generator.

e.g.
```
python3 WordTrainer.py male-names.txt male-names-table.txt
```

## Using the Generator.

The generator is used by providing a path to the output file of the 
trainer. It will then output words that approximate the input words.
The generator can also be used programmatically to produce as many words as
needed.

e.g.
```
python3 WordGenerator.py male-names-table.txt
```