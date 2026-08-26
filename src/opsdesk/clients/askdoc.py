from __future__ import annotations

import httpx

from opsdesk.contracts.askdoc import SearchMatchesRequest, SearchMatchesResponse
from opsdesk.settings import get_settings

SEARCH_MATCHES_PATH = "/api/askdoc/search-matches"


class AskDocClient:
    """HTTP client for AskDoc. Retrieval only — do not call /query from the agent."""

    def __init__(
        self,
        base_url: str | None = None,
        *,
        timeout: float = 30.0,
        client: httpx.Client | None = None,
    ) -> None:
        self._base_url = (base_url or get_settings().askdoc_base_url).rstrip("/")
        self._owns_client = client is None
        self._client = client or httpx.Client(base_url=self._base_url, timeout=timeout)

    def search_matches(self, request: SearchMatchesRequest) -> SearchMatchesResponse:
        response = self._client.post(
            SEARCH_MATCHES_PATH,
            json=request.model_dump(),
        )
        response.raise_for_status()
        return SearchMatchesResponse.model_validate(response.json())

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> AskDocClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
