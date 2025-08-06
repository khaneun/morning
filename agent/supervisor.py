from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from agent.worker import news_agent, report_agent, price_agent
from config.setting import API_CONFIG

# Define the LLM for the supervisor
llm = ChatOpenAI(
    model=API_CONFIG['OPENAI']['MODEL_NAME'],
    temperature=API_CONFIG['OPENAI']['TEMPERATURE'],
    openai_api_key=API_CONFIG['OPENAI']['ACCESS_KEY']
)

# The state is shared between the supervisor and the workers
class StockState(BaseModel):
    stock_code: str
    info_log: list[str] = []
    next_action: str = ""

def supervisor_node(state: StockState) -> StockState:
    """The supervisor node that decides the next action."""
    context = "\n".join(state.info_log)
    prompt = f"""
        당신은 주식 분석을 총괄하는 슈퍼바이저입니다.
        현재 주식 코드: {state.stock_code}
        지금까지 수집한 정보:
        {context}

        다음 단계로 어떤 워커를 호출하시겠습니까?
        - 뉴스 분석이 필요하면 'fetch_news'
        - 리포트 분석이 필요하면 'fetch_report'
        - 현재가 조회가 필요하면 'fetch_price'
        - 분석이 충분하면 'end'

        'fetch_news', 'fetch_report', 'fetch_price', 'end' 중 하나만 선택해서 답변하세요.
    """
    print("--- 슈퍼바이저 결정 ---")
    print(f"Prompt: {prompt}")
    response = llm.invoke(prompt)
    decision = response.content.strip().lower()

    if decision not in ["fetch_news", "fetch_report", "fetch_price", "end"]:
        decision = "end"

    print(f"결정: {decision}")
    state.next_action = decision
    return state

# Create the supervisor graph
builder = StateGraph(StockState)

builder.add_node("supervisor", supervisor_node)
builder.add_node("fetch_news_worker", lambda state: news_agent.invoke(state))
builder.add_node("fetch_report_worker", lambda state: report_agent.invoke(state))
builder.add_node("fetch_price_worker", lambda state: price_agent.invoke(state))

# The supervisor decides which worker to call
builder.add_conditional_edges(
    "supervisor",
    lambda state: state.next_action,
    {
        "fetch_news": "fetch_news_worker",
        "fetch_report": "fetch_report_worker",
        "fetch_price": "fetch_price_worker",
        "end": END,
    },
)

# After a worker is done, it goes back to the supervisor to decide the next step
builder.add_edge("fetch_news_worker", "supervisor")
builder.add_edge("fetch_report_worker", "supervisor")
builder.add_edge("fetch_price_worker", "supervisor")

builder.set_entry_point("supervisor")

# The final graph is the supervisor graph
supervisor_graph = builder.compile()
