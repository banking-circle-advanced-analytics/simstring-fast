from collections.abc import Iterable


class BaseMeasure:
    def min_feature_size(self,  query_size: int, alpha: float) -> int:
        raise NotImplementedError

    def max_feature_size(self, query_size: int, alpha: float) -> int:
        raise NotImplementedError

    def minimum_common_feature_count(self, query_size: int, y_size: int, alpha: float) -> int:
        raise NotImplementedError

    def similarity(self, X: Iterable[str], Y: Iterable[str]) -> float:
        raise NotImplementedError
