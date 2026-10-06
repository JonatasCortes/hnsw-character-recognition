import time
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

import numpy as np

from src.domain import Label
from src.hnsw._progress import ProgressCallback


class ImageClassifier(Protocol):

    def classify(self, image: np.ndarray) -> str: ...


@dataclass(frozen=True)
class HnswTestReport:
    total_tests: int
    total_correct: int
    total_incorrect: int
    accuracy: float
    execution_time_per_test: float
    total_execution_time: float
    confusion_counts: Counter[tuple[str, str]]


class HnswTester:

    def run(self, classifier: ImageClassifier, images: Sequence[np.ndarray], labels: Sequence[int], on_progress: ProgressCallback | None = None) -> HnswTestReport:
        total_tests = len(images)
        if total_tests == 0:
            raise ValueError("No test images were provided.")
        if total_tests != len(labels):
            raise ValueError("images and labels must have the same length.")

        correct_count = 0
        confusion_counts: Counter[tuple[str, str]] = Counter()
        start = time.perf_counter()

        for test_number, (image, raw_label) in enumerate(zip(images, labels), start=1):
            expected_label = Label(raw_label)
            actual_label = classifier.classify(image)
            confusion_counts[(str(expected_label), str(actual_label))] += 1

            if actual_label == expected_label:
                correct_count += 1
            if on_progress is not None:
                on_progress(test_number / total_tests * 100)

        elapsed = time.perf_counter() - start
        return HnswTestReport(
            total_tests=total_tests,
            total_correct=correct_count,
            total_incorrect=total_tests - correct_count,
            accuracy=correct_count / total_tests,
            execution_time_per_test=elapsed / total_tests,
            total_execution_time=elapsed,
            confusion_counts=confusion_counts,
        )
