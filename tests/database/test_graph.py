# -*- coding:utf-8 -*-

from unittest import TestCase
from simstring.database.graph import GDatabase
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
import pickle
import os


class TestGraph(TestCase):
    strings = ["a", "ab", "abc", "abcd", "abcde"]

    def setUp(self):
        self.db = GDatabase(CharacterNgramFeatureExtractor(2))
        for string in self.strings:
            self.db.add(string)

    def test_strings(self):
        self.assertEqual(sorted(self.db.all()), sorted(self.strings))


    def test_lookup_strings_by_feature_set_size_and_feature(self):
        self.assertEqual(
            self.db.lookup_strings_by_feature_set_size_and_feature(4, "ab_1"),
            set(["abc"]),
        )
        self.assertEqual(
            self.db.lookup_strings_by_feature_set_size_and_feature(3, "ab_1"),
            set(["ab"]),
        )
        self.assertEqual(
            self.db.lookup_strings_by_feature_set_size_and_feature(2, "ab_1"), set([])
        )
