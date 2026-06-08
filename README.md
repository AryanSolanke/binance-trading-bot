# Binance Futures Testnet Trading Bot

A robust, professional-grade Python trading bot for the Binance Futures Testnet (USDT-M). Built with a focus on modularity, strict validation, and a clean command-line interface.

## Features

- **Order Types**: Support for MARKET, LIMIT, and STOP_LIMIT orders.
- **Strict Validation**: Powered by Pydantic to ensure data integrity before API calls.
- **Enhanced CLI**: A clean terminal interface using Typer and Rich.
- **Structured Logging**: Detailed logs for all API interactions, requests, and errors.
- **Clean Architecture**: Decoupled layers for CLI, business logic, and API interaction.

## Tech Stack

- **Python 3.x**
- **python-binance**: Binance API wrapper.
- **Typer**: CLI framework.
- **Rich**: Terminal formatting.
- **Pydantic**: Data validation and settings management.
- **python-dotenv**: Environment variable management.

## Getting Started

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Trading_bot
```

### 2. Set Up Environment
Create a .env file in the root directory and add your Binance Testnet API credentials:
```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
BINANCE_USE_TESTNET=True
```

### 3. Install Dependencies
It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage Examples

The bot is accessible via the cli.py script.

### Help Menu
```bash
python cli.py --help
```

### Place a MARKET Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a LIMIT Order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 65000
```

### Place a STOP_LIMIT Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP_LIMIT --quantity 0.001 --price 68000 --stop-price 67500
```

## Project Structure

```text
.
├── cli.py               # Main entry point (Typer CLI)
├── trading_bot/
│   ├── bot/
│   │   ├── client.py        # Binance API wrapper & authentication
│   │   ├── orders.py        # Business logic & orchestration
│   │   ├── validators.py    # Pydantic models for strict validation
│   │   ├── exceptions.py    # Custom exception classes
│   │   └── logging_config.py # Centralized logging setup
├── tests/               # Unit test suite
├── trading_bot.log      # Detailed log file
├── README.md            # Documentation
└── requirements.txt     # Dependency list
```

## Assumptions and Notes

1. **Testnet Only**: By default, BINANCE_USE_TESTNET is set to True.
2. **USDT-M Futures**: The bot specifically targets Binance USDT-Margined Futures.
3. **Explicit URL**: The bot is configured to use https://testnet.binancefuture.com as requested.
4. **Time in Force**: LIMIT and STOP_LIMIT orders use GTC (Good 'Til Cancelled) by default.

## Safety and Security

- Never commit your .env file.
- This bot is for educational purposes on the Testnet. Use at your own risk.
