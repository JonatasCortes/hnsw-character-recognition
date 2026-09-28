from pathlib import Path
from src.domain import Label
from src.hnsw import HnswClassifier
from collections import Counter
from src.services import extract_balanced_testing_images, extract_balanced_testing_labels
import time
import json


class HnswTester:

    def __init__(self, hnsw_file: Path, results_file: Path, max_candidates: int) -> None:
        self.__max_candidates = max_candidates
        self.__hnsw_file = hnsw_file
        self.__results_file = results_file
        self.__reset_state()

    def run(self):
        self.__reset_state()
        start = time.perf_counter()
        self.__run_tests()
        elapsed = time.perf_counter() - start
        self.__save_results(elapsed)
        self.__done = True

    def get_progress(self):
        return self.__progress

    def is_done(self):
        return self.__done

    def __reset_state(self):
        self.__progress: float = 0.0
        self.__done: bool = False
        self.__tests_count: int = 0
        self.__correct_count: int = 0
        self.__incorrect_count: int = 0
        self.__inconclusive_count: int = 0
        self.__confusion_counts: Counter[tuple[str, str]] = Counter()

    def __run_tests(self):
        images = extract_balanced_testing_images()
        labels = extract_balanced_testing_labels()
        HnswClassifier.download_hnsw(self.__hnsw_file)

        for image, raw_label in zip(images, labels):
            self.__tests_count += 1
            self.__progress = (self.__tests_count / len(images)) * 100
            expected_label = Label(raw_label)
            actual_label = HnswClassifier.classify(
                image, self.__max_candidates)
            self.__update_results(expected_label, actual_label)

    def __update_results(self, expected_label: Label, actual_label: str):
        self.__confusion_counts[(str(expected_label), str(actual_label))] += 1

        if actual_label == "n/a":
            self.__inconclusive_count += 1
        elif actual_label == expected_label:
            self.__correct_count += 1
            return
        self.__incorrect_count += 1

    def __save_results(self, elapsed_time: float):
        with self.__results_file.open(mode="w", encoding="utf-8") as file:
            json.dump(
                {
                    "max_candidates": self.__max_candidates,
                    "total_tests": self.__tests_count,
                    "total_correct": self.__correct_count,
                    "total_incorrect": self.__incorrect_count,
                    "total_inconclusive": self.__inconclusive_count,
                    "acuracy": self.__correct_count / self.__tests_count,
                    "execution_time_per_test": elapsed_time / self.__tests_count,
                    "total_execution_time": elapsed_time,
                    "confusion_matrix": [
                        {"expected": expected, "actual": actual, "count": count}
                        for (expected, actual), count in self.__confusion_counts.items()
                    ],
                }, file, indent=4, ensure_ascii=False
            )
