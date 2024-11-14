# -*- coding:utf-8 -*-

import pytest
from simstring.database.dict import DictDatabase
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
import pickle
import os

# Sample strings used in multiple tests
strings = ["a", "ab", "abc", "abcd", "abcde"]

@pytest.fixture
def db():
    db = DictDatabase(CharacterNgramFeatureExtractor(2))
    for string in strings:
        db.add(string)
    return db

def test_strings(db):
    assert sorted(db.all()) == sorted(strings)

def test_lookup_strings_by_feature_set_size_and_feature(db):
    assert db.lookup_strings_by_feature_set_size_and_feature(4, "ab_1") == set(["abc"])
    assert db.lookup_strings_by_feature_set_size_and_feature(3, "ab_1") == set(["ab"])
    assert db.lookup_strings_by_feature_set_size_and_feature(2, "ab_1") == set([])

@pytest.fixture
def setup_multistep_save(db):
    with open("test.pkl", "wb") as f:
        db.to_pickle(f)
    yield "test.pkl"
    os.remove("test.pkl")

def test_multistep_save(db, setup_multistep_save):
    with open(setup_multistep_save, "rb") as f:
        data2 = pickle.load(f)
    new = DictDatabase.from_dict(data2)

    assert db._min_feature_size == new._min_feature_size
    assert db._max_feature_size == new._max_feature_size
    assert db.feature_extractor.__class__ == new.feature_extractor.__class__
    assert db.feature_extractor.n == new.feature_extractor.n
    assert db.feature_set_size_to_string_map == new.feature_set_size_to_string_map
    assert db.feature_set_size_and_feature_to_string_map == new.feature_set_size_and_feature_to_string_map

@pytest.fixture
def setup_compact_save(db):
    db.save("test2.pkl")
    yield "test2.pkl"
    os.remove("test2.pkl")

# def test_compact_save(db, setup_compact_save):
#     new = DictDatabase.load(setup_compact_save)

#     assert db._min_feature_size == new._min_feature_size
#     assert db._max_feature_size == new._max_feature_size
#     assert db.feature_extractor.__class__ == new.feature_extractor.__class__
#     assert db.feature_extractor.n == new.feature_extractor.n
#     assert db.feature_set_size_to_string_map == new.feature_set_size_to_string_map
#     assert db.feature_set_size_and_feature_to_string_map == new.feature_set_size_and_feature_to_string_map
