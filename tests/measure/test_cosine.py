# -*- coding:utf-8 -*-

import pytest
from simstring.measure.cosine import CosineMeasure

# Instantiate the measure only once for all tests
measure = CosineMeasure()

@pytest.mark.parametrize("feature_count, similarity, expected_min_size", [
    (5, 1.0, 5),
    (5, 0.5, 2)
])
def test_min_feature_size(feature_count, similarity, expected_min_size):
    assert measure.min_feature_size(feature_count, similarity) == expected_min_size

@pytest.mark.parametrize("feature_count, similarity, expected_max_size", [
    (5, 1.0, 5),
    (5, 0.5, 20)
])
def test_max_feature_size(feature_count, similarity, expected_max_size):
    assert measure.max_feature_size(feature_count, similarity) == expected_max_size

@pytest.mark.parametrize("x_size, y_size, similarity, expected_count", [
    (5, 5, 1.0, 5),
    (5, 20, 1.0, 10),
    (5, 5, 0.5, 3)
])
def test_minimum_common_feature_count(x_size, y_size, similarity, expected_count):
    assert measure.minimum_common_feature_count(x_size, y_size, similarity) == expected_count

@pytest.mark.parametrize("x, y, expected_similarity", [
    (["a", "ab", "bc", "c"], ["a", "ab", "bc", "c"], 1.0),
    (["a", "ab", "bc", "c"], ["a", "ab", "bc", "cd", "e"], 0.67),
    (["a", "ab", "ba", "ab", "a"], ["a", "ab", "ba", "ab", "a"], 1.0),
    (["a", "ab", "bc", "c"], ["a", "ab", "ba", "ab", "a"], 0.58),
    (
        [
            ' "m', '"me', "met", "eth", "thy", "hyl", "yl ", "l s", " su", "sul",
            "ulf", "lfo", "fon", "one", 'ne"', 'e" '
        ],
        [
            ' "m', '"me', "met", "eth", "thy", "hyl", "yl ", "l s", " su", "sul",
            "ulp", "lph", "pho", "hon", "one", 'ne"', 'e" '
        ],
        0.79
    )
])
def test_similarity(x, y, expected_similarity):
    assert round(measure.similarity(x, y), 2) == expected_similarity
