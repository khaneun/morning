from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from agent.core.workflows import TOOLS

class StockState(BaseModel):
    stock_code: str
    info_log: list[str] = []
    next_action: str = ""

def tool_invoker(state: StockState, tool_name: str):
    """
    지정된 도구를 호출하고 그 결과를 상태(State)에 기록하는 노드 함수입니다.

    Args:
        state (StockState): 현재 상태를 담고 있는 Pydantic 모델. 'stock_code'를 포함해야 합니다.
        tool_name (str): 호출할 도구의 이름.

    Returns:
        StockState: 도구 실행 결과가 'info_log'에 추가된 업데이트된 상태.

    Raises:
        ValueError: 지정된 'tool_name'을 찾을 수 없을 때 발생합니다.
    """
    tool = TOOLS.get(tool_name)
    if not tool:
        raise ValueError(f"Tool '{tool_name}' not found.")

    result = tool.invoke(state.stock_code)
    state.info_log.append(f"[{tool_name.upper()}_AGENT] 결과: {result}")
    return state

def create_worker(tool_name: str) -> StateGraph:
    """
    단일 도구를 호출하는 간단한 워커(Worker) 에이전트 그래프를 생성합니다.

    이 팩토리 함수는 특정 도구를 실행하는 노드 하나만으로 구성된 StateGraph를 만듭니다.
    이를 통해 각 도구에 대한 전문화된 에이전트를 쉽게 생성할 수 있습니다.

    Args:
        tool_name (str): 워커가 사용할 도구의 이름.

    Returns:
        StateGraph: 컴파일된 워커 에이전트 그래프.
    """
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
