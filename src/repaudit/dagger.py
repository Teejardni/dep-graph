from typing import Dict
from .deps import _resolve_dependency_versions
from .metadata import get_package_metadata
import httpx
import networkx as nx
import asyncio

async def build_dependency_tree(client: httpx.AsyncClient, packages):

    visited = {}
    queue = list(packages.keys())
    while queue:
        results = await asyncio.gather(
            *[get_package_metadata(client, package) for package in queue],
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

def build_dependency_graph(deps: Dict) -> nx.DiGraph:
    graph = nx.DiGraph()

    for package, metadata in deps.items():
        graph.add_node(package)
        sub_deps = _resolve_dependency_versions(metadata["requires_dist"])
        for dep in sub_deps:
            if dep in deps: 
                graph.add_edge(dep, package)  # dep must exist before package
    try:
        cycle = nx.find_cycle(graph)
        print(f"Cycle detected, cannot resolve install order: {list(cycle)}")
        return graph, None
    except nx.NetworkXNoCycle:
        order = nx.topological_sort(graph)
    return graph, order


