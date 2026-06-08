import os
import typer
from typing import Optional
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from trading_bot.bot.client import BinanceClient
from trading_bot.bot.orders import OrderManager
from trading_bot.bot.logging_config import logger
from trading_bot.bot.exceptions import TradingBotError

# Load environment variables
load_dotenv()

app = typer.Typer(help="Binance Futures Testnet Trading Bot")
console = Console()

def get_client():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    use_testnet = os.getenv("BINANCE_USE_TESTNET", "True").lower() == "true"

    if not api_key or not api_secret:
        console.print("[bold red]Error:[/bold red] BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env file.")
        raise typer.Exit(code=1)

    return BinanceClient(api_key, api_secret, testnet=use_testnet)

@app.command()
def place(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair (e.g., BTCUSDT)"),
    side: str = typer.Option(..., "--side", "-d", help="Order side (BUY/SELL)"),
    order_type: str = typer.Option(..., "--type", "-t", help="Order type (MARKET/LIMIT/STOP_LIMIT)"),
    quantity: float = typer.Option(..., "--quantity", "-q", help="Quantity to trade"),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Price (required for LIMIT/STOP_LIMIT)"),
    stop_price: Optional[float] = typer.Option(None, "--stop-price", "-sp", help="Stop Price (required for STOP_LIMIT)")
):
    """
    Place an order on Binance Futures Testnet.
    """
    try:
        client = get_client()
        manager = OrderManager(client)

        console.print(Panel(f"[bold cyan]Requesting {order_type} {side} for {symbol}[/bold cyan]"))
        
        with console.status("[bold green]Placing order...") as status:
            response = manager.execute_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
                stop_price=stop_price
            )

        # Print success table
        table = Table(title="Order Confirmation", show_header=True, header_style="bold magenta")
        table.add_column("Field", style="dim")
        table.add_column("Value")

        table.add_row("Order ID", str(response.get("orderId")))
        table.add_row("Symbol", response.get("symbol"))
        table.add_row("Status", f"[bold green]{response.get('status')}[/bold green]")
        table.add_row("Executed Qty", str(response.get("executedQty")))
        table.add_row("Avg Price", str(response.get("avgPrice", "N/A")))
        table.add_row("Type", response.get("type"))
        table.add_row("Side", response.get("side"))

        console.print(table)
        console.print("[bold green]SUCCESS: Order placed successfully.[/bold green]")

    except TradingBotError as e:
        console.print(f"[bold red]API Error:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/bold red] {e}")

if __name__ == "__main__":
    app()
