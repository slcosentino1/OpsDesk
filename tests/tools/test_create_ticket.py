from opsdesk.tickets.memory import InMemoryTicketStore
from opsdesk.tools.create_ticket import create_ticket
from opsdesk.tools.lookup_ticket import lookup_ticket


def test_create_ticket_assigns_next_id_and_is_lookupable():
    store = InMemoryTicketStore(tickets=[])

    created = create_ticket(
        store,
        title="VPN not connecting",
        requester="ana@company.com",
        summary="Cannot connect after the last laptop update.",
    )

    assert "TCK-101" in created
    assert "open" in created
    assert lookup_ticket(store, "TCK-101").startswith("[TCK-101]")


def test_create_ticket_increments_after_seed():
    store = InMemoryTicketStore()

    created = create_ticket(
        store,
        title="Email signature",
        requester="juan@company.com",
        summary="Need the new company signature.",
    )

    assert "TCK-104" in created
    assert store.get("TCK-104") is not None
    assert store.get("TCK-104").status == "open"
