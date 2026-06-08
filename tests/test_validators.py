import pytest
from trading_bot.bot.validators import OrderRequest, OrderType, OrderSide
from pydantic import ValidationError

def test_valid_market_order():
    request = OrderRequest(
        symbol="BTCUSDT",
        side=OrderSide.BUY,
        order_type=OrderType.MARKET,
        quantity=0.001
    )
    assert request.symbol == "BTCUSDT"
    assert request.quantity == 0.001

def test_invalid_limit_order_no_price():
    with pytest.raises(ValidationError):
        OrderRequest(
            symbol="BTCUSDT",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=0.001
            # price missing
        )

def test_valid_limit_order():
    request = OrderRequest(
        symbol="BTCUSDT",
        side=OrderSide.BUY,
        order_type=OrderType.LIMIT,
        quantity=0.001,
        price=60000.0
    )
    assert request.price == 60000.0

def test_invalid_stop_limit_no_stop_price():
    with pytest.raises(ValidationError):
        OrderRequest(
            symbol="BTCUSDT",
            side=OrderSide.BUY,
            order_type=OrderType.STOP_LIMIT,
            quantity=0.001,
            price=61000.0
            # stop_price missing
        )
