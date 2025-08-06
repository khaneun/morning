from agent.core.tool_registry import tool
from api.ki import kis_auth, kis_domstk
import pandas as pd

# --- KIS API Initialization ---

_KIS_API_INITIALIZED = False

def _initialize_kis_api():
    """
    Authenticates with the KIS API if not already authenticated.
    This function should be called by any tool that needs the API.
    """
    global _KIS_API_INITIALIZED
    if not _KIS_API_INITIALIZED:
        # For now, we will use the production environment.
        # 모의투자를 사용하려면 'vps'로 변경
        kis_auth.auth(svr='prod')
        _KIS_API_INITIALIZED = True
        print("KIS API Initialized.")

# --- Real KIS API Tools ---

@tool(name='fetch_price')
def get_stock_price(stock_code: str) -> str:
    """
    Fetches the current price of a given stock code from the KIS API.
    Args:
        stock_code (str): The 6-digit stock code (e.g., "005930").
    Returns:
        str: A string containing the current price information, or an error message.
    """
    _initialize_kis_api()
    try:
        # FHKST01010100 주식현재가 시세
        res = kis_domstk.get_inquire_price(itm_no=stock_code)
        if res.isOK():
            price = res.getBody().output['stck_prpr']
            return f"현재 {stock_code}의 가격은 {price}원 입니다."
        else:
            return f"가격 조회 실패: {res.getErrorMessage()}"
    except Exception as e:
        return f"가격 조회 중 오류 발생: {e}"

@tool(name='buy_stock')
def buy_stock(stock_code: str, quantity: int, price: int) -> str:
    """
    Places a cash buy order for a given stock.
    Args:
        stock_code (str): The 6-digit stock code.
        quantity (int): The number of shares to buy.
        price (int): The price per share.
    Returns:
        str: A confirmation message or an error message.
    """
    _initialize_kis_api()
    try:
        # TTTC0802U 주식 현금 매수 주문
        res = kis_domstk.get_order_cash(ord_dv="buy", itm_no=stock_code, qty=quantity, unpr=price)
        if res is not None and str(res.getBody().rt_cd) == "0":
            order_num = res.getBody().output['ODNO']
            return f"매수 주문 성공. 주문번호: {order_num}"
        else:
            return f"매수 주문 실패: {res.getBody().msg1 if res else '응답 없음'}"
    except Exception as e:
        return f"매수 주문 중 오류 발생: {e}"

@tool(name='sell_stock')
def sell_stock(stock_code: str, quantity: int, price: int) -> str:
    """
    Places a cash sell order for a given stock.
    Args:
        stock_code (str): The 6-digit stock code.
        quantity (int): The number of shares to sell.
        price (int): The price per share.
    Returns:
        str: A confirmation message or an error message.
    """
    _initialize_kis_api()
    try:
        # TTTC0801U 주식 현금 매도 주문
        res = kis_domstk.get_order_cash(ord_dv="sell", itm_no=stock_code, qty=quantity, unpr=price)
        if res is not None and str(res.getBody().rt_cd) == "0":
            order_num = res.getBody().output['ODNO']
            return f"매도 주문 성공. 주문번호: {order_num}"
        else:
            return f"매도 주문 실패: {res.getBody().msg1 if res else '응답 없음'}"
    except Exception as e:
        return f"매도 주문 중 오류 발생: {e}"

@tool(name='get_balance')
def get_balance() -> str:
    """
    Fetches the current account balance and portfolio.
    Returns:
        str: A string detailing the account balance and holdings.
    """
    _initialize_kis_api()
    try:
        # TTTC8434R 주식잔고조회
        res = kis_domstk.get_inquire_balance_lst()
        if res is not None:
            # res is a DataFrame here
            holdings = res[['pdno', 'prdt_name', 'hldg_qty', 'prpr', 'evlu_amt']]
            holdings_str = holdings.to_string(index=False)

            # Get cash balance
            res_cash = kis_domstk.get_inquire_balance_obj()
            cash = res_cash.getBody().output2[0]['dnca_tot_amt']

            return f"--- 계좌 잔고 ---\n주문가능현금: {cash}원\n\n--- 보유 주식 ---\n{holdings_str}"
        else:
            return "잔고 조회 실패: 응답 없음"
    except Exception as e:
        return f"잔고 조회 중 오류 발생: {e}"

# --- Dummy Tools (Kept for compatibility with researcher agent) ---

@tool(name='fetch_report')
def get_stock_reports(stock_code: str) -> str:
    """(Dummy) Fetches analyst reports for a stock."""
    return f"{stock_code} 관련 증권사 리포트: '긍정적 전망, 목표가 상향 조정' (Dummy Data)"

@tool(name='fetch_news')
def get_stock_news(stock_code: str) -> str:
    """(Dummy) Fetches recent news for a stock."""
    return f"{stock_code} 관련 최신 뉴스: '신기술 개발 성공, 시장 기대감 상승' (Dummy Data)"
