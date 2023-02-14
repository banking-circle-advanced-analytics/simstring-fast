class BaseMeasure:
    def min_feature_size(self, _query_size, _alpha) -> int:
        raise NotImplementedError

    def max_feature_size(self, _query_size, _alpha) -> int:
        raise NotImplementedError

    def minimum_common_feature_count(self, _query_size, _y_size, _alpha) -> int:
        raise NotImplementedError

    def similarity(self, X, Y) -> float:
        raise NotImplementedError

    def __getstate__(self):
        """To pickle the object"""
        return self.__dict__

    def __setstate__(self, d):
        """To unpickle the object"""
        self.__dict__ = d