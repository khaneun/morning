from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from config.setting import API_CONFIG
from pydantic import BaseModel

llm = ChatOpenAI(
    model=API_CONFIG['OPENAI']['MODEL_NAME'],
    temperature=API_CONFIG['OPENAI']['TEMPERATURE'],
    openai_api_key=API_CONFIG['OPENAI']['ACCESS_KEY']
)

class TraderState(BaseModel):
    report: str
    decision: str = ""

def make_decision(state: TraderState) -> TraderState:
    report = state['report']
    prompt = f"""
        You are a professional stock trader. Your task is to make a trading decision based on the provided research report.

        Research Report:
        ---
        {report}
        ---

        Based on this report, should you 'buy', 'sell', or 'hold' the stock?
        Only respond with 'buy', 'sell', or 'hold'.
    """
    print(f"Trader Prompt: {prompt}")
    response = llm.invoke(prompt)
    decision = response.content.strip().lower()
    if decision not in ['buy', 'sell', 'hold']:
        decision = 'hold' # Default to a safe action

    state['decision'] = decision
    print(f"Trader Decision: {decision}")
    return state

# Trader workflow
builder = StateGraph(TraderState)
builder.add_node("make_decision", make_decision)
builder.add_edge("make_decision", END)
builder.set_entry_point("make_decision")

graph = builder.compile()

def run_trader(report: str) -> str:
    initial_state = {"report": report}
    result_state = graph.invoke(initial_state)
    decision = result_state['decision']
    print(f"--- Trader Final Decision: {decision} ---")
    return decision
