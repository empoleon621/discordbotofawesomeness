# anime_cache.py
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional

import httpx

# AniList GraphQL endpoint
ANILIST_URL = "https://graphql.anilist.co"

# how many top titles to maintain and paging
TOP_N = 500
PER_PAGE = 50  # 10 pages of 50 == 500
FRESHNESS = timedelta(minutes=10)  # how long before refresh

# GraphQL to get popular anime sorted by popularity descending
TOP_ANIME_QUERY = """
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    media(type: ANIME, sort: POPULARITY_DESC) {
      id
      title {
        romaji
        english
        native
      }
    }
  }
}
"""

# GraphQL to fetch detailed info about a single anime by name
DETAIL_QUERY = """
query ($search: String) {
  Media(search: $search, type: ANIME) {
    id
    title {
      romaji
      english
    }
    description(asHtml: false)
    averageScore
    episodes
    status
    coverImage {
      large
      medium
    }
    siteUrl
  }
}
"""

class AniListCache:
    def __init__(self):
        self.titles: List[str] = []
        self.last_updated: Optional[datetime] = None
        self._lock = asyncio.Lock()
        self._client = httpx.AsyncClient(timeout=10)

    async def _fetch_page(self, page: int) -> List[str]:
        variables = {"page": page, "perPage": PER_PAGE}
        try:
            resp = await self._client.post(
                ANILIST_URL,
                json={"query": TOP_ANIME_QUERY, "variables": variables},
                headers={"Accept": "application/json"},
            )
            resp.raise_for_status()
            payload = resp.json()
            media = payload.get("data", {}).get("Page", {}).get("media", [])
            titles: List[str] = []
            for m in media:
                # prefer English, then romaji
                t = m["title"].get("english") or m["title"].get("romaji") or ""
                if t:
                    titles.append(t)
            return titles
        except Exception:
            return []

    async def refresh_if_stale(self):
        async with self._lock:
            now = datetime.utcnow()
            if self.last_updated and (now - self.last_updated) < FRESHNESS and self.titles:
                return  # still fresh
            all_titles: List[str] = []
            # fetch pages 1..(TOP_N/PER_PAGE)
            pages = (TOP_N + PER_PAGE - 1) // PER_PAGE
            for page in range(1, pages + 1):
                page_titles = await self._fetch_page(page)
                if not page_titles:
                    break  # bail on failure, keep whatever we have
                all_titles.extend(page_titles)
                # throttle a bit to be polite / avoid transient throttling
                await asyncio.sleep(0.2)
                if len(all_titles) >= TOP_N:
                    break
            if all_titles:
                self.titles = all_titles[:TOP_N]
                self.last_updated = datetime.utcnow()

    async def get_suggestions(self, current: str) -> List[str]:
        await self.refresh_if_stale()
        if not self.titles:
            return []
        lowered = current.lower()
        # simple substring match (could be improved with fuzzy logic)
        matches = [t for t in self.titles if lowered in t.lower()]
        return matches[:25]

    async def fetch_details(self, name: str) -> Optional[dict]:
        try:
            resp = await self._client.post(
                ANILIST_URL,
                json={"query": DETAIL_QUERY, "variables": {"search": name}},
                headers={"Accept": "application/json"},
            )
            resp.raise_for_status()
            payload = resp.json()
            return payload.get("data", {}).get("Media")
        except Exception:
            return None

    async def close(self):
        await self._client.aclose()
