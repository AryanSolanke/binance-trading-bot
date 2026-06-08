import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from .logging_config import logger
from .exceptions import APIError, ConnectionError
from .validators import OrderRequest, OrderType, OrderSide

class BinanceClient:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        try:
            self.client = Client(api_key, api_secret, testnet=testnet)
            
            # Explicitly set the base URL for Futures Testnet as per requirement
            if testnet:
                self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
                logger.info("Configured for Binance Futures Testnet: https://testnet.binancefuture.com")
            
            logger.info(f"Initialized Binance Client (Testnet={testnet})")
        except Exception as e:
            logger.error(f"Failed to initialize Binance Client: {e}")
            raise ConnectionError(f"Could not connect to Binance: {e}")

    def place_order(self, request: OrderRequest):
        """Places an order on Binance Futures Testnet."""
        try:
            logger.debug(f"Placing {request.order_type} {request.side} order for {request.symbol}")
            
            params = {
                "symbol": request.symbol,
                "side": request.side.value,
                "quantity": request.quantity,
            }

            if request.order_type == OrderType.MARKET:
                response = self.client.futures_create_order(
                    type=Client.FUTURE_ORDER_TYPE_MARKET,
                    **params
                )
            elif request.order_type == OrderType.LIMIT:
                response = self.client.futures_create_order(
                    type=Client.FUTURE_ORDER_TYPE_LIMIT,
                    timeInForce=Client.TIME_IN_FORCE_GTC,
                    price=str(request.price),
                    **params
                )
            elif request.order_type == OrderType.STOP_LIMIT:
                response = self.client.futures_create_order(
                    type=Client.FUTURE_ORDER_TYPE_STOP,
                    timeInForce=Client.TIME_IN_FORCE_GTC,
                    price=str(request.price),
                    stopPrice=str(request.stop_price),
                    **params
                )
            else:
                raise ValueError(f"Unsupported order type: {request.order_type}")

            logger.info(f"Order placed successfully: {response.get('orderId')}")
            logger.debug(f"API Response: {response}")
            return response

        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.message} (Code: {e.code})")
            raise APIError(f"Binance API Error: {e.message}")
        except Exception as e:
            logger.error(f"Unexpected error while placing order: {e}")
            raise APIError(f"An unexpected error occurred: {e}")

    def get_order_status(self, symbol: str, order_id: int):
        """Fetches the current status of an existing order."""
        try:
            return self.client.futures_get_order(symbol=symbol, orderId=order_id)
        except Exception as e:
            logger.error(f"Failed to fetch order status: {e}")
            return None
