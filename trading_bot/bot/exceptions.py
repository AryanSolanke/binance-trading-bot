class TradingBotError(Exception):
    """Base exception for the trading bot."""
    pass

class APIError(TradingBotError):
    """Raised when the Binance API returns an error."""
    pass

class ValidationError(TradingBotError):
    """Raised when input validation fails."""
    pass

class ConnectionError(TradingBotError):
    """Raised when there is a network issue."""
    pass
