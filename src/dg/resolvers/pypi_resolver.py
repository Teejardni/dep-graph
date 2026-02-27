import httpx
import asyncio
import tomllib
from typing import List, Dict
from pathlib import Path
from packaging.requirements import Requirement, InvalidRequirement





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

class PYPIResolver:
    #def init()
    async def get_package_metadata(self, client: httpx.AsyncClient, package: str, version: str | None = None):
        """Fetches the package metadata from PyPi"""
        url = f"https://pypi.org/pypi/{package}/json" if not version else f"https://pypi.org/pypi/{package}/{version}/json"
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Package '{package}' not found on PyPI") from e
            raise
        except httpx.RequestError as e:
            raise ConnectionError(f"Network error fetching '{package}': {e}") from e

        info = response.json()["info"]
        return {
                "name": info["name"],
                "version": info["version"],
                "requires_python": info["requires_python"],
                "requires_dist": info["requires_dist"] or []
                }
    

    async def resolve(self, client: httpx.AsyncClient, packages):

        visited = {}
        queue = list(packages.keys())
        while queue:
            results = await asyncio.gather(
                *[self.get_package_metadata(client, package) for package in queue],
                return_exceptions=True
            )
            next_queue = []
            for package, result in zip(queue, results):
                if isinstance(result, Exception):
                    print(f"Warning: failed to fetch '{package}', skipping: {result}")
                    continue
                visited[package] = result
                sub_deps = _resolve_dependency_versions(result["requires_dist"])
                for sd in sub_deps:
                    if sd not in visited and sd not in next_queue:
                        next_queue.append(sd)
        
            queue = next_queue

    
        return visited


    def parse_manifest(self, filepath: Path):
        """ Read pyproject to receive deps"""
        filepath = Path(filepath)
        pptml = filepath / "pyproject.toml"
        try:
            with pptml.open("rb") as f:
                data = tomllib.load(f).get('project')
            rp = data.get('requires-python')
            
            packages = _resolve_dependency_versions(data.get('dependencies'))

            return rp, packages
                        
            
        except Exception as e:

            return e

