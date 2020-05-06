"""
Class for transforming Tokens into examples to learn from, their features need to be mapped to unique identifiers.
@author: Tanja Heck and Masoumeh Tari
@date: May 2020
@place: Germany, University of Tuebingen
"""

from attr import dataclass

# TODO: should we add annotation here? @dataclass
class Numberer:

    def __init__(self, values=None):
        # TODO: why we have else?
        """ Constructor """
        if values is None:
            self.data = ['<UNK>']
        else:
            self.data = values

    def __len__(self):
        """ This method returns the number of mapped values (including the <UNK> labels). """
        return len(self.data)

    # TODO: it is not what we are supposed to implement?
    def value2idx(self, value, insert):
        """ This method returns the index of a value in labels. """

        if value in self.data:
            return self.data.index(value)
        else:
            if insert:
                self.data.append(value)
                return self.data.index(value)
            else:
                return 0

    # TODO: insert toggles whether new items are added???
    # TODO: seq2idx name?
    def seq2indices(self, values, insert):
        """ This method returns a generator for the indices of the given values in labels. """
        for value in values:
            yield self.value2idx(value, insert)

    def idx2value(self, idx):
        """ This method returns the label at the given index in labels. """
        return self.data[idx] if idx < len(self.data) else self.data[0]

    def indices2seq(self, indices):
        """ This method returns a generator for the labels of the given indices in labels. """
        for index in indices:
            yield self.idx2value(index)

    def save(self, file):
        """ This method saves the state of the numberer to the specified file. """
        # TODO: what kind of format? file is a path not an object to write!
        file.write(';'.join(self.data))

    @staticmethod
    def load(file):
        """This method initializes a numberer object from the specified file and returns it."""
        line = file.readline()
        return Numberer(line.split(';'))
