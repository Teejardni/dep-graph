import httpx

async def get_package_metadata(client: httpx.AsyncClient, package: str, version: str | None = None):
    url = f"https://pypi.org/pypi/{package}/json" if not version else f"https://pypi.org/pypi/{package}/{version}/json"
    response = await client.get(url)
    response.raise_for_status()
    print(f'Resp is: {response.json()}')
    return response.json()




