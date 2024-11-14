# -*- coding:utf-8 -*-

import pytest
from simstring.measure.overlap import OverlapMeasure, LeftOverlapMeasure

maxsize = 5

# Initialize measure instances for both overlap types
overlap_measure = OverlapMeasure(maxsize=maxsize)
left_overlap_measure = LeftOverlapMeasure(maxsize=maxsize)

# Test cases for OverlapMeasure
@pytest.mark.parametrize("feature_count, similarity, expected_min_size", [
    (5, 1.0, 5),
    (5, 0.5, 2)
])
def test_overlap_min_feature_size(feature_count, similarity, expected_min_size):
    assert overlap_measure.min_feature_size(feature_count, similarity) == expected_min_size

@pytest.mark.parametrize("feature_count, similarity, expected_max_size", [
    (5, 1.0, maxsize),
    (5, 0.5, maxsize)
])
def test_overlap_max_feature_size(feature_count, similarity, expected_max_size):
    assert overlap_measure.max_feature_size(feature_count, similarity) == expected_max_size

@pytest.mark.parametrize("x_size, y_size, similarity, expected_count", [
    (5, 5, 1.0, 5),
    (5, 20, 1.0, 5),
    (5, 5, 0.5, 3)
])
def test_overlap_minimum_common_feature_count(x_size, y_size, similarity, expected_count):
    assert overlap_measure.minimum_common_feature_count(x_size, y_size, similarity) == expected_count

@pytest.mark.parametrize("x, y, expected_similarity", [
    ([1, 2, 3], [1, 2, 3], 3),
    ([1, 2, 3], [1, 2, 3, 4], 3),
    ([1, 2, 3], [1, 1, 2, 3], 3),
    ([1, 2, 3, 4], [1, 1, 2, 3], 3),
    ([1, 1, 2, 3], [1, 1, 2, 3], 3)
])
def test_overlap_similarity(x, y, expected_similarity):
    assert round(overlap_measure.similarity(x, y), 2) == expected_similarity

# Test cases for LeftOverlapMeasure
@pytest.mark.parametrize("feature_count, similarity, expected_min_size", [
    (5, 1.0, 5),
    (5, 0.5, 2)
])
def test_left_overlap_min_feature_size(feature_count, similarity, expected_min_size):
    assert left_overlap_measure.min_feature_size(feature_count, similarity) == expected_min_size

@pytest.mark.parametrize("feature_count, similarity, expected_max_size", [
    (5, 1.0, maxsize),
    (5, 0.5, maxsize)
])
def test_left_overlap_max_feature_size(feature_count, similarity, expected_max_size):
    assert left_overlap_measure.max_feature_size(feature_count, similarity) == expected_max_size

@pytest.mark.parametrize("x_size, y_size, similarity, expected_count", [
    (5, 5, 1.0, 5),
    (5, 20, 1.0, 5),
    (5, 5, 0.5, 2)
])
def test_left_overlap_minimum_common_feature_count(x_size, y_size, similarity, expected_count):
    assert left_overlap_measure.minimum_common_feature_count(x_size, y_size, similarity) == expected_count

@pytest.mark.parametrize("x, y, expected_similarity", [
    ([1, 2, 3], [1, 2, 3], 1.0),
    ([1, 2, 3], [1, 2, 3, 4], 1.0),
    ([1, 2, 3], [1, 1, 2, 3], 1.0),
    ([1, 2, 3, 4], [1, 1, 2, 3], 0.75),
    ([1, 1, 2, 3], [1, 1, 2, 3], 1.0)
])
def test_left_overlap_similarity(x, y, expected_similarity):
    assert round(left_overlap_measure.similarity(x, y), 2) == expected_similarity
