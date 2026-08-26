import sys

from opsdesk.graph.agent import build_agent


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        print("Usage: python -m opsdesk '<question>'", file=sys.stderr)
        raise SystemExit(1)

    agent = build_agent()
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
