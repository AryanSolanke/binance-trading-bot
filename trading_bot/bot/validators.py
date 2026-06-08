from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator

class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP_LIMIT = "STOP_LIMIT"

class OrderRequest(BaseModel):
    symbol: str = Field(..., description="Trading pair, e.g., BTCUSDT")
    side: OrderSide
    order_type: OrderType
    quantity: float = Field(..., gt=0, description="Quantity to buy or sell")
    price: Optional[float] = Field(None, gt=0, description="Price for LIMIT and STOP_LIMIT orders")
    stop_price: Optional[float] = Field(None, gt=0, description="Stop price for STOP_LIMIT orders")

    @field_validator('symbol')
    @classmethod
    def validate_symbol(cls, v: str) -> str:
        return v.upper()

    @model_validator(mode='after')
    def check_required_fields(self) -> 'OrderRequest':
        if self.order_type in [OrderType.LIMIT, OrderType.STOP_LIMIT] and self.price is None:
            raise ValueError(f"Price is required for {self.order_type.value} orders.")
        
        if self.order_type == OrderType.STOP_LIMIT and self.stop_price is None:
            raise ValueError("Stop price is required for STOP_LIMIT orders.")
            
        return self
