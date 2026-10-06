from pathlib import Path

import numpy as np

from src.domain import HNSW
from src.hnsw._builder import HnswBuilder
from src.hnsw._classifier import HnswClassifier
from src.hnsw._parameters import HnswParameters
from src.hnsw._progress import ProgressTracker
from src.hnsw._storage import HnswStorage
from src.hnsw._tester import HnswTester, HnswTestReport
from src.services import (extract_balanced_testing_images,
                          extract_balanced_testing_labels,
                          extract_balanced_training_images,
                          extract_balanced_training_labels)

Dataset = tuple[list[np.ndarray], list[int]]


class Hnsw:

    def __init__(self, parameters: HnswParameters, model_file: Path | None = None, results_file: Path | None = None) -> None:
        self.__parameters = parameters
        self.__model_file = model_file
        self.__results_file = results_file
        self.__builder = HnswBuilder(parameters)
        self.__tester = HnswTester()
        self.__storage = HnswStorage()
        self.__classifier: HnswClassifier | None = None
        self.__training_set: Dataset | None = None
        self.__testing_set: Dataset | None = None
        self.__train_progress = ProgressTracker()
        self.__test_progress = ProgressTracker()
        self.__classification_progress = ProgressTracker()

    @classmethod
    def from_file(cls, model_file: Path) -> Hnsw:
        parameters, _ = HnswStorage().load_model(model_file)
        return cls(HnswParameters(**parameters), model_file=model_file)

    def get_parameters(self) -> HnswParameters:
        return self.__parameters

    def get_train_progress(self) -> float:
        return self.__train_progress.get_value()

    def is_train_done(self) -> bool:
        return self.__train_progress.is_done()

    def get_test_progress(self) -> float:
        return self.__test_progress.get_value()

    def is_test_done(self) -> bool:
        return self.__test_progress.is_done()

    def is_classification_done(self) -> bool:
        return self.__classification_progress.is_done()

    def train(self, ignore_cache: bool = False) -> None:
        self.__train_progress.reset()

        if not ignore_cache and self.__has_reusable_model():
            self.__train_progress.finish()
            return

        images, labels = self.__get_training_set()
        hnsw = self.__builder.build(images, labels,
                                    self.__train_progress.update)
        self.__use_model(hnsw)

        if self.__model_file is not None:
            self.__storage.save_model(self.__model_file, self.__parameters,
                                      hnsw)
        self.__train_progress.finish()

    def test(self) -> HnswTestReport:
        classifier = self.__get_classifier()
        self.__test_progress.reset()

        images, labels = self.__get_testing_set()
        report = self.__tester.run(classifier, images, labels,
                                   self.__test_progress.update)

        if self.__results_file is not None:
            self.__storage.save_report(self.__results_file, self.__parameters,
                                       report)
        self.__test_progress.finish()
        return report

    def classify(self, image: np.ndarray) -> str:
        self.__classification_progress.reset()
        classification = self.__get_classifier().classify(image)
        self.__classification_progress.finish()
        return classification

    def __has_reusable_model(self) -> bool:
        if self.__classifier is not None:
            return True
        hnsw = self.__try_load_model()
        if hnsw is None:
            return False
        self.__use_model(hnsw)
        return True

    def __get_classifier(self) -> HnswClassifier:
        if self.__classifier is not None:
            return self.__classifier

        hnsw = self.__try_load_model()
        if hnsw is None:
            raise RuntimeError(
                "No trained model matching the current parameters is available. Call train() first.")
        return self.__use_model(hnsw)

    def __use_model(self, hnsw: HNSW) -> HnswClassifier:
        self.__classifier = HnswClassifier(hnsw, self.__parameters)
        return self.__classifier

    def __try_load_model(self) -> HNSW | None:
        if self.__model_file is None or not self.__model_file.exists():
            return None

        stored_parameters, hnsw = self.__storage.load_model(self.__model_file)
        if stored_parameters != self.__parameters.to_dict():
            return None
        return hnsw

    def __get_training_set(self) -> Dataset:
        if self.__training_set is None:
            self.__training_set = (
                list(extract_balanced_training_images()),
                [int(label) for label in extract_balanced_training_labels()],
            )
        return self.__training_set

    def __get_testing_set(self) -> Dataset:
        if self.__testing_set is None:
            self.__testing_set = (
                list(extract_balanced_testing_images()),
                [int(label) for label in extract_balanced_testing_labels()],
            )
        return self.__testing_set
