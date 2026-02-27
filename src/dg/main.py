from genericpath import exists
from .viz import visualize_pydot
from .viz import visualize_matplotlib
import click
import asyncio
import httpx
from pathlib import Path
from .deps import read_pyproject, parse_data
from .dagger import build_dependency_tree
from .dagger import build_dependency_graph

@click.group()
def cli():
    pass


#@cli.command()
#@cli.argument("audit", default=".", type=click.Path(exists=True))


@cli.command()
@click.argument("path", default=".", type=click.Path(exists=True))
@click.option("--fancy", "-f", is_flag=True, help="Matplotlib visualisation instead of pydot")
@click.option("--json", "as_json", is_flag=True, help="Dump raw output as JSON, no visualisation")
def resolve(path, fancy, as_json):
    """Resolve dependencies from a pyproject.toml"""
    async def _run():
        async with httpx.AsyncClient() as client:
            rproj = read_pyproject(Path(path))
            rp, packages = parse_data(rproj)
            deps = await build_dependency_tree(client, packages)
            graph, order = build_dependency_graph(deps)
            return deps, graph, order

    deps, graph, order = asyncio.run(_run())
    if order is None:
        click.echo(click.style("Cycle detected, cannot visualize", fg="red"))
        return
    if as_json:
        import json
        click.echo(json.dumps(deps, indent=2, default=str))
        return

    if fancy:
        visualize_matplotlib(graph) 
    
    else:
        visualize_pydot(graph)

@cli.command()
@click.argument("package")
@click.option("--json", "as_json", is_flag=True, help="Dump raw output as JSON, no visualisation")
def inspect(package, as_json):
    """Inspect a single package and its full dependency tree"""
    async def _run():
        async with httpx.AsyncClient() as client:
            deps = await build_dependency_tree(client, {package: ""})
            graph, order = build_dependency_graph(deps)
            return deps, graph, order

    deps, graph, order = asyncio.run(_run())

    if as_json:
        import json
        click.echo(json.dumps(deps, indent=2, default=str))
        return
    else:
        
        visualize_pydot(graph)


if __name__ == "__main__":
    cli()
