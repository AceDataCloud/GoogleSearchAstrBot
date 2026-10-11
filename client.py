"""Google web search through the Ace Data Cloud SERP API."""

from __future__ import annotations

import asyncio
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener


class SearchError(RuntimeError):
    """A public error that omits credentials and raw server data."""


class _NoRedirect(HTTPRedirectHandler):
    """Keep the API key on the fixed Ace Data Cloud host."""

    def redirect_request(self, request, fp, code, msg, headers, newurl):
        """Reject a redirect without copying the Authorization header.

        Args:
            request: Original request.
            fp: Response stream.
            code: Redirect status code.
            msg: HTTP status text.
            headers: Redirect headers.
            newurl: Redirect target.

        Returns:
            None so urllib raises an HTTP error.
        """
        return


OPENER = build_opener(_NoRedirect)


class GoogleSearchClient:
    """Run one synchronous Google web search."""

    def __init__(self, api_key: str) -> None:
        """Hold the configured generation key only in memory.

        Args:
            api_key: Ace Data Cloud API key with `/serp/google` access.

        Raises:
            SearchError: If the key is missing or is a management token.
        """
        token = api_key.strip()
        if (
            not token
            or token.lower().startswith("bearer ")
            or token.startswith("platform-")
        ):
            raise SearchError(
                "Set an Ace Data Cloud API key with Google Search access."
            )
        self._api_key = token

    def _search(self, query: str, number: int) -> dict[str, Any]:
        """Send one request and keep only public search result fields.

        Args:
            query: Nonempty search text.
            number: Number of web results, from 1 to 20.

        Returns:
            Search status, trace ID, and structured organic results.

        Raises:
            SearchError: For failed requests or invalid server data.
        """
        request = Request(
            "https://api.acedata.cloud/serp/google",
            data=json.dumps(
                {"query": query, "number": number, "page": 1, "type": "search"}
            ).encode(),
            headers={
                "Authorization": "Bearer " + self._api_key,
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "AceDataCloudAstrBot/0.1.0",
            },
            method="POST",
        )
        try:
            with OPENER.open(request, timeout=60) as response:
                body = json.load(response)
                trace_id = response.headers.get(
                    "x-trace-id", ""
                ) or response.headers.get("x-request-id", "")
        except HTTPError as exc:
            raise SearchError(
                f"Ace Data Cloud returned HTTP {exc.code}. Check key access."
            ) from None
        except (URLError, TimeoutError, OSError):
            raise SearchError(
                "The API connection failed. Check request history before retrying."
            ) from None
        except (ValueError, UnicodeError):
            raise SearchError("The API returned invalid JSON.") from None
        if (
            not isinstance(body, dict)
            or body.get("success") is False
            or body.get("error")
        ):
            raise SearchError("Search failed. Check the request history for details.")
        organic = body.get("organic", [])
        if not isinstance(organic, list):
            raise SearchError("The API returned an unexpected result format.")
        items = [
            {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "position": item.get("position"),
            }
            for item in organic[:number]
            if isinstance(item, dict)
        ]
        return {
            "status": "succeeded",
            "success": True,
            "query": query,
            "trace_id": str(body.get("trace_id") or trace_id),
            "organic": items,
        }

    async def search(self, query: str, number: int = 3) -> dict[str, Any]:
        """Search the web without blocking AstrBot's event loop.

        Args:
            query: Search text.
            number: Result count, from 1 to 20.

        Returns:
            Structured web results.

        Raises:
            SearchError: If input or the API response is invalid.
        """
        query = query.strip()
        if not query or len(query) > 2048:
            raise SearchError("Provide a search query of 1–2048 characters.")
        if (
            not isinstance(number, int)
            or isinstance(number, bool)
            or not 1 <= number <= 20
        ):
            raise SearchError("Result count must be an integer from 1 to 20.")
        return await asyncio.to_thread(self._search, query, number)
