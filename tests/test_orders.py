import pytest
from unittest.mock import MagicMock
from trading_bot.bot.orders import OrderManager
from trading_bot.bot.client import BinanceClient

@pytest.fixture
def mock_client():
    client = MagicMock(spec=BinanceClient)
    return client

def test_execute_order_success(mock_client):
    manager = OrderManager(mock_client)
    mock_client.place_order.return_value = {"orderId": 12345, "status": "NEW"}
    
    response = manager.execute_order(
        symbol="BTCUSDT",
        side="BUY",
        order_type="MARKET",
        quantity=0.001
    )
    
    assert response["orderId"] == 12345
    mock_client.place_order.assert_called_once()
