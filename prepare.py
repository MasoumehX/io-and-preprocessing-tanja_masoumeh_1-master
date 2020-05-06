"""
This file has some scripts to prepare the training data.
@author: Tanja Heck and Masoumeh Tari
@date: May 2020
@place: Germany, University of Tuebingen
"""

import sys
import os
import toml as toml
from data.numberer import Numberer
from data.reader import read_sentences


def main(args):

    try:
        # Check if one argument is missing. The number of arguments is four.
        if not len(args) == 4:
            raise TypeError("You need to specify the .config file, the .conllu file and the target file as arguments")

        _, configfile, train_data, train_labels = args

        # Checking if the files are not a directory and they exist.
        files = [configfile, train_data, train_labels]
        for file in files:
            if os.path.isdir(file) or not os.path.exists(file):
                raise TypeError("File " + file + "is a directory or it does not exist!")

        # fields = toml.load(args[1])
        # TODO: using the argument name
        fields = toml.load(configfile)
        if 'target' not in fields:
            raise KeyError('The config file must contain an entry for the field "target"')

        # Extracting the target field
        field_to_extract = fields['target']

        sentences = [entry for entry in read_sentences(train_data)]
        numberer = Numberer()
        for sentence in sentences:
            for token in sentence:
                if field_to_extract == 'LEMMA':
                    numberer.value2idx(token.lemma, True)
                elif field_to_extract == 'UPOS':
                    numberer.value2idx(token.upos, True)
                elif field_to_extract == 'FEATS':
                    numberer.value2idx(token.feats, True)
                elif field_to_extract == 'XPOS':
                    numberer.value2idx(token.xpos, True)
                else:
                    raise ValueError('The value given for "target" in the config file is not supported.')

        with open(train_labels, "r", encoding="utf8") as file:
            numberer.save(file)

        # TODO: why 'w'
        # file = open(args[3], "w")
        # numberer.save(file)
        # file.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    arguments = sys.argv
    main(arguments)
