import tomllib
from pathlib import Path
import httpx


def read_pyproject(filepath: Path):
    """ Read pyproject to receive deps"""
    try:
        with open(f"{filepath}/pyproject.toml", "rb") as f:
            data = tomllib.load(f).get('project')
            
        return data
    except Exception as e:
        return e

