from abc import ABC
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
from simstring.feature_extractor.word_ngram import WordNgramFeatureExtractor
from typing import Union


class BaseDatabase(ABC):
    def __init__(self, feature_extractor: Union[
            CharacterNgramFeatureExtractor, WordNgramFeatureExtractor
        ]):
        raise NotImplementedError

    def add(self, string: str) -> None:
        raise NotImplementedError

    def lookup_strings_by_feature_set_size_and_feature(self, size: int, feature: str) -> set[str]:
        raise NotImplementedError
