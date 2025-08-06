from agent.supervisor import supervisor_graph, StockState

def run(stock_code):
    """
    Runs the multi-agent stock analysis system.
    """
    initial_state = StockState(stock_code=stock_code, info_log=["분석 시작"])

    # Invoke the supervisor graph
    result_state = supervisor_graph.invoke(initial_state)

    print("\n--- 최종 분석 결과 ---")
    print("\n".join(result_state['info_log']))
    print("--------------------")
