# python-graphviz-plus

A set of graph and network visualization utilities that extend `graphviz`, `networkx`, and `pandas`. Highly optimized for generating clean, elegant, and styled graphs in both Jupyter Notebooks and standard Python scripts.

## Key Features

- **`AdjacencyList`**: Parse edge lists (traditional `ll` representation) or dictionaries of neighbor tuples. Easily convert these structures into Pandas DataFrames for quick inspection and tabular formatting.
- **`BlackNeatoGraph`**: An elegant Graphviz-based class using the `neato` layout engine. Renders beautiful dark-themed networks with circular nodes, custom positioning (`pos`), overlap prevention, and automatic styling. Provides direct helpers to check graph properties (e.g., maximum/minimum degrees, regularity).
- **`ValencyList`**: A specialized helper class to calculate, analyze, and manage the degrees (valency) of all nodes in a graph. Features handshake lemma validation, regular graph detection, and sorted list exports.

## Installation

You can install `python-graphviz-plus` directly from PyPI:

```bash
pip install python-graphviz-plus
```

## Quick Start

### 1. Generating a Black Neato Graph
```python
from graph import BlackNeatoGraph

# Define an edge list (source, destination)
edges = [
    ("A", "B"),
    ("B", "C"),
    ("C", "A"),
    ("C", "D")
]

# Position mapping for nodes (optional)
positions = [
    ("A", "0,0!"),
    ("B", "1,1!"),
    ("C", "2,0!"),
    ("D", "3,-1!")
]

# Create and render the black graph
g = BlackNeatoGraph(ll=edges, lp=positions, name="MyBeautifulGraph")

# Inside a Jupyter Notebook, it will render inline:
# g
# Or save to a file:
g.render("graph_output", format="png", cleanup=True)
```

### 2. Inspecting Node Valencies
```python
from graph import ValencyList

# Analyze the valencies from the edge list
valencies = ValencyList(edges)

print("Degrees mapping:", valencies.raw())
print("Is regular graph?", valencies.is_regular())
print("Handshake lemma holds?", valencies.sum_check())
```

### 3. Converting to a Tabular Adjacency Matrix / DataFrame
```python
from graph import AdjacencyList

adj = AdjacencyList(edges)
df = adj.to_dataframe()

# Display as pandas DataFrame
print(df)
```

## Requirements
- Python >= 3.8
- `graphviz`
- `networkx`
- `pandas`

*Note: Ensure that the Graphviz system binaries (`dot`, `neato`, etc.) are installed on your system path.*
