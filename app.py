from agent.researcher import run_research
from agent.trader import run_trader

def main(stock_code: str):
    """
    Main workflow to run the stock trading agent.
    1. Runs the researcher agent to gather information.
    2. Runs the trader agent to make a decision.
    3. Prints the final decision.
    """
    print(f"--- Starting Trading Workflow for Stock: {stock_code} ---")

    # 1. Run the researcher agent
    report = run_research(stock_code)

    # 2. Run the trader agent
    decision = run_trader(report)

    # 3. Print the final result
    print("\n" + "="*50)
    print(f"Master Workflow Complete. Final Decision for {stock_code}: {decision.upper()}")
    print("="*50)

if __name__ == "__main__":
    # Using Samsung Electronics as an example
    samsung_stock_code = "005930"
    main(samsung_stock_code)
