from .base import BaseFeatureExtractor, SENTINAL_CHAR
from typing import List

class CharacterNgramFeatureExtractor(BaseFeatureExtractor):
    def __init__(self, n:int=2):
        self.n = n

    def features(self, string):
        list_of_ngrams = self._each_cons('$' * (self.n - 1) + string + '$' * (self.n - 1), self.n)
        return self.uniquify_list(list_of_ngrams) 
