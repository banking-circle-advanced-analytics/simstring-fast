# -*- coding:utf-8 -*-

import pytest
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor

@pytest.mark.parametrize("n, input_text, expected_features", [
    (2, "abcde", ["$a_1", "ab_1", "bc_1", "cd_1", "de_1", "e$_1"]),
    (3, "abcde", ["$$a_1", "$ab_1", "abc_1", "bcd_1", "cde_1", "de$_1", "e$$_1"]),
    (2, "あいうえお", ["$あ_1", "あい_1", "いう_1", "うえ_1", "えお_1", "お$_1"]),  # Japanese text
    (2, "marc anthony", [
        '$m_1', 'ma_1', 'ar_1', 'rc_1', 'c _1', ' a_1', 'an_1', 'nt_1', 'th_1', 
        'ho_1', 'on_1', 'ny_1', 'y$_1'
    ]),
    (2, "anthony marc", [
        '$a_1', 'an_1', 'nt_1', 'th_1', 'ho_1', 'on_1', 'ny_1', 'y _1', 
        ' m_1', 'ma_1', 'ar_1', 'rc_1', 'c$_1'
    ])
])
def test_features(n, input_text, expected_features):
    extractor = CharacterNgramFeatureExtractor(n)
    assert extractor.features(input_text) == expected_features


def test_endmarker():
    c_end = CharacterNgramFeatureExtractor(endmarker=" ")
    assert set(c_end.features("marc anthony")) == set(c_end.features("anthony marc"))