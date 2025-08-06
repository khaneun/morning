from agent.supervisor import supervisor_graph, StockState

def run(stock_code):
    """
    주어진 주식 코드에 대해 멀티 에이전트 기반의 주식 분석 시스템을 실행합니다.

    이 함수는 시스템의 메인 진입점(entry point) 역할을 합니다.
    초기 상태를 설정하고, 슈퍼바이저 그래프를 호출하여 분석을 시작합니다.
    분석이 완료되면 최종 결과를 콘솔에 출력합니다.

    Args:
        stock_code (str): 분석할 주식의 종목 코드.
    """
    initial_state = StockState(stock_code=stock_code, info_log=["분석 시작"])

    # Invoke the supervisor graph
    result_state = supervisor_graph.invoke(initial_state)

    print("\n--- 최종 분석 결과 ---")
    print("\n".join(result_state['info_log']))
    print("--------------------")
