# -*- coding:utf-8 -*-

import pytest
from simstring.feature_extractor.word_ngram import WordNgramFeatureExtractor

@pytest.mark.parametrize("n, input_text, expected_features", [
    (2, "abcd", [(" ", "abcd"), ("abcd", " ")]),
    (2, "hello world", [(" ", "hello"), ("hello", "world"), ("world", " ")]),
    (3, "hello world", [(" ", "hello", "world"), ("hello", "world", " ")])
])
def test_features(n, input_text, expected_features):
    extractor = WordNgramFeatureExtractor(n)
    assert extractor.features(input_text) == expected_features
