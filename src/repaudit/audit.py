from pathlib import Path
from typing import List
from .report import Report

class Auditor:
    def __init__(self, resolvers=None):
        self.resolvers = resolvers or {}

    async def run(self, path: Path, client) -> List[Report]:
        findings = []
        
        return findings
