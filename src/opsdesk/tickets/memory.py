from opsdesk.contracts.tickets import Ticket

DEFAULT_TICKETS = [
    Ticket(
        id="TCK-101",
        title="VPN disconnects after sleep",
        status="open",
        requester="ana@company.com",
        summary="VPN drops when the laptop sleeps. Workaround: reconnect from Settings > Network.",
    ),
    Ticket(
        id="TCK-102",
        title="New laptop request",
        status="closed",
        requester="juan@company.com",
        summary="Replacement laptop delivered on 2026-08-12.",
    ),
    Ticket(
        id="TCK-103",
        title="GitHub org access",
        status="in_progress",
        requester="mia@company.com",
        summary="Waiting on manager approval to add the user to the engineering org.",
    ),
]


class InMemoryTicketStore:
    def __init__(self, tickets: list[Ticket] | None = None) -> None:
        seed = tickets if tickets is not None else DEFAULT_TICKETS
        self._tickets = {ticket.id: ticket for ticket in seed}

    def get(self, ticket_id: str) -> Ticket | None:
        return self._tickets.get(ticket_id)
