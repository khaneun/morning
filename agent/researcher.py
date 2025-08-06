from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from config.setting import API_CONFIG
from pydantic import BaseModel
import agent.tools
from agent.core.tool_registry import TOOLS


llm = ChatOpenAI(
    model=API_CONFIG['OPENAI']['MODEL_NAME'],
    temperature=API_CONFIG['OPENAI']['TEMPERATURE'],
    openai_api_key=API_CONFIG['OPENAI']['ACCESS_KEY']
)

class ResearchState(BaseModel):
    stock_code: str
    info_log: list[str] = []
    next_action: str = ""

# Dispatcher
def decide_next_action(state: ResearchState) -> ResearchState:
    context = "\n".join(state.info_log)
    prompt = f"""
        You are a financial researcher. Your goal is to gather information about a stock.

        Current stock code: {state.stock_code}
        Information gathered so far:
        {context}

        What do you want to do next?
        1. Fetch news (fetch_news)
        2. Fetch analyst reports (fetch_report)
        3. Fetch current price (fetch_price)
        4. Finish research (end)

        Choose one of: 'fetch_news', 'fetch_report', 'fetch_price', 'end'
    """
    print(f"Researcher Prompt: {prompt}")
    response = llm.invoke(prompt)
    decision = response.content.strip().lower()
    if decision not in ["fetch_news", "fetch_report", "fetch_price", "end"]:
        decision = "end"
    state.next_action = decision
    state.info_log.append(f"LLM Decision: {decision}")
    return state

def tool_wrapper(tool_func, state: ResearchState) -> ResearchState:
    result = tool_func(state.stock_code)
    state.info_log.append(result)
    return state

def generate_report(state: ResearchState) -> ResearchState:
    report = "\n".join(state.info_log)
    state.info_log.append(f"Final Report:\n{report}")
    return state


# Research workflow
builder = StateGraph(ResearchState)
builder.add_node("fetch_news", lambda s : tool_wrapper(TOOLS["fetch_news"], s))
builder.add_node("fetch_report", lambda s : tool_wrapper(TOOLS["fetch_report"], s))
builder.add_node("fetch_price", lambda s : tool_wrapper(TOOLS["fetch_price"], s))
builder.add_node("decide", decide_next_action)
builder.add_node("report", generate_report)

builder.add_conditional_edges(
    "decide",
    lambda state: state.next_action or "end",
    {
        "fetch_news" : "fetch_news",
        "fetch_report": "fetch_report",
        "fetch_price": "fetch_price",
        "end" : "report"
    })

builder.add_edge("fetch_news", "decide")
builder.add_edge("fetch_report", "decide")
builder.add_edge("fetch_price", "decide")
builder.set_entry_point("decide")
builder.add_edge("report", "__end__")

graph = builder.compile()

def run_research(stock_code: str) -> str:
    initial_state = ResearchState(stock_code=stock_code)
    result_state = graph.invoke(initial_state)
    final_report = result_state['info_log'][-1]
    print("--- Research Complete ---")
    print(final_report)
    return final_report
