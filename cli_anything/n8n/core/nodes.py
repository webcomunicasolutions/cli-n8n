"""Node discovery — search n8n community nodes via npm registry.

Uses the npm registry API to search for n8n community node packages.
No authentication needed.
"""

from __future__ import annotations

from typing import Any

import requests


NPM_SEARCH_URL = "https://registry.npmjs.com/-/v1/search"


def search_nodes(query: str, *, limit: int = 15) -> dict[str, Any]:
    """Search for n8n community node packages on npm."""
    resp = requests.get(
        NPM_SEARCH_URL,
        params={"text": f"n8n-nodes {query}", "size": limit},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    packages = []
    for obj in data.get("objects", []):
        pkg = obj.get("package", {})
        name = pkg.get("name", "")
        # Filter out non-node packages
        if not name.startswith("n8n-nodes") and "n8n-nodes" not in name:
            continue
        packages.append({
            "name": name,
            "version": pkg.get("version", ""),
            "description": pkg.get("description", "")[:120],
            "author": pkg.get("publisher", {}).get("username", pkg.get("author", {}).get("name", "")),
            "npm_url": f"https://www.npmjs.com/package/{name}",
            "weekly_downloads": obj.get("score", {}).get("detail", {}).get("popularity", 0),
        })

    return {"total": data.get("total", 0), "packages": packages}


def get_node_info(package_name: str) -> dict[str, Any]:
    """Get detailed info about an npm node package."""
    resp = requests.get(
        f"https://registry.npmjs.com/{package_name}",
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    latest = data.get("dist-tags", {}).get("latest", "")
    latest_data = data.get("versions", {}).get(latest, {})

    # Extract n8n-specific metadata
    n8n_meta = latest_data.get("n8n", {})
    node_list = n8n_meta.get("nodes", [])
    credential_list = n8n_meta.get("credentials", [])

    return {
        "name": data.get("name", ""),
        "version": latest,
        "description": data.get("description", ""),
        "author": data.get("author", {}).get("name", "") if isinstance(data.get("author"), dict) else str(data.get("author", "")),
        "license": latest_data.get("license", ""),
        "homepage": data.get("homepage", ""),
        "repository": data.get("repository", {}).get("url", "") if isinstance(data.get("repository"), dict) else "",
        "npm_url": f"https://www.npmjs.com/package/{data.get('name', '')}",
        "n8n_nodes": [n.get("type", n) if isinstance(n, dict) else n for n in node_list],
        "n8n_credentials": [c.get("type", c) if isinstance(c, dict) else c for c in credential_list],
        "install_cmd": f"cd ~/.n8n && npm install {data.get('name', '')}",
        "keywords": latest_data.get("keywords", [])[:10],
    }
