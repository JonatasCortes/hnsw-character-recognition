from typing import Any

from src.domain import HNSW, Candidate, Position, Label
from src.services import SearchEngine, hamming_distance
from pathlib import Path
from collections import defaultdict
import numpy as np
import json


class HnswClassifier:

    @classmethod
    def download_hnsw(cls, file_path: Path):
        with file_path.open(mode="r", encoding="utf-8") as file:
            cls.__hnsw = HNSW(
                json.load(file, object_hook=cls.__restore_integer_keys))
            cls.__search_engine = SearchEngine(cls.__hnsw, hamming_distance)

    @classmethod
    def classify(cls, image: np.ndarray, max_candidates: int, image_sections: int, luminance_threshold: int) -> str:
        target_position = Position(image, image_sections, luminance_threshold)
        engine = cls.__search_engine

        top_layer_id = next(reversed(cls.__hnsw))
        pointer = next(iter(cls.__hnsw[top_layer_id]))

        for layer_id in reversed(cls.__hnsw):
            engine.explore_layer(target_position, layer_id,
                                 max_candidates, pointer)
            pointer = engine.get_nearest_neighbor()

        return cls.__extract_most_common_label(sorted(engine.get_candidates()))

    @classmethod
    def __extract_most_common_label(cls, candidates: list[Candidate]) -> str:
        if not candidates:
            raise ValueError("No candidates found for classification.")

        bottom_layer = cls.__hnsw[0]
        scores: defaultdict[int, float] = defaultdict(float)
        best_label = -1
        best_score = 0.0

        for candidate in candidates:
            label = bottom_layer[candidate.id]["label"]
            label_score_increment = 1 / (1 + candidate.distance_to_target)
            label_score = scores[label] + label_score_increment
            scores[label] = label_score

            if label_score > best_score:
                best_label = label
                best_score = label_score

        return Label(best_label)

    @staticmethod
    def __restore_integer_keys(obj: dict[Any, Any]) -> dict[int, Any]:
        if obj and all(key.isdigit() for key in obj):
            return {int(key): value for key, value in obj.items()}
        return obj
