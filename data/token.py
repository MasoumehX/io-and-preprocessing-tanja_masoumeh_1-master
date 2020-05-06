"""
Class for token representation for each sentence in the corpus.


@author: Tanja Heck and Masoumeh Tari
@date: April 2020
@place: Germany, University of Tuebingen
"""

from typing import Optional
from attr import dataclass


@dataclass
class Token:
    """ Tokens according to CONLL-U format. Assumption that lists are also represented as strings."""

    # TODO: why we are not using the _init_ which is the constructor for the class?

    # Input variables. Some of the variables are optionals and it means they can be filled with string values or None.
    form: Optional[str]
    lemma: Optional[str] = None
    upos: Optional[str] = None
    xpos: Optional[str] = None
    feats: Optional[str] = None
    head: Optional[str] = None
    deprel: Optional[str] = None
    deps: Optional[str] = None
    misc: Optional[str] = None

    def __str__(self):
        """This method returns the CONLL-U representation of the token in one line."""

        return self.none_to_underscore(self.form) + '\t' + self.none_to_underscore(self.lemma) + \
            '\t' + self.none_to_underscore(self.upos) + '\t' + self.none_to_underscore(self.xpos) + \
            '\t' + self.none_to_underscore(self.feats) + '\t' + self.none_to_underscore(self.head) + \
            '\t' + self.none_to_underscore(self.deprel) + '\t' + self.none_to_underscore(self.deps) + \
            '\t' + self.none_to_underscore(self.misc)

    def none_to_underscore(self, feature):
        """ This method converts None values to '_' (underscore) """
        return '_' if feature is None else feature
