from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from agent.core.workflows import TOOLS

class StockState(BaseModel):
    stock_code: str
    info_log: list[str] = []
    next_action: str = ""

def tool_invoker(state: StockState, tool_name: str):
    """A node that invokes a tool and returns the result."""
    tool = TOOLS.get(tool_name)
    if not tool:
        raise ValueError(f"Tool '{tool_name}' not found.")

    result = tool.invoke(state.stock_code)
    state.info_log.append(f"[{tool_name.upper()}_AGENT] 결과: {result}")
    return state

def create_worker(tool_name: str) -> StateGraph:
    """Creates a worker agent graph that invokes a single tool."""
    builder = StateGraph(StockState)

    # The worker's only job is to invoke the tool.
    builder.add_node(
        f"{tool_name}_node",
        lambda state: tool_invoker(state, tool_name)
    )

    # The graph starts and ends with this single node.
    builder.set_entry_point(f"{tool_name}_node")
    builder.add_edge(f"{tool_name}_node", END)

    return builder.compile()

# Create the worker agents
news_agent = create_worker("fetch_news")
report_agent = create_worker("fetch_report")
price_agent = create_worker("fetch_price")
