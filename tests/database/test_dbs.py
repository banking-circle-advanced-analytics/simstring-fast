## -*- coding:utf-8 -*-

import pytest
from simstring.database.dict import DictDatabase
from simstring.database.disk import DiskDatabase
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
import os
import shutil
from multiprocessing import Pool
from faker import Faker
import random

# Set up Faker
f = Faker()
Faker.seed(0)

# Fixture to create random strings
@pytest.fixture
def strings():
    return [f.name().replace('-', ' ') for _ in range(100)]

# Fixture for DictDatabase
@pytest.fixture
def dict_db(strings):
    db = DictDatabase(CharacterNgramFeatureExtractor(2))
    for string in strings:
        db.add(string)
    return db

# Fixture for DiskDatabase with setup and teardown
@pytest.fixture
def disk_db(strings):
    path = f"tmp_db_for_tests-{random.randint(1000,10000)}"
    db = DiskDatabase(CharacterNgramFeatureExtractor(2), path=path)
    with Pool(processes=8) as pool:
        for _ in pool.imap_unordered(db.add, strings):
            pass
    yield db
    shutil.rmtree(path, ignore_errors=True)

# Test to compare the contents of dict_db and disk_db
def test_strings(dict_db, disk_db):
    assert set(dict_db.all()) == set(disk_db.all())

# Test for equivalence from disk_db to dict_db
def test_equivalence_disk_to_dict(dict_db, disk_db):

    for key in disk_db.feature_set_size_to_string_map.iterkeys():
        assert dict_db.feature_set_size_to_string_map[key] == disk_db.feature_set_size_to_string_map[key]

    for key in disk_db.feature_set_size_and_feature_to_string_map.iterkeys():
        disk_val = disk_db.feature_set_size_and_feature_to_string_map[key]
        k1, k2 = key.split('-')
        dict_val = dict_db.feature_set_size_and_feature_to_string_map[int(k1)][k2]
        assert disk_val == dict_val

# Test for equivalence from dict_db to disk_db
def test_equivalence_dict_to_disk(dict_db, disk_db):
    for size, value in dict_db.feature_set_size_and_feature_to_string_map.items():
        for feature, dict_value in value.items():
            disk_value = disk_db.get_feature_set_size_and_feature_to_string_map(size, feature)
            assert dict_value == disk_value

    for size, string_set in dict_db.feature_set_size_to_string_map.items():
        assert string_set == disk_db.feature_set_size_to_string_map[size]
