# Word Generator

This project is a tool to help with procedural name generation. 
It has two components, a trainer and a generator. You first train the word
generator on a dataset using the trainer, and you can then generate words
that approximate the structure of the words in the training set.

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
trainer. It will then output 10 words that approximate the input words.
The generator can also be used programmatically to produce as many words as
needed.

e.g.
```
python3 WordGenerator.py male-names-table.txt
```

## TODO

* Allow the user to pass a predicate to the generator to prevent unwanted words.
* Add a retry count to the generator.