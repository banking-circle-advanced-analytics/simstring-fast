class BaseDatabase:
    def __init__(self, feature_extractor):
        raise NotImplementedError

    def add(self, string):
        raise NotImplementedError

    def min_feature_size(self):
        raise NotImplementedError

    def max_feature_size(self):
        raise NotImplementedError

    def lookup_strings_by_feature_set_size_and_feature(self, size, feature):
        raise NotImplementedError

    def __getstate__(self):
        """To pickle the object"""
        return self.__dict__

    def __setstate__(self, d):
        """To unpickle the object"""
        self.__dict__ = d