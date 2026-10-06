# HNSW for Image Classification

A from-scratch Python implementation of **HNSW** (*Hierarchical Navigable Small World*) applied to handwritten character classification on the **EMNIST Balanced** dataset. Images are encoded as binary integers, compared with the Hamming distance, and classified by searching for their nearest neighbors in a hierarchical graph.

Unlike the original algorithm, this project assigns nodes to layers **deterministically** (see [section 4](#4-modifications-to-the-original-hnsw)).

---

## Table of Contents

- [1. Getting Started](#1-getting-started)
- [2. Overview](#2-overview)
  - [2.1 Goal and Approach](#21-goal-and-approach)
  - [2.2 Dataset](#22-dataset)
  - [2.3 Technologies](#23-technologies)
- [3. The Original HNSW](#3-the-original-hnsw)
  - [3.1 The Problem](#31-the-problem)
  - [3.2 What the Name Means](#32-what-the-name-means)
  - [3.3 Layers](#33-layers)
  - [3.4 Search](#34-search)
  - [3.5 Insertion](#35-insertion)
- [4. Modifications to the Original HNSW](#4-modifications-to-the-original-hnsw)
  - [4.1 Summary](#41-summary)
  - [4.2 Layer Growth Factor](#42-layer-growth-factor)
  - [4.3 Determinism](#43-determinism)
  - [4.4 Advantages and Drawbacks](#44-advantages-and-drawbacks)
- [5. Image Representation and Distance](#5-image-representation-and-distance)
  - [5.1 From Image to Position](#51-from-image-to-position)
  - [5.2 Example](#52-example)
  - [5.3 Hamming Distance](#53-hamming-distance)
- [6. Building the Index](#6-building-the-index)
- [7. Classification](#7-classification)
- [8. The Hnsw Class](#8-the-hnsw-class)
  - [8.1 Parameters](#81-parameters)
  - [8.2 Services](#82-services)
  - [8.3 Usage](#83-usage)
- [9. Training, Testing and Metrics](#9-training-testing-and-metrics)
- [10. Project Structure](#10-project-structure)

---

## 1. Getting Started

**Requires Python 3.14 or newer** (the project relies on `heapq` max-heap support introduced in 3.14).

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Windows (PowerShell)**

```powershell
py -3.14 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

On Windows CMD, activate with `.venv\Scripts\activate.bat` instead.

`main.py` opens the interface for training and testing the model.

---

## 2. Overview

### 2.1 Goal and Approach

The goal is to classify handwritten characters efficiently. Classification follows the **k-nearest neighbors** idea: a new image receives the label of the training images most similar to it. The expensive part of k-NN is finding those neighbors, since comparing a query against every training image is slow.

HNSW replaces this exhaustive search with an **approximate nearest neighbor** search over a graph, trading a small amount of accuracy for a large gain in speed.

### 2.2 Dataset

Experiments use **EMNIST Balanced**: grayscale handwritten characters in **47 classes**.

| Group | Characters |
|---|---|
| Digits | `0`–`9` |
| Uppercase | `A`–`Z` |
| Lowercase | `a b d e f g h n q r t` |

### 2.3 Technologies

| Technology | Use |
|---|---|
| Python 3.14 | Language |
| NumPy | Image manipulation |
| Desklab | Interface |

---

## 3. The Original HNSW

> This section describes the original algorithm (Malkov and Yashunin). The changes made in this project are in [section 4](#4-modifications-to-the-original-hnsw).

### 3.1 The Problem

Given a set of elements and a query, find the elements closest to the query under a distance metric. HNSW builds a **proximity graph** where each element is linked to some of its near neighbors, and searches by walking the graph instead of scanning every element.

### 3.2 What the Name Means

| Part | Meaning |
|---|---|
| **Hierarchical** | The graph is organized in **layers**. Upper layers have few nodes and long-range links; the bottom layer holds every node. |
| **Navigable** | Greedy navigation works: starting anywhere and always moving to the neighbor closest to the query leads to a region near the answer. |
| **Small World** | Any two nodes are connected by a short path. |

### 3.3 Layers

Layer 0 contains **all** elements, and each higher layer contains a subset of the layer below it. Each element's top layer is drawn from an exponentially decaying distribution:

> the higher the layer, the lower the probability that a node reaches it.

This sparsity is intentional. With few nodes, links in upper layers are **long** and act as highways that quickly bring the search close to the right region, the same principle as a *skip list*.

### 3.4 Search

1. Start at an **entry point** in the top layer.
2. In each layer, walk greedily toward neighbors closer to the query until no neighbor improves the distance.
3. The best node found becomes the entry point of the next layer down.
4. In layer 0, the search is more thorough: it keeps a bounded list of candidates and returns the best ones.

Only the nodes along a path (and their neighborhoods) are visited, so cost grows roughly **logarithmically** with the number of elements instead of linearly. The price is that the result is *approximate*, and the graph needs extra memory for its links.

### 3.5 Insertion

1. Draw the new element's top layer.
2. Descend greedily from the top down to that layer to find a good entry point.
3. In each layer from the element's top layer to 0, find nearby candidates and pick neighbors with a **selection heuristic** that favors neighbors in different directions rather than only the closest ones.
4. Links are **bidirectional**. A neighbor that exceeds its connection limit is pruned.

---

## 4. Modifications to the Original HNSW

### 4.1 Summary

| Aspect | Original HNSW | This project |
|---|---|---|
| Top layer of each node | Random, drawn from an exponential distribution | **Planned deterministically** from `layer_growth_factor` |
| Number of layers | Outcome of the random draws | **Computed** from the number of nodes, classes and `layer_growth_factor` |
| Distribution across classes | Ignores labels | Every layer has **balanced quantities per class** |

### 4.2 Layer Growth Factor

`layer_growth_factor` indirectly controls the number of layers. Counting from the top layer, the size of each layer is:

```python
size = round(num_classes * layer_growth_factor ** depth)
```

The last layer is capped at the total number of nodes, so sizes are computed until they reach or exceed that total. The number of layers is approximately `ceil(log(num_nodes / num_classes)) + 1`, with the logarithm in base `layer_growth_factor`.

> [!IMPORTANT]
> `depth` is not the layer id. The formula counts from the top (`depth = 0` is the highest layer), while layer ids count from the bottom: layer `0` is the largest and contains every node.

Larger values produce **fewer layers with bigger jumps in size**; smaller values produce **more layers and a smoother transition**. By default (`None`), `max_neighbors` is used.

> Experimentally, when `layer_growth_factor` is close to the maximum number of neighbors per node, the layer distribution approaches that of the original HNSW.

**Example (EMNIST Balanced, `layer_growth_factor = 16`):** 47 classes, 112,800 training nodes.

| Layer id | Nodes in layer |
|---|---:|
| 3 (top) | 47 |
| 2 | 752 |
| 1 | 12,032 |
| 0 (bottom) | 112,800 |

Layers are nested: a node present in a layer is also present in every layer below it. Within each layer, nodes are split **evenly across classes**. Classes with few samples contribute all they have, and the rest is shared equally among the remaining classes. As a result, the top layer holds exactly one node per class, and every layer keeps all classes represented.

### 4.3 Determinism

A node's layer is a function of the labels, the insertion order and `layer_growth_factor`, with nothing drawn at random. To avoid bias from the way the dataset is organized, the training set is shuffled with a fixed seed (`shuffle_seed`) before insertion. The same data and parameters always produce **the same index**.

### 4.4 Advantages and Drawbacks

**Advantages**

- **Reproducible**: same data and parameters give the same index.
- **Explicit control**: the number and size of layers are known before building and tuned with a single parameter.
- **Full class coverage** in every layer, including the top, so the search starts in a region that already represents every class.

**Drawbacks**

- **Needs the full dataset and labels up front.** Layers are planned over the complete set, so there is no incremental insertion.
- Using **labels inside the structure** is specific to supervised classification; the original HNSW is label-agnostic.
- Performance depends on the **insertion order**, hence the seeded shuffle.

---

## 5. Image Representation and Distance

### 5.1 From Image to Position

Each EMNIST image is converted into a `Position`, an integer whose bits encode the image:

1. **Binarization**: pixels strictly greater than `luminance_threshold` become `1`, the rest `0`. Strokes must therefore be **light** on a **dark** background.
2. **Cropping**: the matrix is cropped to the smallest rectangle containing all `1` pixels, making the representation independent of where the character sits in the image.
3. **Normalization**: the crop is resized to exactly `image_sections × image_sections` cells.
4. **Integer construction**: the grid is flattened row by row into a bit sequence, with a leading `1` (control bit) prepended so leading zeros are preserved.

Each graph node stores its `position`, its `label` and its `neighbors` in that layer. A node that appears in several layers has an independent record in each.

### 5.2 Example

With `image_sections = 3` and `luminance_threshold = 128`:

```text
Image         Binarized     Cropped    Resized 3x3    Bits
0   0   0  0  0 0 0 0      1 1        1 1 1          111111110
0 200 220  0  0 1 1 0      1 0        1 1 1          + control bit -> 1111111110
0 210   0  0  0 1 0 0                 1 1 0          = 1022
0   0   0  0  0 0 0 0
```

### 5.3 Hamming Distance

The distance between two images is the **Hamming distance** between their `Position`s: the number of grid cells in which they differ. It is computed with two bitwise operations:

```python
def hamming_distance(num1: int, num2: int) -> int:
    return (num1 ^ num2).bit_count()
```

XOR sets a bit to `1` exactly where the two numbers differ, and `bit_count()` counts those bits. The control bit is identical in every `Position`, so it cancels out. The distance ranges from `0` (identical) to `image_sections²`.

This is the only metric HNSW uses: it decides which candidates become neighbors during construction, which nodes the search visits, and how much each candidate counts when classifying.

---

## 6. Building the Index

1. **Preparation**: the training set is shuffled with `shuffle_seed` and the layers are planned (see [section 4](#4-modifications-to-the-original-hnsw)), which fixes each node's top layer.
2. **Insertion**: nodes are inserted one at a time.
   - The search descends greedily through the layers above the node's top layer to find an entry point.
   - From the node's top layer down to layer 0, it finds `construction_max_candidates` nearby nodes and selects up to `max_neighbors` of them with the selection heuristic. A candidate is rejected if it is closer to an already selected neighbor than to the new node, which keeps neighbors diverse.
   - Links are created in both directions. Any neighbor left with too many connections is pruned, dropping its farthest links first.
   - In layer 0, both limits (neighbors and candidates) are **doubled**.
3. If a node reaches a layer higher than any existing one, it becomes the new entry point.

---

## 7. Classification

1. The image is converted into a `Position` using the same `image_sections` and `luminance_threshold` as in training.
2. The search starts at the top-layer entry point and descends layer by layer, keeping up to `classification_max_candidates` candidates per layer. The best node of each layer is the entry point of the next.
3. The candidates found in layer 0 are the result, each with its Hamming distance to the query.
4. Each candidate **votes** for its label with weight `1 / (1 + distance)`: a candidate at distance 0 counts `1`, one at distance 9 counts `0.1`.
5. Weights are summed per label and the label with the highest total is the predicted class.

A few very close candidates can therefore outvote many distant ones. Raising `classification_max_candidates` widens the search at the cost of time.

---

## 8. The Hnsw Class

`Hnsw` is the main interface of the project. It centralizes training, testing, classification, persistence and progress reporting, so scripts, graphical interfaces or other applications only need `Hnsw` and `HnswParameters`.

### 8.1 Parameters

Parameters are provided through an immutable `HnswParameters` dataclass.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `max_neighbors` | `int` | required | Maximum neighbors per node (doubled in layer 0) |
| `construction_max_candidates` | `int` | required | Candidate list size during construction (doubled in layer 0) |
| `classification_max_candidates` | `int` | required | Candidate list size during classification |
| `image_sections` | `int` | required | Number of horizontal and vertical divisions of each image |
| `luminance_threshold` | `int` | required | Binarization threshold (pixel > threshold becomes `1`) |
| `layer_growth_factor` | `float \| None` | `None` | Growth between layers; `None` uses `max_neighbors`. Must be greater than 1 |
| `shuffle_seed` | `int` | `0` | Seed for shuffling the training set |

### 8.2 Services

| Service | Description |
|---|---|
| `Hnsw(parameters, model_file=None, results_file=None)` | Creates an instance. The optional files define where the model and the test results are saved |
| `Hnsw.from_file(model_file)` | Creates an instance from a saved model, reading its parameters from the file |
| `train(ignore_cache=False)` | Builds the index from the EMNIST Balanced training set |
| `test()` | Runs the test set and returns a `HnswTestReport` (also saved as JSON if `results_file` was given) |
| `classify(image)` | Classifies a 2D `np.ndarray` and returns the predicted character as a `str` |
| `get_parameters()` | Returns the instance's `HnswParameters` |
| `get_train_progress()` / `is_train_done()` | Training progress (0–100) and completion |
| `get_test_progress()` / `is_test_done()` | Test progress (0–100) and completion |
| `is_classification_done()` | Whether the last classification has finished |

`train()` is skipped when a model with **identical parameters** is already in memory or in `model_file`; use `train(ignore_cache=True)` to force a rebuild. `test()` and `classify()` raise `RuntimeError` if no compatible model is available. `train()` and `test()` are synchronous, so to follow progress, run them in a separate thread and poll the progress getters.

### 8.3 Usage

```python
from pathlib import Path

import numpy as np

from src.hnsw import Hnsw, HnswParameters

parameters = HnswParameters(
    max_neighbors=16,
    construction_max_candidates=100,
    classification_max_candidates=32,
    image_sections=16,
    luminance_threshold=128,
)
hnsw = Hnsw(parameters, model_file=Path("model.json"), results_file=Path("results.json"))

hnsw.train()
report = hnsw.test()
print(f"Accuracy: {report.accuracy:.2%}")

image = np.zeros((28, 28), dtype=np.uint8)
image[6:22, 12:16] = 255
print(hnsw.classify(image))
```

The parameter values above are illustrative. A saved model can be reused later with `Hnsw.from_file(Path("model.json"))`.

---

## 9. Training, Testing and Metrics

**Training.** The EMNIST Balanced training set is loaded, the index is built (see [section 6](#6-building-the-index)) and the model is saved to `model_file`, if provided. Training time is not recorded.

**Testing.** Each test image is classified and compared with its expected label. The report contains:

| Field | Description |
|---|---|
| `total_tests`, `total_correct`, `total_incorrect` | Test image counts |
| `accuracy` | `total_correct / total_tests`, between `0` and `1` |
| `total_execution_time` | Total time of the test loop, in seconds |
| `execution_time_per_test` | Average time per image, in seconds |
| `confusion_matrix` | List of `{ "expected", "actual", "count" }` entries |

Times are measured with `time.perf_counter()` and cover only the classification loop, excluding dataset loading and training. The confusion matrix is stored sparsely: only (expected, predicted) pairs that occurred are listed, and absent pairs have count zero.

**Files.**

- **Results file** (`results_file`): the report fields above plus `parameters`, with `layer_growth_factor` already resolved to its effective value.
- **Model file** (`model_file`): `parameters` (used to decide whether the model can be reused) and `layers`, the complete index.

---

## 10. Project Structure

```text
.
├── main.py          # Entry point: opens the training and testing interface
└── src/
    ├── domain/      # Graph types, Position and Label
    ├── hnsw/        # The Hnsw class and its parameters, builder, tester, classifier and storage
    └── services/    # Search, layer planning, neighbor selection, connections and dataset extraction
```