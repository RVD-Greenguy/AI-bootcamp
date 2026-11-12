"""
OneMap SG location service.
- Geocode Singapore postal codes via OneMap public search API (no auth)
- Get travel times (drive + public transport) via OneMap routing API (requires token)
- Haversine distance + P1 registration zone classification
"""
from __future__ import annotations
import math
import streamlit as st
import requests

ONEMAP_BASE = "https://www.onemap.gov.sg/api"


# ── Auth ─────────────────────────────────────────────────────────────────────

def _get_token() -> str:
    """Return OneMap bearer token from secrets/env."""
    try:
        return st.secrets.get("ONEMAP_TOKEN", "") or st.secrets.get("ONEMAP_API_KEY", "")
    except Exception:
        pass
    import os
    return os.getenv("ONEMAP_TOKEN", "") or os.getenv("ONEMAP_API_KEY", "")


# ── Geocoding (no auth needed) ────────────────────────────────────────────────

@st.cache_data(ttl=86400, show_spinner=False)
def geocode_postal(postal_code: str) -> dict | None:
    """
    Geocode a 6-digit Singapore postal code using OneMap search API.
    Returns {"lat": float, "lng": float, "address": str} or None.
    """
    postal_code = postal_code.strip().zfill(6)
    try:
        resp = requests.get(
            f"{ONEMAP_BASE}/common/elastic/search",
            params={
                "searchVal": postal_code,
                "returnGeom": "Y",
                "getAddrDetails": "Y",
                "pageNum": 1,
            },
            timeout=8,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if not results:
            return None
        hit = results[0]
        return {
            "lat": float(hit["LATITUDE"]),
            "lng": float(hit["LONGITUDE"]),
            "address": hit.get("ADDRESS", ""),
            "block": hit.get("BLK_NO", ""),
            "road": hit.get("ROAD_NAME", ""),
            "building": hit.get("BUILDING", ""),
        }
    except Exception:
        return None


# ── Routing (requires token) ──────────────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def get_drive_time(start_lat: float, start_lng: float,
                   end_lat: float, end_lng: float) -> int | None:
    """
    Get estimated driving time in minutes via OneMap routing API.
    Returns None if token unavailable or request fails.
    """
    token = _get_token()
    if not token:
        return None
    try:
        resp = requests.get(
            f"{ONEMAP_BASE}/public/routingsvc/route",
            params={
                "start": f"{start_lat},{start_lng}",
                "end": f"{end_lat},{end_lng}",
                "routeType": "drive",
                "token": token,
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        total_seconds = data.get("route_summary", {}).get("total_time")
        if total_seconds is not None:
            return max(1, round(total_seconds / 60))
        return None
    except Exception:
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def get_pt_time(start_lat: float, start_lng: float,
                end_lat: float, end_lng: float) -> int | None:
    """
    Get estimated public transport time in minutes via OneMap routing API.
    Returns None if token unavailable or request fails.
    """
    token = _get_token()
    if not token:
        return None
    try:
        import time as _time
        # PT routing needs a date and time — use current epoch
        date_str = __import__("datetime").date.today().strftime("%m-%d-%Y")
        epoch = int(_time.time())
        resp = requests.get(
            f"{ONEMAP_BASE}/public/routingsvc/route",
            params={
                "start": f"{start_lat},{start_lng}",
                "end": f"{end_lat},{end_lng}",
                "routeType": "pt",
                "token": token,
                "date": date_str,
                "time": "07:30:00",
                "mode": "TRANSIT",
                "maxWalkDistance": "1000",
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        itineraries = data.get("plan", {}).get("itineraries", [])
        if itineraries:
            return max(1, round(itineraries[0]["duration"] / 60))
        return None
    except Exception:
        return None


# ── Distance utilities ────────────────────────────────────────────────────────

def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Straight-line distance between two lat/lng points in km."""
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def estimate_drive_min(dist_km: float) -> int:
    """Rough driving time estimate for Singapore (off-peak)."""
    return max(5, round(5 + dist_km * 2.2))


def estimate_pt_min(dist_km: float) -> int:
    """Rough public transport time estimate for Singapore."""
    return max(12, round(12 + dist_km * 4.5))


def travel_convenience(dist_km: float) -> dict:
    """Classify travel convenience and P1 priority zone."""
    if dist_km <= 1.0:
        return {"label": "Within 1 km", "emoji": "🟢", "p1_zone": "Phase 2B/2C priority", "colour": "#16a34a"}
    elif dist_km <= 2.0:
        return {"label": "1–2 km", "emoji": "🟡", "p1_zone": "Phase 2C consideration", "colour": "#ca8a04"}
    elif dist_km <= 5.0:
        return {"label": "2–5 km", "emoji": "🟠", "p1_zone": "No distance priority", "colour": "#ea580c"}
    else:
        return {"label": f"{dist_km:.1f} km", "emoji": "🔴", "p1_zone": "Far — no priority", "colour": "#dc2626"}
