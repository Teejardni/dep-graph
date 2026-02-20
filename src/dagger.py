from deps import resolve_dependency_versions
from metadata import get_package_metadata
import httpx
import networkx as nx


async def build_dependancy_tree(client: httpx.AsyncClient, packages: dict([str, str])):

    visited = {}
    queue = list(packages.keys())

    while queue:
        package = queue.pop(0)

        if package in visited:
            continue

        try:
            md = get_package_metadata(client, package)
        
        except ValueError as e:
            print(f"Warning: {e}, skipping")
            continue

        visited[package] = md

        sub_deps = resolve_dependency_versions(md["requires_dist"])
        for sd in sub_deps:
            if sd not in visited:
                queue.append(sd)


    return visited


