import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.supervisor import supervisor_graph, StockState
from agent.worker import news_agent, report_agent, price_agent

class TestAgents(unittest.TestCase):

    def test_worker_agents_invocation(self):
        """Test that worker agents can be invoked without errors."""
        initial_state = StockState(stock_code="005930")

        # Test news_agent
        result = news_agent.invoke(initial_state)
        self.assertIn("[FETCH_NEWS_AGENT] 결과:", result['info_log'][-1])

        # Test report_agent
        result = report_agent.invoke(initial_state)
        self.assertIn("[FETCH_REPORT_AGENT] 결과:", result['info_log'][-1])

        # Test price_agent
        result = price_agent.invoke(initial_state)
        self.assertIn("[FETCH_PRICE_AGENT] 결과:", result['info_log'][-1])

    @patch('agent.supervisor.llm')
    def test_supervisor_routing_to_news(self, mock_llm):
        """Test that the supervisor correctly routes to the news worker."""

        # Configure the mock's invoke method
        mock_llm.invoke.side_effect = [
            MagicMock(content="fetch_news"),
            MagicMock(content="end")
        ]

        initial_state = StockState(stock_code="005930", info_log=["분석 시작"])
        final_state = supervisor_graph.invoke(initial_state)

        # Check that the news agent was called
        self.assertTrue(any("[FETCH_NEWS_AGENT] 결과:" in log for log in final_state['info_log']))
        # Check that other agents were not called
        self.assertFalse(any("[FETCH_REPORT_AGENT] 결과:" in log for log in final_state['info_log']))

    @patch('agent.supervisor.llm')
    def test_supervisor_routing_to_report(self, mock_llm):
        """Test that the supervisor correctly routes to the report worker."""

        # Configure the mock's invoke method
        mock_llm.invoke.side_effect = [
            MagicMock(content="fetch_report"),
            MagicMock(content="end")
        ]

        initial_state = StockState(stock_code="005930", info_log=["분석 시작"])
        final_state = supervisor_graph.invoke(initial_state)

        # Check that the report agent was called
        self.assertTrue(any("[FETCH_REPORT_AGENT] 결과:" in log for log in final_state['info_log']))
        self.assertFalse(any("[FETCH_NEWS_AGENT] 결과:" in log for log in final_state['info_log']))


if __name__ == '__main__':
    unittest.main()
