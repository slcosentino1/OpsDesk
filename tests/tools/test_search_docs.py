from unittest.mock import MagicMock
from uuid import uuid4

from opsdesk.contracts.askdoc import QueryMatch, SearchMatchesRequest, SearchMatchesResponse
from opsdesk.tools.search_docs import search_docs


def test_search_docs_formats_matches():
    client = MagicMock()
    client.search_matches.return_value = SearchMatchesResponse(
        query="vpn reset",
        matches=[
            QueryMatch(
                chunk_id=uuid4(),
                job_id=uuid4(),
                file_name="vpn.md",
                chunk_index=0,
                text="Reset VPN from Settings > Network.",
                score=0.91,
            )
        ],
    )

    output = search_docs(client, "vpn reset")

    client.search_matches.assert_called_once_with(SearchMatchesRequest(query="vpn reset"))
    assert "vpn.md" in output
    assert "Reset VPN from Settings > Network." in output


def test_search_docs_empty_matches():
    client = MagicMock()
    client.search_matches.return_value = SearchMatchesResponse(query="unknown", matches=[])

    output = search_docs(client, "unknown")

    assert output == "No documentation matches found."
