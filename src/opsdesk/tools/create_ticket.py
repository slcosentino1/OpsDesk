from opsdesk.tickets.memory import InMemoryTicketStore
from opsdesk.tools.lookup_ticket import _format_ticket

CREATE_TICKET_TOOL = {
    "type": "function",
    "function": {
        "name": "create_ticket",
        "description": (
            "Create a new internal support ticket. "
            "Use when the user wants to open a ticket and you have a title, "
            "requester, and a short summary of the problem."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Short ticket title.",
                },
                "requester": {
                    "type": "string",
                    "description": "Who is asking, typically an email.",
                },
                "summary": {
                    "type": "string",
                    "description": "Short description of the problem.",
                },
            },
            "required": ["title", "requester", "summary"],
        },
    },
}


def create_ticket(
    store: InMemoryTicketStore,
    *,
    title: str,
    requester: str,
    summary: str,
) -> str:
    ticket = store.create(title=title, requester=requester, summary=summary)
    return f"Created ticket {ticket.id}.\n{_format_ticket(ticket)}"
