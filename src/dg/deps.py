from typing import List
from typing import Dict
import tomllib
from pathlib import Path
from packaging.requirements import Requirement, InvalidRequirement

def read_pyproject(filepath: Path):
    """ Read pyproject to receive deps"""
    filepath = Path(filepath)
    pptml = filepath / "pyproject.toml"
    try:
        with pptml.open("rb") as f:
            data = tomllib.load(f).get('project')
            
        return data
    except Exception as e:

        return e

def _resolve_dependency_versions(deps: List[str]):
    """ Returns a dict of resolved dependencies from a PEP 508 list """
    resolved = {}
    for dep in deps:
        try:
            req = Requirement(dep)
            if req.marker and "extra" in str(req.marker):
                continue
            resolved[req.name.lower()] = str(req.specifier)
        except InvalidRequirement as e:
            print(f"Warning: Could not process requirement '{dep}' : {e}")
            continue

    return resolved

def parse_data(data: Dict):
    rp = data.get('requires-python')
    packages = _resolve_dependency_versions(data.get('dependencies'))

    return rp, packages

