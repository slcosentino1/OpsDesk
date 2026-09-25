from __future__ import annotations

import json
import operator
from typing import Annotated, Any, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from openai import OpenAI

from opsdesk.clients.askdoc import AskDocClient
from opsdesk.settings import get_settings
from opsdesk.tickets.memory import InMemoryTicketStore
from opsdesk.tools.create_ticket import CREATE_TICKET_TOOL, create_ticket
from opsdesk.tools.lookup_ticket import LOOKUP_TICKET_TOOL, lookup_ticket
from opsdesk.tools.search_docs import SEARCH_DOCS_TOOL, search_docs

TOOLS = [SEARCH_DOCS_TOOL, LOOKUP_TICKET_TOOL, CREATE_TICKET_TOOL]

SYSTEM_PROMPT = (
    "You are an internal support agent. "
    "Use search_docs to retrieve company documentation before answering. "
    "Use lookup_ticket when the user asks about a ticket id such as TCK-101. "
    "Use create_ticket when the user wants to open a new ticket. "
    "Ground documentation answers in the retrieved passages. "
    "If nothing relevant is found, say so."
)


class AgentState(TypedDict):
    messages: Annotated[list[dict[str, Any]], operator.add]


def _assistant_message(message: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "role": "assistant",
        "content": message.content or "",
    }
    if message.tool_calls:
        payload["tool_calls"] = [
            {
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments,
                },
            }
            for tool_call in message.tool_calls
        ]
    return payload


def _run_tool(
    *,
    askdoc: AskDocClient,
    tickets: InMemoryTicketStore,
    name: str,
    arguments: dict[str, Any],
) -> str:
    if name == "search_docs":
        return search_docs(askdoc, query=arguments["query"])
    if name == "lookup_ticket":
        return lookup_ticket(tickets, ticket_id=arguments["ticket_id"])
    if name == "create_ticket":
        return create_ticket(
            tickets,
            title=arguments["title"],
            requester=arguments["requester"],
            summary=arguments["summary"],
        )
    return f"Unknown tool: {name}"


def build_agent(
    *,
    client: AskDocClient | None = None,
    tickets: InMemoryTicketStore | None = None,
    llm: OpenAI | None = None,
) -> CompiledStateGraph:
    settings = get_settings()
    askdoc = client or AskDocClient()
    ticket_store = tickets or InMemoryTicketStore()
    llm_client = llm or OpenAI(
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key,
    )

    def call_model(state: AgentState) -> dict[str, list[dict[str, Any]]]:
        response = llm_client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *state["messages"]],
            tools=TOOLS,
        )
        return {"messages": [_assistant_message(response.choices[0].message)]}

    def run_tools(state: AgentState) -> dict[str, list[dict[str, Any]]]:
        last = state["messages"][-1]
        outputs: list[dict[str, Any]] = []
        for tool_call in last.get("tool_calls") or []:
            arguments = json.loads(tool_call["function"]["arguments"] or "{}")
            outputs.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": _run_tool(
                        askdoc=askdoc,
                        tickets=ticket_store,
                        name=tool_call["function"]["name"],
                        arguments=arguments,
                    ),
                }
            )
        return {"messages": outputs}

    def route(state: AgentState) -> Literal["tools", "__end__"]:
        last = state["messages"][-1]
        if last.get("tool_calls"):
            return "tools"
        return END

    graph = StateGraph(AgentState)
    graph.add_node("model", call_model)
    graph.add_node("tools", run_tools)
    graph.add_edge(START, "model")
    graph.add_conditional_edges("model", route)
    graph.add_edge("tools", "model")
    return graph.compile()
