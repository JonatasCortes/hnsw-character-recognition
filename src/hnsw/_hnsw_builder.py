from src.services import extract_balanced_training_images, extract_balanced_training_labels
from src.domain import HNSW
from src.services import NodeManager
from pathlib import Path
import json


class HnswBuilder:

    def __init__(self, file_path: Path, max_neighbors: int, max_candidates: int) -> None:
        self.__file_path = file_path
        self.__hnsw = HNSW()
        self.__node_inserter = NodeManager(self.__hnsw, max_neighbors,
                                           max_candidates)
        self.__progress: float = 0.0
        self.__done: bool = False

    def build(self) -> None:
        images = extract_balanced_training_images()
        labels = extract_balanced_training_labels()
        total_nodes = len(images)

        for target_id, (image, label) in enumerate(zip(images, labels)):
            self.__node_inserter.insert(target_id, image, label)
            self.__progress = (target_id + 1) / total_nodes * 100

        with self.__file_path.open(mode="w", encoding="utf-8") as file:
            json.dump(self.__hnsw, file, indent=4, ensure_ascii=False)

        self.__done = True

    def get_progress(self) -> float:
        return self.__progress

    def is_done(self) -> bool:
        return self.__done
