from collections import defaultdict
from typing import List, Set, Dict, Union
from .base import BaseDatabase
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
from simstring.feature_extractor.word_ngram import WordNgramFeatureExtractor
import pickle
import ast

def defaultdict_set():
    return defaultdict(set)


class DictDatabase(BaseDatabase):
    def __init__(self, feature_extractor: Union[CharacterNgramFeatureExtractor, WordNgramFeatureExtractor]):
        self.feature_extractor = feature_extractor
        self.strings: List[str] = []
        self.feature_set_size_to_string_map: Dict[int, Set[str]] = defaultdict(
            set
        )  # 3.10 and up only
        self.feature_set_size_and_feature_to_string_map: dict = defaultdict(
            defaultdict_set
        )
        self._min_feature_size = 9999999
        self._max_feature_size = 0


    def add(self, string: str) -> None:
        features = self.feature_extractor.features(string)
        size = len(features)

        self.strings.append(string)
        self.feature_set_size_to_string_map[size].add(string)
        
        self._min_feature_size = min(self._min_feature_size, size)
        self._max_feature_size = max(self._max_feature_size, size)

        for feature in features:
            self.feature_set_size_and_feature_to_string_map[size][feature].add(string)

    def all(self) -> List[str]:
        return self.strings

    def lookup_strings_by_feature_set_size_and_feature(
        self, size: int, feature: str
    ) -> Set[str]:
        return self.feature_set_size_and_feature_to_string_map[size][feature]

    def min_feature_size(self) -> int:
        return self._min_feature_size

    def max_feature_size(self) -> int:
        return self._max_feature_size

    # def __getstate__(self):
    #     """To pickle the object"""
    #     return self.__dict__

    # def __setstate__(self, d):
    #     """To unpickle the object"""
    #     self.__dict__ = d

    def to_pickle(self) -> str:
        "Hack to get object savable with mypyc"
        data = {
            "feature_extractor":self.feature_extractor.__define__(),
            "strings":self.strings,
            "feature_set_size_to_string_map": self.feature_set_size_to_string_map,
            "feature_set_size_and_feature_to_string_map":self.feature_set_size_and_feature_to_string_map,
            "_min_feature_size": self._min_feature_size,
            "_max_feature_size":self._max_feature_size
        }
        return pickle.dumps(data)


    @staticmethod
    def from_dict(data: dict) -> "DictDatabase":
        "Hack to get object loadable with mypyc"
        obj = DictDatabase(ast.literal_eval(data["feature_extractor"]))
        obj.strings = data["strings"]
        obj.feature_set_size_to_string_map.update(data["feature_set_size_to_string_map"])
        obj.feature_set_size_and_feature_to_string_map.update(data["feature_set_size_and_feature_to_string_map"])
        obj._min_feature_size = data["_min_feature_size"]
        obj._max_feature_size = data["_max_feature_size"]
        return obj

    def save(self, filename: str):
        """Save the database to a file as defined by filename.

        Args:
            filename: Filename to save the db at. Should include file extension.

        Returns:
            None
        """
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename: str) -> "DictDatabase":
        """Load db from a file

        Args:
            filename (str): Name of the file to load

        Returns:
            DictDatabase: the db
        """
        with open(filename, "rb") as f:
            db = pickle.load(f)
        return db

    def dumps(self) -> bytes:
        """Generate pickle byte stream

        Returns:
            _type_: _description_
        """
        return pickle.dumps(self)

    @staticmethod
    def loads(binary_data: bytes) -> "DictDatabase":
        """Load a binary string representing a database

        Initially only unpickles the data

        Args:
            binary_data (str): String of data to unpickle

        Returns:
            Model object
        """
        return pickle.loads(binary_data)
