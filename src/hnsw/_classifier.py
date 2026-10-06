from collections import defaultdict

import numpy as np

from src.domain import HNSW, Candidate, Label, Position
from src.hnsw._parameters import HnswParameters
from src.services import SearchEngine, hamming_distance


class HnswClassifier:

    def __init__(self, hnsw: HNSW, parameters: HnswParameters) -> None:
        if not hnsw:
            raise ValueError("The HNSW graph is empty.")

        self.__parameters = parameters
        self.__search_engine = SearchEngine(hnsw, hamming_distance)
        self.__bottom_layer = hnsw[0]
        self.__layer_ids = sorted(hnsw, reverse=True)
        self.__entry_node_id = next(iter(hnsw[self.__layer_ids[0]]))

    def classify(self, image: np.ndarray) -> str:
        parameters = self.__parameters
        target_position = Position(image, parameters.image_sections,
                                   parameters.luminance_threshold)
        engine = self.__search_engine
        pointer = self.__entry_node_id

        for layer_id in self.__layer_ids:
            engine.explore_layer(target_position, layer_id,
                                 parameters.classification_max_candidates,
                                 pointer)
            pointer = engine.get_nearest_neighbor()

        return self.__extract_most_common_label(sorted(engine.get_candidates()))

    def __extract_most_common_label(self, candidates: list[Candidate]) -> str:
        if not candidates:
            raise ValueError("No candidates found for classification.")

        scores: defaultdict[int, float] = defaultdict(float)
        best_label = -1
        best_score = 0.0

        for candidate in candidates:
            label = self.__bottom_layer[candidate.id]["label"]
            label_score = scores[label] + 1 / \
                (1 + candidate.distance_to_target)
            scores[label] = label_score

            if label_score > best_score:
                best_label = label
                best_score = label_score

        return Label(best_label)
