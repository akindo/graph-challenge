# Graph Challenge
## Algorithm
The ownership structure is a sparse graph. Such graphs, due to their low edge count, are best represented using specific data structures that optimize storage and traversal. A sparse graph are ideally represented by an adjacency list. In an adjacency list, each vertex maintains a list of adjacent vertices it is directly connected to.

The optimum algorithm for analyse the ownership structure is a recursive [Depth-First Search](https://en.wikipedia.org/wiki/Depth-first_search) (DFS).

### Time complexity
 $O(V+E)$

where
* $V$ = Number of vertices
* $E$ = Number of edges

### Space Complexity
* DFS: $O(V)$ (for the recursion stack in worst case, when the graph is a linear chain)
* Adjacency list storage: $O(V+E)$

## Run
### With 
Install [UV](https://docs.astral.sh/uv):
```
brew install uv
```

Update and activate venv:
```
uv sync
```

Run:
```
uv run src/main.py
```

### With Python
Create venv:
```
python -m venv .venv
```

Activate venv:
```
. .venv/bin/activate
```

Install dependencies:
```
pip install .
```

Run:
```
python src/main.py
```

Deactivate venv:
```
deactivate
```

## Development
### Format
Verify files correctly formatted:
```
ruff format --check
```

Format:
```
ruff format
```

### Lint
Verify files correctly linted:
```
ruff check
```

Lint:
```
ruff check --fix
```
