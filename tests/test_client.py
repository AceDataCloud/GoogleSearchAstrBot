"""Synchronous search contract and bounded output."""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from client import GoogleSearchClient, SearchError


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload
        self.headers = {"x-trace-id": "trace-search"}

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self, *_):
        return json.dumps(self.payload).encode()


@pytest.mark.asyncio
async def test_search_posts_once_and_returns_public_fields():
    captured = []

    def fake_open(request, timeout):
        captured.append((request.full_url, json.loads(request.data), timeout))
        return FakeResponse(
            {
                "organic": [
                    {
                        "title": "AstrBot Docs",
                        "link": "https://astrbot.app/docs",
                        "snippet": "Plugin guide",
                        "position": 1,
                        "supplier": "internal-only",
                    }
                ]
            }
        )

    with patch("client.OPENER.open", side_effect=fake_open):
        result = await GoogleSearchClient("test-key").search("AstrBot plugin", 3)
    assert captured == [
        (
            "https://api.acedata.cloud/serp/google",
            {"query": "AstrBot plugin", "number": 3, "page": 1, "type": "search"},
            60,
        )
    ]
    assert result["status"] == "succeeded"
    assert result["trace_id"] == "trace-search"
    assert result["organic"] == [
        {
            "title": "AstrBot Docs",
            "link": "https://astrbot.app/docs",
            "snippet": "Plugin guide",
            "position": 1,
        }
    ]


@pytest.mark.asyncio
async def test_invalid_input_does_not_make_a_request():
    with patch("client.OPENER.open") as opening, pytest.raises(SearchError):
        await GoogleSearchClient("test-key").search("", 3)
    assert opening.call_count == 0
