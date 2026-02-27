# repaudit

A CLI tool that resolves Python package dependencies by recursively querying PyPI, builds a directed acyclic graph of the full dependency tree, detects cycles, computes a valid install order via topological sort, and visualizes the result.

## Future Features

- **Disk caching** — cache PyPI responses to `~/.repaudit/cache/` with TTL, making repeat runs near-instant
- **Version conflict detection** — identify cases where two packages require incompatible versions of the same dependency (e.g. `numpy<2.0` vs `numpy>=2.2`)
- **`requirements.txt` support** — resolve deps from a plain requirements file in addition to `pyproject.toml`
- **npm / cargo / conda / pixi support** — extend the resolver to other ecosystems
- **Nix derivation support** — model Nix's content-addressed dependency graph where multiple versions of the same package can coexist
- **`--depth` flag** — limit BFS depth for faster partial resolution on large trees
- **`dg compare`** — diff the dependency trees of two projects side by side
