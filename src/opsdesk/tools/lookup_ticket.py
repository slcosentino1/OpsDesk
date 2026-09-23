from opsdesk.contracts.tickets import Ticket
from opsdesk.tickets.memory import InMemoryTicketStore

LOOKUP_TICKET_TOOL = {
    "type": "function",
    "function": {
        "name": "lookup_ticket",
        "description": (
            "Look up an internal support ticket by id (for example TCK-101). "
            "Use when the user asks about the status or details of a ticket."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "string",
                    "description": "Ticket id, for example TCK-101.",
                }
            },
            "required": ["ticket_id"],
        },
    },
}


def _format_ticket(ticket: Ticket) -> str:
    return (
        f"[{ticket.id}] {ticket.title}\n"
        f"status: {ticket.status}\n"
        f"requester: {ticket.requester}\n"
        f"{ticket.summary}"
    )


def lookup_ticket(store: InMemoryTicketStore, ticket_id: str) -> str:
    ticket = store.get(ticket_id)
    if ticket is None:
        return f"No ticket found for id {ticket_id}."
    return _format_ticket(ticket)
