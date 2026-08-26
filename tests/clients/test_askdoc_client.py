from uuid import uuid4

import httpx
import pytest

from opsdesk.clients.askdoc import AskDocClient
from opsdesk.contracts.askdoc import SearchMatchesRequest


def _client_with_handler(handler):
    transport = httpx.MockTransport(handler)
    http = httpx.Client(transport=transport, base_url="http://askdoc.test")
    return AskDocClient(base_url="http://askdoc.test", client=http)


def test_search_matches_returns_typed_matches():
    chunk_id = uuid4()
    job_id = uuid4()

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/api/askdoc/search-matches"
        body = request.read()
        assert b"vpn reset" in body
        return httpx.Response(
            200,
            json={
                "query": "vpn reset",
                "matches": [
                    {
                        "chunk_id": str(chunk_id),
                        "job_id": str(job_id),
                        "file_name": "vpn.md",
                        "chunk_index": 0,
                        "text": "Reset VPN from Settings > Network.",
                        "score": 0.91,
                    }
                ],
            },
        )

    client = _client_with_handler(handler)
    result = client.search_matches(SearchMatchesRequest(query="vpn reset"))

    assert result.query == "vpn reset"
    assert len(result.matches) == 1
    match = result.matches[0]
    assert match.chunk_id == chunk_id
    assert match.job_id == job_id
    assert match.file_name == "vpn.md"
    assert match.text.startswith("Reset VPN")
    assert match.score == 0.91


def test_search_matches_raises_on_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"detail": "upstream failed"})

    client = _client_with_handler(handler)

    with pytest.raises(httpx.HTTPStatusError):
        client.search_matches(SearchMatchesRequest(query="anything"))
