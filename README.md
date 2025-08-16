# Trackbase Cost Optimization Task

## 1. About the Project

This project contains an **API and utilities to compute total traversal costs** across graph-like paths.

It includes:

- A **baseline algorithm (`logic_as_is`)** for correctness and benchmarking.
- An **optimized algorithm (`improved_logic`)** that uses indexing for far better performance.
- A **FastAPI service** that exposes the functionality for testing with real payloads.
- **Unit tests and benchmarks** for correctness and performance validation.

---

## 2. Setup & Running the Project

### a. Create a Virtual Environment with `uv`

If you’re using [uv](https://github.com/astral-sh/uv):

```bash
uv venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

### b. Install dependencies

```bash
pip install -r requirements.txt
```

### c. Commands

**Run the benchmark harness (compare baseline vs optimized):**

```bash
python main.py
```

**Run the FastAPI app (development mode):**

```bash
uvicorn app:app --reload --port 8000
```

App will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)
Docs auto-generated at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

**Run all tests (unit + API):**

```bash
pytest -q
```

---

## 3. Algorithmic Logic

### Baseline: `logic_as_is`

```python
def logic_as_is(traversals: List[Traversal], pathCosts: List[CostAtNode]) -> List[Traversal]:
    ...
```

- Resets all node cost values to ensure calculations start fresh.
- Iterates through each entry in pathCosts, scanning all nodes across every traversal.
- Accumulates the corresponding costs and assigns the final sum to traversal.total_cost.

**Time Complexity:**
O(T × P × N)
Where:

- **T** = number of traversals
- **N** = number of nodes per traversal
- **P** = number of pathCosts

This triple-nested scan becomes slow for large inputs.

---

### Optimized: `improved_logic`

```python
def improved_logic(traversals: List[Traversal], pathCosts: List[CostAtNode]) -> List[Traversal]:
    ...
```

- Pre-computes and stores all costs in a dictionary keyed by node_id for fast lookups.
- Iterates through each traversal, visiting each node once and attaching its cost directly from the index.
- Leverages pre-computed per-node sums to avoid redundant additions when accumulating totals.

**Time Complexity:**
O(P + T × N)

- Indexing costs: O(P)
- Traversing nodes once per traversal: O(T × N)

This removes the inner nested scan, making performance scale linearly.

---

## 4. API Documentation

### Base URL

```
http://127.0.0.1:8000
```

### Endpoints

#### **Health Check**

`GET /health`
Returns simple status.

```json
{ "status": "ok" }
```

---

#### **Compute Traversal Costs**

`POST /compute`

**Description:**
Given a set of traversals (nodes) and a list of path costs, compute the `total_cost` for each traversal.

**Request Body:**

```json
{
  "traversals": [
    { "nodes": [{ "id": 0 }, { "id": 1 }, { "id": 2 }] },
    { "nodes": [{ "id": 0 }, { "id": 1 }] }
  ],
  "pathCosts": [
    { "node_id": 1, "cost": 5 },
    { "node_id": 2, "cost": 7 },
    { "node_id": 1, "cost": 3 }
  ]
}
```

**Response:**

```json
[
  {
    "nodes": [
      { "id": 0, "costs": null },
      {
        "id": 1,
        "costs": [
          { "node_id": 1, "cost": 5 },
          { "node_id": 1, "cost": 3 }
        ]
      },
      { "id": 2, "costs": [{ "node_id": 2, "cost": 7 }] }
    ],
    "total_cost": 15
  },
  {
    "nodes": [
      { "id": 0, "costs": null },
      {
        "id": 1,
        "costs": [
          { "node_id": 1, "cost": 5 },
          { "node_id": 1, "cost": 3 }
        ]
      }
    ],
    "total_cost": 8
  }
]
```

**Validation Errors:**
If a cost references a node ID not present in any traversal:

```json
{
  "detail": "Found 1 cost(s) referencing unknown node_id(s). First few: [99]"
}
```

---

## 5. Tests

- **Unit Tests:** Ensure both algorithms return identical results for random inputs and edge cases.
- **API Tests:** Check endpoints, happy path, and error handling.
- **Performance Harness (`main.py`):** Benchmarks algorithms across parameter sets and prints timings.

---

## 6. Project Structure

```
.
├── app.py           # FastAPI application
├── funcs.py         # Core algorithms (baseline + optimized)
├── helpers.py       # Profiling utilities
├── main.py          # Benchmark harness
├── models.py        # Pydantic models (domain + API schema)
├── requirements.txt # Dependencies
└── tests/           # Unit and API tests
```

---

## 7. Key Learnings & Enhancements

- **Indexing (hashmap) turns O(T×P×N) into O(P + T×N).**
- Unified **Pydantic models** avoid redundancy with dataclasses.
- Clear separation:

  - `funcs.py`: algorithms
  - `app.py`: API layer
  - `main.py`: benchmarking
  - `tests/`: correctness

- Built-in docs (`/docs`) make it easy for others to try the API.

---
