# -*- coding:utf-8 -*-

import pytest
from collections import OrderedDict
from simstring.searcher import Searcher
from simstring.database.dict import DictDatabase
from simstring.measure.cosine import CosineMeasure
from simstring.measure.jaccard import JaccardMeasure
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor


@pytest.fixture
def cosine_searcher():
    strings = ["a", "ab", "abc", "abcd", "abcde"]
    db = DictDatabase(CharacterNgramFeatureExtractor(2))
    for string in strings:
        db.add(string)
    return Searcher(db, CosineMeasure())


@pytest.fixture
def ranked_cosine_searcher():
    db = DictDatabase(CharacterNgramFeatureExtractor(2))
    db.add("foo")
    db.add("bar")
    db.add("fooo")
    db.add("food")
    db.add("fool")
    db.add("follow")
    return Searcher(db, CosineMeasure())


@pytest.fixture
def ranked_cosine_long_searcher():
    db = DictDatabase(CharacterNgramFeatureExtractor(2))
    db.add("Amerikaplads 38 2200 Denmark")
    db.add("Viktoriagade 8E 1655 Denmark")
    db.add("Vesterbrogade 13 1655 Denmark")
    return Searcher(db, CosineMeasure())


@pytest.fixture
def ranked_jaccard_searcher():
    db = DictDatabase(CharacterNgramFeatureExtractor(2))
    db.add("foo")
    db.add("bar")
    db.add("fooo")
    db.add("food")
    db.add("fool")
    db.add("follow")
    return Searcher(db, JaccardMeasure())


# Test cases for CosineMeasure searcher
@pytest.mark.parametrize("query, threshold, expected_results", [
    ("a", 1.0, ["a"]),
    ("ab", 0.5, ["ab", "abc", "abcd"]),
    ("ab", 1.0, ["ab"]),
    ("ab", 0.9, ["ab"]),
    ("abc", 1.0, ["abc"]),
    ("abc", 0.9, ["abc"]),
    ("abcd", 1.0, ["abcd"]),
    ("abcd", 0.9, ["abcd"])
])
def test_searcher(cosine_searcher, query, threshold, expected_results):
    assert cosine_searcher.search(query, threshold) == expected_results


@pytest.mark.parametrize("query, threshold, expected_ranked_results", [
    ("abcd", 1.0, OrderedDict({"abcd": 1.0})),
    ("ab", 0.41, OrderedDict({
        "ab": 1.0,
        "abc": 0.5773502691896258,
        "abcd": 0.5163977794943222,
        "abcde": 0.47140452079103173
    }))
])
def test_ranked_search(cosine_searcher, query, threshold, expected_ranked_results):
    assert cosine_searcher.ranked_search(query, threshold) == expected_ranked_results


# Test cases for RankedSearchCosine
@pytest.mark.parametrize("query, threshold, expected_results", [
    ("fo", 0.5, OrderedDict({
        "foo": 0.8660254037844387,
        "fooo": 0.7745966692414834,
        "food": 0.5163977794943222,
        "fool": 0.5163977794943222
    })),
    ("fo", 0.6, OrderedDict({
        "foo": 0.8660254037844387,
        "fooo": 0.7745966692414834
    }))
])
def test_ranked_search_example(ranked_cosine_searcher, query, threshold, expected_results):
    assert ranked_cosine_searcher.ranked_search(query, threshold) == expected_results


# Test cases for RankedSearchCosine with longer addresses
@pytest.mark.parametrize("query, threshold, expected_results", [
    ("Vesterbrogade 15 1655 Denmark", 0.7, OrderedDict({
        "Vesterbrogade 13 1655 Denmark": 0.9333333333333333
    }))
])
def test_ranked_search_example_long(ranked_cosine_long_searcher, query, threshold, expected_results):
    assert ranked_cosine_long_searcher.ranked_search(query, threshold) == expected_results


# Test cases for RankedSearchJaccard
@pytest.mark.parametrize("query, threshold, expected_results", [
    ("fo", 0.5, OrderedDict({"foo": 0.75, "fooo": 0.6})),
    ("fo", 0.3, OrderedDict({
        "foo": 0.75,
        "fooo": 0.6,
        "food": 0.3333333333333333,
        "fool": 0.3333333333333333
    }))
])
def test_ranked_search_jaccard(ranked_jaccard_searcher, query, threshold, expected_results):
    assert ranked_jaccard_searcher.ranked_search(query, threshold) == expected_results


def test_deteminism():
    db = DictDatabase(CharacterNgramFeatureExtractor(2))
    db.add("fo")
    db.add("foo")
    db.add("fooo")
    db.add("foooo")
    db.add("fooooo")
    db.add("foooooo")
    db.add("fooooooo")
    db.add("foooooooo")
    db.add("fooooooooo")
    db.add("foooooooooo")
    db.add("fooooooooooo")
    db.add("foooooooooooo")
    db.add("fooooooooooooo")
    db.add("foooooooooooooo")
    db.add("fooooooooooooooo")
    searcher =  Searcher(db, CosineMeasure())
    result = searcher.search("foo", 0.8)
    # breakpoint()