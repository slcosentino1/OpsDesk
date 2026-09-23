from opsdesk.contracts.tickets import Ticket
from opsdesk.tickets.memory import InMemoryTicketStore
from opsdesk.tools.lookup_ticket import lookup_ticket


def test_lookup_ticket_formats_found_ticket():
    store = InMemoryTicketStore(
        tickets=[
            Ticket(
                id="TCK-101",
                title="VPN disconnects after sleep",
                status="open",
                requester="ana@company.com",
                summary="Reconnect from Settings > Network.",
            )
        ]
    )

    output = lookup_ticket(store, "TCK-101")

    assert "TCK-101" in output
    assert "open" in output
    assert "Reconnect from Settings > Network." in output


def test_lookup_ticket_missing_id():
    store = InMemoryTicketStore(tickets=[])

    output = lookup_ticket(store, "TCK-999")

    assert output == "No ticket found for id TCK-999."


def test_default_store_has_seed_tickets():
    store = InMemoryTicketStore()

    assert store.get("TCK-101") is not None
    assert store.get("TCK-999") is None
