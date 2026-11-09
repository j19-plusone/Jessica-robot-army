"""AOEE: safe, read-only GitHub discovery and upgrade proposals.

No automatic dependency installation, code execution, merges, or deployment.
Uses GitHub public REST API and standard library only.
"""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone

TOPICS = {
    "agents": "topic:ai-agents",
    "skills": "topic:agent-skills",
    "models": "topic:large-language-model",
    "voice": "topic:speech-recognition",
    "health": "topic:healthcare",
}
MAX_RESULTS = 10

def search_repositories(topic="agents", since="2026-10-01", limit=5, opener=None):
    if topic not in TOPICS:
        raise ValueError("Unknown research topic")
    datetime.strptime(since, "%Y-%m-%d")
    if not isinstance(limit, int) or not 1 <= limit <= MAX_RESULTS:
        raise ValueError("limit must be between 1 and 10")
    query = f'{TOPICS[topic]} pushed:>={since} archived:false'
    params = urllib.parse.urlencode({"q": query, "sort": "updated", "order": "desc", "per_page": limit})
    url = "https://api.github.com/search/repositories?" + params
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "Jessica-AOEE-Research/0.1"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    request = urllib.request.Request(url, headers=headers)
    response = (opener or urllib.request.urlopen)(request, timeout=15)
    with response:
        data = json.load(response)
    return [{
        "name": item["full_name"],
        "url": item["html_url"],
        "updated_at": item.get("pushed_at"),
        "stars": item.get("stargazers_count", 0),
        "license": (item.get("license") or {}).get("spdx_id", "UNKNOWN"),
        "description": (item.get("description") or "")[:250],
        "status": "research_only",
        "approval_required": True,
    } for item in data.get("items", [])]

def make_report(topic, results):
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "topic": topic,
        "candidates": results,
        "policy": "Discovery only; inspect source, provenance, license, dependencies, and security before sandbox evaluation.",
        "automatic_code_changes": False,
        "automatic_installation": False,
        "automatic_deployment": False,
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", choices=sorted(TOPICS), default="agents")
    parser.add_argument("--since", default="2026-10-01")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(make_report(args.topic, search_repositories(args.topic, args.since, args.limit)), ensure_ascii=False, indent=2))
