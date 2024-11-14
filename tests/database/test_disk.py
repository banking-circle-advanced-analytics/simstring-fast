# -*- coding:utf-8 -*-

import pytest
import random
import pickle
import os
import shutil
from simstring.database.disk import DiskDatabase
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor


@pytest.fixture
def disk_db():
    # Setup the DiskDatabase with a random temporary path and add strings
    db = DiskDatabase(CharacterNgramFeatureExtractor(2), path=f"tmp_db_for_tests-{random.randint(1000, 10000)}")
    strings = ["a", "ab", "abc", "abcd", "abcde"]
    for string in strings:
        db.add(string)
    yield db
    # Teardown: Remove the database folder after test is completed
    shutil.rmtree(db.path, ignore_errors=True)


# Test case to check the strings stored in the database
def test_strings(disk_db):
    expected_strings = ["a", "ab", "abc", "abcd", "abcde"]
    assert sorted(disk_db.all()) == sorted(expected_strings)


# Test case for lookup functionality by feature set size and feature
@pytest.mark.parametrize("feature_size, feature, expected_result", [
    (4, "ab_1", {"abc"}),
    (3, "ab_1", {"ab"}),
    (2, "ab_1", set()),
])
def test_lookup_strings_by_feature_set_size_and_feature(disk_db, feature_size, feature, expected_result):
    result = disk_db.lookup_strings_by_feature_set_size_and_feature(feature_size, feature)
    assert result == expected_result


# Test case to test saving and loading the database using pickle
def test_load_from_folder(disk_db):
    # Save the database to a pickle file
    with open("test.pkl", "wb") as f:
        pickle.dump(disk_db, f)

    # Load the database from the pickle file
    with open("test.pkl", "rb") as f:
        loaded_db = pickle.load(f)

    # Validate the features and mappings
    assert disk_db.feature_extractor.__class__ == loaded_db.feature_extractor.__class__
    assert disk_db.feature_extractor.n == loaded_db.feature_extractor.n
    assert set(disk_db.feature_set_size_to_string_map.iterkeys()) == set(loaded_db.feature_set_size_to_string_map.iterkeys())
    assert set(disk_db.feature_set_size_and_feature_to_string_map.iterkeys()) == set(loaded_db.feature_set_size_and_feature_to_string_map.iterkeys())

    # Clean up the pickle file after test
    os.remove("test.pkl")
