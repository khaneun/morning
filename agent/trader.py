from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from config.setting import API_CONFIG
from pydantic import BaseModel, Field
import json
import re

# Import tools and the registry
import agent.tools
from agent.core.tool_registry import TOOLS

llm = ChatOpenAI(
    model=API_CONFIG['OPENAI']['MODEL_NAME'],
    temperature=API_CONFIG['OPENAI']['TEMPERATURE'],
    openai_api_key=API_CONFIG['OPENAI']['ACCESS_KEY']
)

class TraderState(BaseModel):
    report: str
    stock_code: str
    decision: str = ""
    quantity: int = 0
    current_price: int = 0
    trade_result: str = ""

def make_decision(state: TraderState) -> TraderState:
    report = state['report']
    stock_code = state['stock_code']

    prompt = f"""
        You are a professional stock trader. Your task is to make a trading decision based on the provided research report.

        Research Report for stock code {stock_code}:
        ---
        {report}
        ---

        Based on this report, should you 'buy', 'sell', or 'hold' the stock?
        If you decide to buy or sell, specify a quantity of 1 share for this transaction.

        Respond with a JSON object in the following format:
        {{
            "decision": "buy" | "sell" | "hold",
            "quantity": 1
        }}
    """
    print(f"Trader Prompt: {prompt}")
    response = llm.invoke(prompt)

    try:
        # Extract JSON from the response
        json_str = response.content.strip()
        decision_data = json.loads(json_str)

        decision = decision_data.get('decision', 'hold').lower()
        quantity = decision_data.get('quantity', 0)

        if decision not in ['buy', 'sell', 'hold']:
            decision = 'hold'

        state['decision'] = decision
        state['quantity'] = quantity if decision != 'hold' else 0
        print(f"Trader Decision: {decision}, Quantity: {state['quantity']}")

    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing LLM response: {e}. Defaulting to 'hold'.")
        state['decision'] = 'hold'
        state['quantity'] = 0

    return state

def get_price_node(state: TraderState) -> TraderState:
    stock_code = state['stock_code']
    print(f"Fetching price for {stock_code}...")
    price_str = TOOLS['fetch_price'](stock_code)

    # Extract the number from the string '현재 005930의 가격은 75000원 입니다.'
    price_match = re.search(r'(\d+)원', price_str)
    if price_match:
        price = int(price_match.group(1))
        state['current_price'] = price
        print(f"Current price for {stock_code} is {price}.")
    else:
        print("Could not parse price from string. Cannot execute trade.")
        # If price fetch fails, we can't trade. Force a hold.
        state['decision'] = 'hold'
    return state

def execute_trade(state: TraderState) -> TraderState:
    decision = state['decision']
    stock_code = state['stock_code']
    quantity = state['quantity']
    price = state['current_price']

    print(f"Executing trade: {decision} {quantity} shares of {stock_code} at {price}")

    if decision == 'buy':
        result = TOOLS['buy_stock'](stock_code, quantity, price)
    elif decision == 'sell':
        result = TOOLS['sell_stock'](stock_code, quantity, price)
    else:
        result = "No action taken."

    state['trade_result'] = result
    print(f"Trade Result: {result}")
    return state

def should_trade(state: TraderState) -> str:
    """Conditional edge to decide if we should execute a trade."""
    if state['decision'] in ['buy', 'sell'] and state['quantity'] > 0:
        return "get_price"
    else:
        return "end"

# Trader workflow
builder = StateGraph(TraderState)
builder.add_node("make_decision", make_decision)
builder.add_node("get_price", get_price_node)
builder.add_node("execute_trade", execute_trade)

builder.set_entry_point("make_decision")
builder.add_conditional_edges(
    "make_decision",
    should_trade,
    {
        "get_price": "get_price",
        "end": END
    }
)
builder.add_edge("get_price", "execute_trade")
builder.add_edge("execute_trade", END)

graph = builder.compile()

def run_trader(report: str, stock_code: str) -> dict:
    initial_state = {"report": report, "stock_code": stock_code}
    result_state = graph.invoke(initial_state)

    final_decision = {
        "decision": result_state.get('decision'),
        "trade_result": result_state.get('trade_result', 'No trade executed.')
    }
    print(f"--- Trader Final State: {final_decision} ---")
    return final_decision
