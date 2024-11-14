# -*- coding:utf-8 -*-

import pytest
from simstring.measure.jaccard import JaccardMeasure

# Instantiate the measure once for all tests
measure = JaccardMeasure()

@pytest.mark.parametrize("feature_count, similarity, expected_min_size", [
    (5, 1.0, 5),
    (5, 0.5, 3)
])
def test_min_feature_size(feature_count, similarity, expected_min_size):
    assert measure.min_feature_size(feature_count, similarity) == expected_min_size

@pytest.mark.parametrize("feature_count, similarity, expected_max_size", [
    (5, 1.0, 5),
    (5, 0.5, 10)
])
def test_max_feature_size(feature_count, similarity, expected_max_size):
    assert measure.max_feature_size(feature_count, similarity) == expected_max_size

@pytest.mark.parametrize("x_size, y_size, similarity, expected_count", [
    (5, 5, 1.0, 5),
    (5, 20, 1.0, 13),
    (5, 5, 0.5, 4)
])
def test_minimum_common_feature_count(x_size, y_size, similarity, expected_count):
    assert measure.minimum_common_feature_count(x_size, y_size, similarity) == expected_count

@pytest.mark.parametrize("x, y, expected_similarity", [
    (["1", "2", "3"], ["1", "2", "3"], 1.0),
    (["1", "2", "3"], ["1", "2", "3", "4"], 0.75),
    (["A", "AB", "BC", "C"], ["B", "BC", "CD", "DE", "E"], 0.125)
])
def test_similarity(x, y, expected_similarity):
    assert round(measure.similarity(x, y), 3) == expected_similarity
