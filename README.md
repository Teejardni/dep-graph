# repaudit

A CLI tool to audit a cross-ecosystem codebase in one shot.

```bash
repaudit .
```
---

## Objectives

- Vulnerabilities
- Unpinned dependencies
- Dependency drift 
- Version mismatches
- Cycles
- Deprecations

A unified report across every ecosystem it finds in your repo.

---

## Supported ecosystems

| Ecosystem | Manifest | Status |
|-----------|----------|--------|
| Python | `pyproject.toml`, `requirements.txt` | First Priority |
| Node / NPM | `package.json`, `package-lock.json` | Soon |
| Go | `go.mod`, `go.sum` | Soon |
| Docker | `Dockerfile` | Soon (unpinned base images + known vulns) |
| GitHub Actions | `.github/workflows/*.yml` | Soon|
| Conda / Pixi | `environment.yml`, `pixi.toml` | Unknown |

---

## Commands

```bash
# Audit the current directory 
repaudit .

# Audit a specific path
repaudit /path/to/repo

# Output as JSON
repaudit . --json

# Resolve and visualise the dependency graph
repaudit resolve .
repaudit resolve . --fancy     # matplotlib visualisation

# Inspect a single package's full dependency tree
repaudit inspect <package>
repaudit inspect <package> --json
```

---

## resurrect

`resurrect` is a planned sub-feature of repaudit aimed at older Python repositories that have unpinned or underspecified `requirements.txt` files — tools that are still useful but are a pain to actually run.

```bash
repaudit resurrect .
```

It will attempt to resolve a working, pinned set of dependencies for the repo as it exists today, and output a locked `requirements.txt` you can actually use. The goal is to make old repos runnable again without manual archaeology.

---

## Environment upgrade compatibility

Another planned sub-feature is to have repaudit check whether your codebase and its dependencies are compatible with a target Python version before you upgrade.

```bash
repaudit compat . --target 3.12
```

---

---

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | No errors found |
| `1` | One or more error-severity findings |

---


