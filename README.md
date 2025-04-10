# Crypto Tax Economy Health Monitoring Program

A comprehensive tool for monitoring the health of crypto tax economies, with specific support for Finvesta and other tokens in the PulseChain ecosystem.

## Overview

This program helps you monitor and analyze the health of crypto tax economies by tracking:

- Token prices and trading volumes
- Wallet activities and large transactions
- Tax distribution and collection
- Sustainability of tax models and ROI expectations
- Overall ecosystem health metrics

The system is designed to provide alerts for potential issues such as volume drops, large wallet outflows, and unsustainable ROI models.

## Features

- **PulseChain Wallet Tracking**: Monitor wallet activities on the PulseChain network
- **Price & Volume Analysis**: Track token prices and trading volumes via CoinGecko
- **Tax Distribution Verification**: Compare claimed tax distribution with actual on-chain transfers
- **Sustainability Checks**: Verify if tax models can sustain promised ROI
- **Multi-Token Ecosystem Analysis**: Analyze the health of an entire ecosystem of related tokens
- **Data Visualization**: Generate plots of price and volume trends
- **Automated Alerts**: Get notified of potential issues like volume drops or large transactions

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install pandas requests matplotlib python-dotenv
```

## Configuration

Edit the `config.py` file to customize the monitoring settings:

```python
# Token configuration
TOKENS = {
    "hex": {"name": "HEX", "tax_rate": 0.05, "daily_roi": 0.01},
    "pls": {"name": "PulseChain", "tax_rate": 0.05, "daily_roi": 0.01},
    "finvesta": {"name": "Finvesta", "tax_rate": 0.05, "daily_roi": 0.01},
    # Add other tokens here
}

# Wallet configuration
WALLETS = {
    "finvesta_treasury": {"address": "0x123...", "token": "finvesta"},
    # Add other wallets here
}
```

## Usage

### Basic Usage

Run the main script to perform a health check on all configured tokens and wallets:

```bash
python main.py
```

### Specific Token Analysis

To analyze a specific token:

```bash
python main.py --token finvesta
```

### Scheduled Monitoring

Set up a cron job to run the script at regular intervals:

```bash
# Run every hour
0 * * * * cd /path/to/crypto_tax_monitor && python main.py --output reports/hourly_report.json
```

## Example Code

### Monitoring a Single Token

```python
from crypto_monitor import CryptoMonitor

# Create a monitor instance
monitor = CryptoMonitor()

# Add a token to monitor
monitor.add_token("hex", "HEX")

# Analyze token health
health_report = monitor.analyze_token_health("hex")
print(health_report)

# Generate a price and volume plot
monitor.plot_token_data("hex", save_path="hex_analysis.png")
```

### Checking Wallet Activity

```python
from crypto_monitor import CryptoMonitor

# Create a monitor instance
monitor = CryptoMonitor()

# Add a wallet to monitor
monitor.add_wallet("Treasury", "0x123...")

# Check wallet activity
wallet_activity = monitor.check_wallet_activity("Treasury")
print(wallet_activity)
```

### Sustainability Check

```python
from crypto_monitor import CryptoMonitor

# Create a monitor instance
monitor = CryptoMonitor()

# Check if the token's tax model is sustainable
sustainability = monitor.check_sustainability(
    token_id="finvesta",
    daily_volume=1000000,  # $1M
    tax_rate=0.05,  # 5%
    total_supply_value=10000000,  # $10M
    daily_roi=0.01  # 1%
)
print(sustainability)
```

### Finvesta-Specific Monitoring

```python
from finvesta_integration import FinvestaMonitor

# Create a Finvesta monitor instance
monitor = FinvestaMonitor()

# Add Finvesta and related tokens
monitor.add_token("finvesta", "Finvesta")
monitor.add_token("token1", "Token1")
monitor.add_token("token2", "Token2")

# Set tax rates and ROI expectations
monitor.set_token_tax_rate("finvesta", 0.05)  # 5% tax
monitor.set_token_roi_expectation("finvesta", 0.01)  # 1% daily ROI

# Add project wallets
monitor.add_project_wallet("finvesta", "Treasury", "0x123...")
monitor.add_project_wallet("finvesta", "Development", "0x456...")

# Run a complete health check
health_report = monitor.run_finvesta_health_check(output_file="finvesta_health_report.json")
```

## Output Examples

### Token Health Report

```json
{
  "token": "finvesta",
  "current_price": 0.0123,
  "price_change_30d": -5.2,
  "price_volatility": 12.3,
  "current_volume": 250000,
  "volume_change_30d": -15.7,
  "volume_health": "Normal",
  "timestamp": "2025-04-10 04:25:00"
}
```

### Sustainability Report

```json
{
  "token": "finvesta",
  "daily_volume": 1000000,
  "tax_rate": 0.05,
  "daily_tax_revenue": 50000,
  "total_supply_value": 10000000,
  "daily_roi": 0.01,
  "required_payouts": 100000,
  "is_sustainable": false,
  "sustainability_ratio": 0.5,
  "timestamp": "2025-04-10 04:25:00"
}
```

## Troubleshooting

### CoinGecko API Errors

- Ensure token IDs are correct (e.g., "hex" for HEX, "pls" for PulseChain)
- CoinGecko has rate limits; add delays between requests if needed

### PulseChain Explorer Issues

- If the API is unstable, manually track wallets through the explorer
- Verify wallet addresses are correct and in the proper format

### Script Not Running

- Ensure all dependencies are installed: `pip install --upgrade requests pandas matplotlib python-dotenv`
- Check Python version: `python --version` (should be 3.6+)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
