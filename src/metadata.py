import httpx

async def get_package_metadata(client: httpx.AsyncClient, package: str, version: str | None = None):
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
    


