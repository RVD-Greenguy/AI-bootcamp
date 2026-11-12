"""
Geocode Singapore schools missing lat/lng via OneMap text search.
Results cached to storage/geocode_cache.json to avoid re-geocoding on every cold start.
"""
import json
import requests
from pathlib import Path

CACHE_PATH = Path(__file__).parent.parent / "storage" / "geocode_cache.json"
ONEMAP_SEARCH = "https://www.onemap.gov.sg/api/common/elastic/search"
SCHOOLS_JSON = Path(__file__).parent.parent / "data" / "seed" / "secondary_schools.json"
PRIMARY_SCHOOLS_JSON = Path(__file__).parent.parent / "data" / "seed" / "primary_schools.json"


def _load_cache() -> dict:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text())
        except Exception:
            return {}
    return {}


def _save_cache(cache: dict):
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, indent=2))


def _search_onemap(query: str) -> dict | None:
    """Search OneMap for a name or postal. Returns first result with geometry."""
    try:
        resp = requests.get(
            ONEMAP_SEARCH,
            params={"searchVal": query, "returnGeom": "Y", "getAddrDetails": "Y", "pageNum": 1},
            timeout=8,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        for r in results:
            if r.get("LATITUDE") and r.get("LONGITUDE"):
                return {
                    "lat": float(r["LATITUDE"]),
                    "lng": float(r["LONGITUDE"]),
                    "address": r.get("ADDRESS", ""),
                    "postal": r.get("POSTAL", ""),
                }
    except Exception:
        pass
    return None


def geocode_missing_schools() -> int:
    """
    Geocode any schools in secondary_schools.json that are missing lat/lng.
    Applies cached results first, then calls OneMap for uncached schools.
    Returns the number of schools newly geocoded this run.
    """
    schools = json.loads(SCHOOLS_JSON.read_text())
    cache = _load_cache()
    filled = 0
    cache_dirty = False

    for school in schools:
        if school.get("lat") and school.get("lng"):
            continue  # already has coordinates

        sid = school["id"]

        if sid in cache:
            # Apply from cache without hitting API
            school["lat"] = cache[sid]["lat"]
            school["lng"] = cache[sid]["lng"]
            if not school.get("address"):
                school["address"] = cache[sid].get("address", "")
            if not school.get("postal"):
                school["postal"] = cache[sid].get("postal", "")
            filled += 1
            continue

        # Try geocoding: postal first (more precise), then full name, then short name
        result = None
        if school.get("postal"):
            result = _search_onemap(school["postal"])
        if not result:
            result = _search_onemap(school["name"])
        if not result and school.get("short_name"):
            result = _search_onemap(school["short_name"])

        if result:
            school["lat"] = result["lat"]
            school["lng"] = result["lng"]
            if not school.get("address"):
                school["address"] = result["address"]
            if not school.get("postal"):
                school["postal"] = result.get("postal", "")
            cache[sid] = result
            cache_dirty = True
            filled += 1

    if filled:
        SCHOOLS_JSON.write_text(json.dumps(schools, indent=2))
    if cache_dirty:
        _save_cache(cache)

    return filled


def geocode_missing_primary_schools() -> int:
    """
    Geocode any schools in primary_schools.json that are missing lat/lng.
    Applies cached results first, then calls OneMap for uncached schools.
    Returns the number of schools newly geocoded this run.
    """
    if not PRIMARY_SCHOOLS_JSON.exists():
        return 0

    schools = json.loads(PRIMARY_SCHOOLS_JSON.read_text())
    cache = _load_cache()
    filled = 0
    cache_dirty = False

    for school in schools:
        if school.get("lat") and school.get("lng"):
            continue

        sid = "pri_" + school["id"]

        if sid in cache:
            school["lat"] = cache[sid]["lat"]
            school["lng"] = cache[sid]["lng"]
            if not school.get("address"):
                school["address"] = cache[sid].get("address", "")
            if not school.get("postal"):
                school["postal"] = cache[sid].get("postal", "")
            filled += 1
            continue

        result = None
        if school.get("postal"):
            result = _search_onemap(school["postal"])
        if not result:
            result = _search_onemap(school["name"])
        if not result and school.get("short_name"):
            result = _search_onemap(school["short_name"])

        if result:
            school["lat"] = result["lat"]
            school["lng"] = result["lng"]
            if not school.get("address"):
                school["address"] = result["address"]
            if not school.get("postal"):
                school["postal"] = result.get("postal", "")
            cache[sid] = result
            cache_dirty = True
            filled += 1

    if filled:
        PRIMARY_SCHOOLS_JSON.write_text(json.dumps(schools, indent=2))
    if cache_dirty:
        _save_cache(cache)

    return filled


def geocode_all() -> int:
    """Geocode all school types. Returns total number newly geocoded."""
    total = 0
    total += geocode_missing_schools()
    total += geocode_missing_primary_schools()
    return total
