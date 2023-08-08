# -*- coding:utf-8 -*-

from unittest import TestCase
from simstring.measure.left_cosine import LeftCosineMeasure


class TestLeftCosineMeasure(TestCase):
    measure = LeftCosineMeasure()

    def test_min_feature_size(self):
        self.assertEqual(self.measure.min_feature_size(5, 1.0), 5)
        self.assertEqual(self.measure.min_feature_size(5, 0.5), 2)

    def test_max_feature_size(self):
        self.assertEqual(self.measure.max_feature_size(5, 1.0), 5)
        self.assertEqual(self.measure.max_feature_size(5, 0.5), 20)

    def test_minimum_common_feature_count(self):
        self.assertEqual(self.measure.minimum_common_feature_count(5, 5, 1.0), 5)
        self.assertEqual(self.measure.minimum_common_feature_count(5, 20, 1.0), 10)
        self.assertEqual(self.measure.minimum_common_feature_count(5, 5, 0.5), 3)

    def test_similarity(self):
        x = ["a", "ab", "bc", "c"]
        y = ["a", "ab", "bc", "cd", "e"]
        self.assertEqual(round(self.measure.similarity(x, x), 2), 1.0)
        self.assertEqual(round(self.measure.similarity(x, y), 2), 0.75)

        z = ["a", "ab", "ba", "ab", "a"]
        self.assertEqual(round(self.measure.similarity(z, z), 2), 1.0)
        self.assertEqual(round(self.measure.similarity(x, z), 2), 0.5)
        self.assertEqual(round(self.measure.similarity(x, y), 2), 0.75)

        # Test as per paper trigrams with quotes of methyl sulphone and methyl sulfone
        a = [
            ' "m',
            '"me',
            "met",
            "eth",
            "thy",
            "hyl",
            "yl ",
            "l s",
            " su",
            "sul",
            "ulf",
            "lfo",
            "fon",
            "one",
            'ne"',
            'e" ',
        ]
        b = [
            ' "m',
            '"me',
            "met",
            "eth",
            "thy",
            "hyl",
            "yl ",
            "l s",
            " su",
            "sul",
            "ulp",
            "lph",
            "pho",
            "hon",
            "one",
            'ne"',
            'e" ',
        ]
        self.assertEqual(
            round(self.measure.similarity(a, b), 3), 0.812
        )

        name = ["Vl", "la", "ad", "di", "im", "mi", "ir", "r ", " P", "Pu", "ut", "ti", "in"]
        sentence = ["Do", "on", "na", "at", "ti", "io", "on", "n ", " t", "to", "o ", " t", "he", "e ", " g", "gr", "re", "ea", "at", "t ", " V", "Vl", "la", "ad", "di", "im", "mi", "ir", "r ", " P", "Pu", "ut", "ti", "in", "n ", " m", "my", "y ", " f", "fa", "av", "vo", "or", "ri", "it", "te", "e ", " p", "pr", "re", "es", "si", "id", "de", "en", "nt"]
        self.assertEqual(
            round(self.measure.similarity(name, sentence), 2), 1.0
        )
