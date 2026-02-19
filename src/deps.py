from typing import List
from typing import Dict
import tomllib
from pathlib import Path
from packaging.requirements import Requirement, InvalidRequirement

def read_pyproject(filepath: Path):
    """ Read pyproject to receive deps"""
    try:
        with open(f"{filepath}/pyproject.toml", "rb") as f:
            data = tomllib.load(f).get('project')
            
        return data
    except Exception as e:

        return e

def resolve_dependency_versions(deps: List[str]):
    resolved = {}
    for dep in deps:
        try:
            req = Requirement(dep)
            resolved[req.name.lower()] = str(req.specifier)
        except InvalidRequirement as e:
            print(f"Warning: Could not process requirement '{dep}' : {e}")
            continue

    return resolved

def parse_data(data: Dict):
    rp = data.get('requires-python')
    deps = resolve_dependency_versions(data.get('dependencies'))
    
    return rp, deps



