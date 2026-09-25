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

    def create(self, *, title: str, requester: str, summary: str) -> Ticket:
        ticket = Ticket(
            id=self._next_id(),
            title=title,
            status="open",
            requester=requester,
            summary=summary,
        )
        self._tickets[ticket.id] = ticket
        return ticket

    def _next_id(self) -> str:
        numbers: list[int] = []
        for ticket_id in self._tickets:
            suffix = ticket_id.removeprefix("TCK-")
            if suffix.isdigit():
                numbers.append(int(suffix))
        return f"TCK-{max(numbers, default=100) + 1}"
