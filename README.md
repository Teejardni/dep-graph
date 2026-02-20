# dep-graph (`dg`)

A CLI tool that resolves Python package dependencies by recursively querying PyPI, builds a directed acyclic graph of the full dependency tree, detects cycles, computes a valid install order via topological sort, and visualizes the result.

Built with NetworkX, httpx, and click.

---

## How It Works

1. Reads `pyproject.toml` and extracts direct dependencies
2. Recursively fetches each package's metadata from the PyPI JSON API
3. Builds a directed graph where an edge `A → B` means "A must be installed before B"
4. Detects cycles (which would make resolution impossible)
5. Produces a valid install order via topological sort
6. Visualizes the graph via pydot (default) or matplotlib (`--fancy`)

---

## Installation

Requires Python 3.12+ and [graphviz](https://graphviz.org/download/) installed on your system.

```bash
git clone https://github.com/Teejardni/dep-graph
cd dep-graph
```
(Recommended)
```bash
uv sync
uv pip install -e .
```
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```
---

## Usage

### Resolve dependencies from a `pyproject.toml`

```bash
# Resolve current directory (looks for pyproject.toml)
dg resolve

# Resolve a specific project path
dg resolve /path/to/project

# Fancy matplotlib visualization instead of pydot
dg resolve /path/to/project --fancy

# Dump raw dependency tree as JSON
dg resolve /path/to/project --json
```

### Inspect a single package

```bash
# Full recursive dependency tree for a package
dg inspect numpy

# Dump as JSON instead of visualizing
dg inspect numpy --json
```

---

## Output

- **Default**: Saves `graph.png` to current directory and opens it automatically
- **`--fancy`**: Opens an interactive matplotlib window with color-coded nodes (red = root packages with no dependencies, blue = transitive dependencies)
- **`--json`**: Prints the full dependency metadata to stdout

---

## Future Features

- **Disk caching** — cache PyPI responses to `~/.depgraph/cache/` with TTL, making repeat runs near-instant
- **Version conflict detection** — identify cases where two packages require incompatible versions of the same dependency (e.g. `numpy<2.0` vs `numpy>=2.2`)
- **`requirements.txt` support** — resolve deps from a plain requirements file in addition to `pyproject.toml`
- **npm / cargo / conda / pixi support** — extend the resolver to other ecosystems
- **Nix derivation support** — model Nix's content-addressed dependency graph where multiple versions of the same package can coexist
- **`--depth` flag** — limit BFS depth for faster partial resolution on large trees
- **`dg compare`** — diff the dependency trees of two projects side by side
