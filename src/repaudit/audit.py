from pathlib import Path
from typing import List
import httpx

from .report import Report
from .resolvers.pypi_resolver import parse_manifest, resolve


def check_unpinned(pkgs:dict[str, str]):
    
async def run_audit(path: Path, client: httpx.AsyncClient) -> List[Report]:
    findings: List[Report] = []
    requires_python, packages = parse_manifest(path)
    if not packages:
        return findings
    await resolve(client, packages)
    # TODO: checks go here (CVE, unpinned, version mismatch, cycles, deprecations)
    return findings
