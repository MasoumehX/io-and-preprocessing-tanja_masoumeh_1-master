**Implementing a training preparation script**
  
As the first step, you will need to write a script to prepare your training
data. Your program will need to assign unique numbers to each label occurring
in the training data and save this mapping to a file on disk. This label
inventory will eventually be used for training, validation and prediction.

Add docstrings for every method or class that you implement.
____________

## 1. CONLL-U IO

The data that you will deal with comes in the
[the CONLL-U format](https://universaldependencies.org/format.html).

### Tokens

Tokens are specified through lines with 10 tab-separated (`\t`) fields. Lines
are terminated by a single `\n`.

1. *ID* - Integer starting at 1, specifying the position in the sentence.
Multi-word token *ID* is given as a range. E.g. `1-3` for a multi-word
token spanning positions 1 to 3. Empty nodes are marked by a dot `.` between
two integer values.
2. *FORM* - The surface form of the token.
3. *LEMMA* - Lemmatized representation of the token.
4. *UPOS* - Universal POS.
5. *XPOS* - Language specific POS.
6. *FEATS* - Morphological features.
7. *HEAD* - Index of the head of the token (`0` for ROOT relation).
8. *DEPREL* - Universal dependency relation to the *HEAD*, (`root` if `HEAD == 0`)
9. *DEPS* - Enhanced dependency graph in the form of a list of head-deprel pairs.
10. *MISC* - Other annotations.

**Fields are required to be non-empty.** Absence of an annotation is indicated
by a single underscore `_`. Spaces are only permitted in *FORM*, *LEMMA* and
*MISC*.

### Sentences

Sentences are lists of token lines. Sentence boundaries are marked by a blank
line, i.e. `line == '\n'`. Sentences can be preceded by comments, these are
prefixed with `#`.

### 1.1 Token representation

Implement `data.token.Token` as a 
[dataclass](https://docs.python.org/3/library/dataclasses.html). Your `Token`
doesn't need to store its *ID* field field because it is implicitly stored by
the `Token`s offset in its sentence. 

* Annotations and features need to be accessible by lowercasing the above
  identifiers, i.e. the `XPOS` of a Token `t` should be accessible via
  `t.xpos`, `FEATS` as `t.feats`.
* Unspecified features should **not** be represented as `"_"` for `Token` but as
  `None`, i.e. iff the *UPOS* column of a Token contains `_`, `t.upos is None`.
  * Hint: check out the [typing](https://docs.python.org/3/library/typing.html) 
  and [Optional](https://docs.python.org/3/library/typing.html#typing.Optional)
* `Token.__str__` returns the CONLL-U representation for the given `Token`
  without the *ID* field.

### 1.2 Reader

Implement `data.reader.read_sentences` such that it returns an iterator over
the sentences from the path passed as its argument. Returned sentences need be
represented as a list of `data.token.Token`.

Your reader should ignore comments, multi-word tokens and empty nodes. It
should not return empty sentences and be able to handle multiple blank lines
at the start and end of the file and between sentences.  

The method should **not** return a list of all sentences in the file.

## 2. Numbering features

To transform `Token`s into examples to learn from, their features need to be
mapped to unique identifiers. This mapping is determined by the training data:
the set of possible `labels` is composed of all unique values that the feature
takes in the training set. Depending on the task, an evaluation set can include
values for the given feature that did not appear in the training data. Such
cases are generally handled by returning a special `<UNK>` identifier.

Your task is to implement `data.numberer.Numberer`:

- `Numberer`s have to be initialized with `<UNK>` as their first entry.
- `Numberer.val2idx` returns the corresponding identifier for the input.
  * Unknown values are added if `insert=True`, otherwise return the 
    `<UNK>` index.
  * If an unknown value was added, return the corresponding index. 
- `Numberer.seq2idx` takes an iterable of values as input and returns a
  generator yielding the corresponding indices. Again, `insert` toggles whether
  new items are added.
- `Numberer.idx2val` takes an index as its input and returns the value mapped
  to the given index.
- `Numberer.indices2seq` takes an iterable of indices as input and returns a
  generator yielding the corresponding values.
- `Numberer.save` saves the state of the `Numberer` to the path given as
  argument.
- `Numberer.load` restores the state of the `Numberer` from the path given as
  argument
- `Numberer.__len__` returns the number of mapped values.

After implementing the `Numberer`, you can run some unittests by executing
[pytest](https://docs.pytest.org/en/latest/) in the package root. Passing 
these tests does **not** guarantee everything works as intended. 

## 3. Preparation script

To actually prepare the mapping, you need to implement `prepare.py` such that
it takes as positional arguments a [toml](https://en.wikipedia.org/wiki/TOML)
file specifying the configuration, the path of a CONLL-U file to extract the
labels from and a path to save your `Numberer` to.

For now, your configuration file should contain a single field `target`
specifying what annotation your preparation script should extract. I.e., if
your config file contains `target = "XPOS"`, your script should number all 
values `XPOS` takes in the given CONLL-U file.

Only implement the logic to extract values for `LEMMA`, `UPOS`, `FEATS` and 
`XPOS`.

Do **not** implement your own toml parser, use the `toml` package.

```sh
python prepare.py config.toml train.conllu train.labels
```
should read all values of the feature specified in `config.toml` from 
`train.conllu` and write those to `train.labels`.

You can test your script by downloading
[the UD treebanks](https://universaldependencies.org/#download).