"""Google Search Agent tool for AstrBot."""

from __future__ import annotations

import json

from astrbot.api import AstrBotConfig
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star

from .client import GoogleSearchClient, SearchError


class GoogleSearchPlugin(Star):
    """Search the web from an AstrBot conversation."""

    def __init__(self, context: Context, config: AstrBotConfig) -> None:
        """Receive the API key from AstrBot plugin configuration.

        Args:
            context: AstrBot plugin context.
            config: Plugin configuration with a masked API-key field.
        """
        super().__init__(context)
        self.config = config

    @filter.llm_tool(name="google_search")
    async def google_search(
        self, event: AstrMessageEvent, query: str, number: int = 3
    ) -> str:
        """Find current Google web results with titles, links, and snippets.

        Args:
            query(string): Web search query.
            number(number): Number of results to return, 1 to 20.

        Returns:
            JSON web results and a trace ID when the API provides one.
        """
        try:
            result = await GoogleSearchClient(self.config.get("api_key", "")).search(
                query, number
            )
        except SearchError as exc:
            result = {"status": "error", "message": str(exc)}
        return json.dumps(result, ensure_ascii=False)
