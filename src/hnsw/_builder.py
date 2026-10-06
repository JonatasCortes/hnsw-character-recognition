from collections.abc import Sequence

import numpy as np

from src.domain import HNSW
from src.hnsw._parameters import HnswParameters
from src.hnsw._progress import ProgressCallback
from src.services import NodeManager


class HnswBuilder:

    def __init__(self, parameters: HnswParameters) -> None:
        self.__parameters = parameters

    def build(self, images: Sequence[np.ndarray], labels: Sequence[int], on_progress: ProgressCallback | None = None) -> HNSW:
        if len(images) != len(labels):
            raise ValueError("images and labels must have the same length.")

        hnsw = HNSW()
        node_manager = self.__create_node_manager(hnsw)
        order = self.__shuffled_order(len(images))
        shuffled_images = [images[index] for index in order]
        shuffled_labels = [labels[index] for index in order]
        node_manager.plan_layers(shuffled_labels)
        total_nodes = len(shuffled_images)

        for target_id, (image, label) in enumerate(zip(shuffled_images, shuffled_labels)):
            node_manager.insert(target_id, image, label)
            if on_progress is not None:
                on_progress((target_id + 1) / total_nodes * 100)

        return hnsw

    def __create_node_manager(self, hnsw: HNSW) -> NodeManager:
        parameters = self.__parameters
        return NodeManager(hnsw,
                           parameters.max_neighbors,
                           parameters.construction_max_candidates,
                           parameters.image_sections,
                           parameters.luminance_threshold,
                           parameters.resolved_layer_growth_factor)

    def __shuffled_order(self, size: int) -> list[int]:
        generator = np.random.default_rng(self.__parameters.shuffle_seed)
        return generator.permutation(size).tolist()
