import unittest
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.tools import get_stock_reports, get_stock_news, get_stock_price

class TestTools(unittest.TestCase):

    def test_get_stock_reports(self):
        stock_code = "005930"
        expected_output = f"{stock_code} 관련 증권사 리포트: 'Buy, 목표가 80,000원' 입니다."
        self.assertEqual(get_stock_reports(stock_code), expected_output)

    def test_get_stock_news(self):
        stock_code = "005930"
        expected_output = f"{stock_code} 관련 최신 뉴스: '시장 점유율 확대 중' 입니다."
        self.assertEqual(get_stock_news(stock_code), expected_output)

    def test_get_stock_price(self):
        stock_code = "005930"
        expected_output = f"{stock_code} 현재 주가는 : '72,000원' 입니다."
        self.assertEqual(get_stock_price(stock_code), expected_output)

if __name__ == '__main__':
    unittest.main()
