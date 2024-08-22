import math
from typing import Iterable
from simstring.database.dict import DictDatabase
from simstring.database.disk import DiskDatabase


class DotMeasure:

    def __init__(self, db: None| DictDatabase | DiskDatabase =None, minsize: int = 1) -> None:
    
        if db:
            self.maxsize = db._min_feature_size
        else:
            self.maxsize = minsize

    def min_feature_size(self, query_size: int, alpha: float) -> int:
        return 1

    def max_feature_size(self, query_size: int, alpha: float) -> int:
        return query_size
    
    def minimum_common_feature_count(
        self, query_size: int, y_size: int, alpha: float
    ) -> int:
        return int(math.ceil(alpha * math.sqrt(query_size * y_size)))

    def similarity(self, X: Iterable[str], Y: Iterable[str]) -> float:
        return len(set(X) & set(Y)) / min(len(set(X)) , len(set(Y)))


class LeftDotMeasure(DotMeasure):

    def similarity(self, X: Iterable[str], Y: Iterable[str]) -> float:
        return len(set(X) & set(Y)) / len(set(X)) 



class RightDotMeasure(DotMeasure):
    def similarity(self, X: Iterable[str], Y: Iterable[str]) -> float:
        return len(set(X) & set(Y)) / len(set(Y))
