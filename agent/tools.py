from agent.core.workflows import tool
import requests

# 증권사 리포트 조회 Tool
@tool(name='fetch_report')
def get_stock_reports(stock_code):
    """
    주어진 주식 코드에 대한 증권사 리포트를 조회합니다.
    이 함수는 현재 더미 데이터를 반환합니다.

    Args:
        stock_code (str): 조회할 주식의 종목 코드.

    Returns:
        str: 조회된 리포트 정보를 담은 문자열.
    """
    # Dummy Code : X-API 
    return f"{stock_code} 관련 증권사 리포트: 'Buy, 목표가 80,000원' 입니다."

# 뉴스 조회 Tool
@tool(name='fetch_news')
def get_stock_news(stock_code):
    """
    주어진 주식 코드에 대한 최신 뉴스를 조회합니다.
    이 함수는 현재 더미 데이터를 반환합니다.

    Args:
        stock_code (str): 조회할 주식의 종목 코드.

    Returns:
        str: 조회된 최신 뉴스 정보를 담은 문자열.
    """
    # Dummy Code : Crawling
    return f"{stock_code} 관련 최신 뉴스: '시장 점유율 확대 중' 입니다."


# 현재 주식 가격 조회 Tool
@tool(name='fetch_price')
def get_stock_price(stock_code):
    """
    주어진 주식 코드의 현재 주가를 조회합니다.
    이 함수는 현재 더미 데이터를 반환합니다.

    Args:
        stock_code (str): 조회할 주식의 종목 코드.

    Returns:
        str: 조회된 현재 주가 정보를 담은 문자열.
    """
    # Dummy Code : Crawling
    return f"{stock_code} 현재 주가는 : '72,000원' 입니다."
