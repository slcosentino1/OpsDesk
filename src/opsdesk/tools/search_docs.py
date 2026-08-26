from opsdesk.clients.askdoc import AskDocClient
from opsdesk.contracts.askdoc import QueryMatch, SearchMatchesRequest, SearchMatchesResponse

SEARCH_DOCS_TOOL = {
    "type": "function",
    "function": {
        "name": "search_docs",
        "description": (
            "Search internal documentation via AskDoc. "
            "Use when the answer may be in company docs. "
            "Returns retrieved passages only; you write the final answer."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for internal documentation.",
                }
            },
            "required": ["query"],
        },
    },
}


def _format_match(match: QueryMatch) -> str:
    return (
        f"[{match.file_name} #{match.chunk_index} score={match.score:.2f}]\n{match.text}"
    )


def _format_matches(response: SearchMatchesResponse) -> str:
    if not response.matches:
        return "No documentation matches found."
    return "\n\n".join(_format_match(match) for match in response.matches)


def search_docs(client: AskDocClient, query: str) -> str:
    result = client.search_matches(SearchMatchesRequest(query=query))
    return _format_matches(result)
