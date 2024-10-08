# -*- coding:utf-8 -*-

from unittest import TestCase
from simstring.database.disk import DiskDatabase
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
import random
import pickle
import os
import shutil

class TestDisk(TestCase):
    strings = ["a", "ab", "abc", "abcd", "abcde"]

    def setUp(self):
        self.db = DiskDatabase(CharacterNgramFeatureExtractor(2), path=f"tmp_db_for_tests-{random.randint(1000,10000)}")
        for string in self.strings:
            self.db.add(string)

    
    def tearDown(self) -> None:
        try:
            shutil.rmtree(self.disk_db.path)
        except:
            pass
        return super().tearDown()

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

    def test_load_from_folder(self):

        with open("test.pkl", "wb") as f:
            pickle.dump(self.db, f)

        
        with open("test.pkl", "rb") as f:
            new =  pickle.load(f)

        self.assertEqual(
            self.db.feature_extractor.__class__, new.feature_extractor.__class__
        )
        self.assertEqual(self.db.feature_extractor.n, new.feature_extractor.n)
        self.assertEqual(
            set(self.db.feature_set_size_to_string_map.iterkeys()), set(new.feature_set_size_to_string_map.iterkeys())
        )
        self.assertEqual(
            set(self.db.feature_set_size_and_feature_to_string_map.iterkeys()),
            set(new.feature_set_size_and_feature_to_string_map.iterkeys()),
        )

        os.remove("test.pkl")
