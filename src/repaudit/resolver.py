from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict
from .report import Report

class Resolver(ABC):

    @abstractmethod
    def parse_manifest(self, path: Path) -> Dict[str, str]:
        """Read a manifest file, return {package_name: specifier}"""
        ...

    @abstractmethod
    async def get_metadata(self, client, package: str, version: str | None = None) -> Dict:
        """Fetch package metadata from the ecosystem registry"""
        ...

    @abstractmethod
    async def resolve(self, client, packages: Dict[str, str]) -> Dict:
        """Resolve full dependency tree, return visited package metadata"""
        ...

    @property
    @abstractmethod
    def ecosystem(self) -> str:
        """e.g. 'pypi', 'npm', 'cargo'"""
        ...
