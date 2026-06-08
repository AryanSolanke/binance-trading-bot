import time
from .client import BinanceClient
from .validators import OrderRequest, OrderType, OrderSide
from .logging_config import logger
from typing import Optional

class OrderManager:
    def __init__(self, client: BinanceClient):
        self.client = client

    def execute_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        stop_price: Optional[float] = None
    ):
        """Orchestrates the order placement process."""
        try:
            # 1. Validate Input
            request = OrderRequest(
                symbol=symbol,
                side=OrderSide(side.upper()),
                order_type=OrderType(order_type.upper()),
                quantity=quantity,
                price=price,
                stop_price=stop_price
            )
            
            # 2. Place Order
            response = self.client.place_order(request)
            
            # 3. For MARKET orders, poll for a few seconds to get the fill details
            if request.order_type == OrderType.MARKET and response.get("status") == "NEW":
                logger.debug("Market order pending, polling for fill details...")
                for _ in range(3):
                    time.sleep(1)
                    updated_order = self.client.get_order_status(request.symbol, response.get("orderId"))
                    if updated_order and updated_order.get("status") == "FILLED":
                        return updated_order
            
            # 4. Process Response
            return response
            
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Order execution failed: {e}")
            raise
