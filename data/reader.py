"""
Class for reading the corpus. Please pay attention to the output format.

@author: Tanja Heck and Masoumeh Tari
@date: April 2020
@place: Germany, University of Tuebingen
"""

import re
from data.token import Token


def read_sentences(path):
    """
     This functions reads the corpus and returns a list of sentences in the corpus.
     Each sentences contains a list of Token object with CONNL-U format.

    Args:
         path (string) : The path to the corpus's file on the hard disk.
     Return:
         sentences (list):  A list of all sentences in the corpus.
    """

    try:
        sentences = []
        tokens = []

        # Check if the given path is exist.
        with open(path, "r", encoding="utf8") as file:

            # Iterate over the lines in the file.
            for line in file:

                line = line.strip()

                # Checking if we are at the beginning of line to read tokens
                if not line.startswith('#'):

                    # Checking if the line is a blank line
                    if line == '\n' or line == '':
                        if tokens:
                            sentences.append(tokens)
                            tokens = []
                    else:
                        string_tokens = [None if x == '_' else x for x in line.split("\t")]
                        # Create a Token object
                        token = Token(string_tokens[1], string_tokens[2], string_tokens[3], string_tokens[4],
                                      string_tokens[5], string_tokens[6], string_tokens[7], string_tokens[8],
                                      string_tokens[9])

                        # Detecting the multi-words using the regex pattern. Multi-words should be ignored.
                        if re.search(r'^\d\-\d', line) is None and re.search(r'^\d\.\d', line) is None:
                            tokens.append(token)

            # At the end, we add tokens to the list of sentences.
            if tokens:
                sentences.append(tokens)
            return iter(sentences)
    except Exception as e:
        print(e)


