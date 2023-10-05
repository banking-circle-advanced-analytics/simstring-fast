from collections import defaultdict
from typing import List, Set, Dict, Union
from .base import BaseDatabase
from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
from simstring.feature_extractor.word_ngram import WordNgramFeatureExtractor
import pickle
import ast
from io import BufferedWriter
from neo4j import GraphDatabase, RoutingControl


def defaultdict_set():
    return defaultdict(set)

class GDatabase(BaseDatabase):
    def __init__(
        self,
        feature_extractor: Union[
            CharacterNgramFeatureExtractor, WordNgramFeatureExtractor
        ],
        uri= "neo4j://localhost:7687"
    ):
        self.feature_extractor = feature_extractor
        self.strings: List[str] = []
        self.feature_set_size_to_string_map: Dict[int, Set[str]] = dict()
        self.feature_set_size_and_feature_to_string_map: dict = defaultdict(
            defaultdict_set
        )
        self.uri = uri
        
        # make this smarter:
        with GraphDatabase.driver(uri) as driver:
            self._add_node(driver, 9999999, "min_feature_size", "value")
            self._add_node(driver, 0, "max_feature_size", "value")
        self._min_feature_size = 9999999
        self._max_feature_size = 0

    def add(self, string: str) -> None:
        features = self.feature_extractor.features(string)
        size = len(features)

        with GraphDatabase.driver(self.uri) as driver:
            self._add_string_and_size(driver, string, size)

        for feature in features:
            self._add_string_size_and_feature(driver, string, size, feature)

    def all(self) -> List[str]:
        with GraphDatabase.driver(self.uri) as driver:
            return self._find_and_strings(driver)

    def lookup_strings_by_feature_set_size_and_feature(
        self, size: int, feature: str
    ) -> Set[str]:
        with GraphDatabase.driver(self.uri) as driver:
            return set(self._find_and_strings_by_size_and_feature(driver, size, feature))
    

    def _add_node(self, driver, data, data_key, node_type):
        if isinstance(data, str):
            driver.execute_query(f'MERGE (:{node_type} {{ {data_key}:"{data}" }})')
        elif isinstance(data, int):
            driver.execute_query(f"MERGE (:{node_type} {{ {data_key}:{data} }})")

    def _add_string_and_size(self, driver, string, size):
        driver.execute_query(
            "MERGE (string:string {string: $string}) "
            "MERGE (size:size {size: $size}) "
            "MERGE (string)-[:has]->(size)",
            string=string, size=size, database_="neo4j",
        )

    def _add_string_size_and_feature(self, driver, string, size, feature):
        driver.execute_query(
            "MERGE (string:string {string: $string}) "
            "MERGE (size:size {size: $size}) "
            "MERGE (feature:feature {feature: $feature}) "
            "MERGE (string)-[:has]->(size)"
            "MERGE (string)-[:has]->(feature)",
            string=string, size=size, feature=feature, database_="neo4j",
        )

    def _find_and_strings(self, driver):
        strings = driver.execute_query(
           "MATCH (s:string) "
            "RETURN s.string AS string",
            database_="neo4j",
            result_transformer_=lambda r: r.value("string")
        )
        return strings
    
    
    def _find_and_strings_by_size_and_feature(self, driver,size, feature):
        strings = driver.execute_query(
           "MATCH (feature:feature)<-[:has]-(string:string)-[:has]->(size:size)"
           "WHERE size.size = $size "
           "AND feature.feature = $feature "
            "RETURN string.string AS string",
            size=size,
            feature=feature,
            database_="neo4j",
            result_transformer_=lambda r: r.value("string")
        )
        return strings