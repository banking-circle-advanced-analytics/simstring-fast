# -*- coding:utf-8 -*-

from unittest import TestCase
from simstring.measure.dot import DotMeasure


class TestCosine(TestCase):
    measure = DotMeasure()

    def test_min_feature_size(self):
        # self.assertEqual(self.measure.min_feature_size(5, 1.0), 5)
        # self.assertEqual(self.measure.min_feature_size(5, 0.5), 2)
        ...

    def test_max_feature_size(self):
        # self.assertEqual(self.measure.max_feature_size(5, 1.0), 5)
        # self.assertEqual(self.measure.max_feature_size(5, 0.5), 20)
        ...

    def test_minimum_common_feature_count(self):
        # self.assertEqual(self.measure.minimum_common_feature_count(5, 5, 1.0), 5)
        # self.assertEqual(self.measure.minimum_common_feature_count(5, 20, 1.0), 10)
        # self.assertEqual(self.measure.minimum_common_feature_count(5, 5, 0.5), 3)
        ...

    def test_similarity(self):
        x = ["a", "ab", "bc", "c"]
        y = ["a", "ab", "bc", "cd", "e"]
        self.assertEqual(round(self.measure.similarity(x, x), 2), 1.0)
        self.assertEqual(round(self.measure.similarity(x, y), 2), 0.75)

        z = ["a", "ab", "ba", "ab", "a"]
        self.assertEqual(round(self.measure.similarity(z, z), 2), 1.0)
        self.assertEqual(round(self.measure.similarity(x, z), 2), 0.67)
        self.assertEqual(round(self.measure.similarity(y, z), 2), 0.67)

        # "vladimir putin"
        v = [" v", "vl", "la", "ad", "di", "mi", "ir", "r ", " p", "pu", "ut", "ti", "in", "n "]

        # "vladimir putin is my favorite president of russia"
        s = [" v", "vl", "la", "ad", "di", "mi", "ir", "r ", " p", "pu", "ut", "ti", "in", "n ", " i", "is", "s ", " m", "my", "y ", " f", "fa", "av", "vo", "or", "ri", "it", "te", "e ", " p", "pr", "re", "es", "si", "id", "de", "en", "nt", "t ", " o", "of", "f ", " r", "ru", "us", "ss", "si", "ia", "a "]

        # "vlad putin the impaler is no match for volodymyr zelenskyy"
        i = [" v", "vl", "la", "ad", "d ", " p", "pu", "ut", "ti", "in", "n ", " t", "th", "he", "e ", " i", "im", "mp", "pa", "al", "le", "er", "r ", " i", "is", "s ", " n", "no", "o ", " m", "ma", "at", "tc", "ch", "h ", " f", "fo", "or", "r ", " v", "vo", "ol", "lo", "od", "dy", "ym", "my", "yr", "r ", " z", "ze", "el", "le", "ns", "sk", "ky", "yy", "y "]

        self.assertEqual(round(self.measure.similarity(v, s), 2), 1)
        self.assertEqual(round(self.measure.similarity(v, i), 2), 0.79)
