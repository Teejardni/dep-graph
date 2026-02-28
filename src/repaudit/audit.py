from .resolvers.pypi_resolver import PYPIResolver
from pathlib import Path
from typing import List
from .report import Report

RESOLVERS = {
        "pypi": PYPIResolver()
        }

class Auditor:
    def __init__(self):
        self.resolvers = RESOLVERS

    async def run(self, path: Path, client, env: str | None = None) -> List[Report]:
        findings = []
        resolver = self.resolvers["pypi"]
        requires_python, packages = resolver.parse_manifest(path, env)
        if not packages:
            return findings
        deps = await resolver.resolve(client, packages)
        
        return findings
