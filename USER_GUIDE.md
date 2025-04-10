#!/usr/bin/env python3
"""
Crypto Tax Economy Health Monitoring Program - User Guide

This document provides detailed instructions on how to use the crypto tax economy
health monitoring program, with specific focus on monitoring Finvesta and other tokens.
"""

# Table of Contents
# -----------------
# 1. Introduction
# 2. Installation
# 3. Configuration
#    3.1 Token Configuration
#    3.2 Wallet Configuration
#    3.3 Monitoring Settings
#    3.4 Output Settings
# 4. Basic Usage
#    4.1 Command-Line Interface
#    4.2 Running Health Checks
#    4.3 Analyzing Specific Tokens
#    4.4 Monitoring Wallets
# 5. Advanced Features
#    5.1 Sustainability Checks
#    5.2 Tax Distribution Verification
#    5.3 Ecosystem Analysis
# 6. Interpreting Results
#    6.1 Health Reports
#    6.2 Sustainability Reports
#    6.3 Alert Indicators
# 7. Automation
#    7.1 Scheduled Monitoring
#    7.2 Integration with Other Systems
# 8. Troubleshooting
# 9. FAQ

# 1. Introduction
# ---------------

"""
The Crypto Tax Economy Health Monitoring Program is a comprehensive tool designed to help you
monitor and analyze the health of crypto tax economies, with specific support for Finvesta
and other tokens in the PulseChain ecosystem.

This program helps you track token prices, trading volumes, wallet activities, tax distribution,
and sustainability metrics to ensure the long-term health of crypto tax economies.
"""

# 2. Installation
# --------------

"""
To install the program, follow these steps:

1. Ensure you have Python 3.6 or higher installed:
   $ python --version

2. Clone or download the repository:
   $ git clone https://github.com/yourusername/crypto-tax-monitor.git
   $ cd crypto-tax-monitor

3. Install the required dependencies:
   $ pip install pandas requests matplotlib python-dotenv

4. Verify the installation:
   $ python main.py --help
"""

# 3. Configuration
# ---------------

"""
Before using the program, you need to configure it with your specific tokens and wallets.
All configuration is done in the `config.py` file.

3.1 Token Configuration

The TOKENS dictionary contains information about each token you want to monitor:

```python
TOKENS = {
    "hex": {"name": "HEX", "tax_rate": 0.05, "daily_roi": 0.01},
    "pls": {"name": "PulseChain", "tax_rate": 0.05, "daily_roi": 0.01},
    "finvesta": {"name": "Finvesta", "tax_rate": 0.05, "daily_roi": 0.01},
    # Add other tokens here
}
```

For each token, you need to specify:
- The CoinGecko token ID (e.g., "hex" for HEX)
- A display name
- The tax rate (e.g., 0.05 for 5%)
- The daily ROI expectation (e.g., 0.01 for 1%)

3.2 Wallet Configuration

The WALLETS dictionary contains information about wallets you want to monitor:

```python
WALLETS = {
    "finvesta_treasury": {"address": "0x123...", "token": "finvesta"},
    "finvesta_development": {"address": "0x456...", "token": "finvesta"},
    # Add other wallets here
}
```

For each wallet, you need to specify:
- A wallet name
- The wallet address
- The associated token (optional, used for token-specific analysis)

3.3 Monitoring Settings

The MONITORING_CONFIG dictionary contains settings for the monitoring process:

```python
MONITORING_CONFIG = {
    "check_interval_minutes": 60,  # How often to run health checks
    "alert_thresholds": {
        "volume_drop_percent": 50,  # Alert if volume drops by this percentage
        "large_transaction_eth": 0.05,  # Alert for transactions larger than this amount
        "sustainability_ratio_warning": 1.5,  # Warning level for sustainability ratio
        "sustainability_ratio_critical": 1.0,  # Critical level for sustainability ratio
    },
    "history_days": 30,  # Number of days of historical data to fetch
}
```

3.4 Output Settings

The OUTPUT_CONFIG dictionary contains settings for reports and plots:

```python
OUTPUT_CONFIG = {
    "save_reports": True,  # Whether to save health reports
    "report_directory": "reports",  # Directory to save reports
    "generate_plots": True,  # Whether to generate plots
    "plot_directory": "plots",  # Directory to save plots
}
```
"""

# 4. Basic Usage
# -------------

"""
4.1 Command-Line Interface

The program provides a command-line interface through the `main.py` script:

```
python main.py [options]
```

Available options:
- `--token TOKEN_ID`: Analyze a specific token
- `--wallet WALLET`: Check a specific wallet
- `--output FILE`: Save the health report to a file
- `--plot`: Generate plots for all monitored tokens
- `--check-all`: Run a complete health check on all tokens and wallets
- `--finvesta`: Run Finvesta-specific health check
- `--sustainability`: Check sustainability of tax models
- `--config FILE`: Use a custom configuration file
- `--help`: Show help message

4.2 Running Health Checks

To run a basic health check on all configured tokens and wallets:

```
python main.py
```

To run a complete health check and save the report:

```
python main.py --check-all --output health_report.json
```

4.3 Analyzing Specific Tokens

To analyze a specific token:

```
python main.py --token finvesta
```

To analyze a token and check its sustainability:

```
python main.py --token finvesta --sustainability
```

To analyze a token and generate a plot:

```
python main.py --token finvesta --plot
```

4.4 Monitoring Wallets

To check a specific wallet:

```
python main.py --wallet finvesta_treasury
```

You can also check a wallet by address:

```
python main.py --wallet 0x123...
```
"""

# 5. Advanced Features
# ------------------

"""
5.1 Sustainability Checks

The program can check if a token's tax model is sustainable based on its trading volume,
tax rate, and ROI expectations:

```
python main.py --token finvesta --sustainability
```

This will analyze whether the tax revenue generated from trading volume is sufficient
to sustain the promised ROI for token holders.

5.2 Tax Distribution Verification

For Finvesta and other tokens with tax distribution, the program can verify if the
actual on-chain tax distribution matches the claimed distribution:

```
python main.py --finvesta
```

This will analyze the transactions of project wallets to verify tax collection and distribution.

5.3 Ecosystem Analysis

For tokens that are part of a larger ecosystem (like Finvesta), the program can analyze
the health of the entire ecosystem:

```
python main.py --finvesta
```

This will analyze the health of all tokens in the ecosystem and provide an overall
ecosystem health assessment.
"""

# 6. Interpreting Results
# ---------------------

"""
6.1 Health Reports

Health reports contain information about token prices, trading volumes, and other metrics:

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

Key metrics to watch:
- `price_change_30d`: Price change over the last 30 days (%)
- `price_volatility`: Price volatility (%)
- `volume_change_30d`: Volume change over the last 30 days (%)
- `volume_health`: Assessment of volume health (Normal, Warning, etc.)

6.2 Sustainability Reports

Sustainability reports assess whether a token's tax model can sustain its promised ROI:

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

Key metrics to watch:
- `daily_tax_revenue`: Estimated daily tax revenue ($)
- `required_payouts`: Required payouts to sustain the promised ROI ($)
- `is_sustainable`: Whether the tax model is sustainable (true/false)
- `sustainability_ratio`: Ratio of tax revenue to required payouts (>1 is sustainable)

6.3 Alert Indicators

The program uses the following alert indicators:

- `⚠️ Volume drop`: Indicates a significant drop in trading volume
- `🚨 Large transaction`: Indicates a large wallet transaction
- `⚠️ Unsustainable ROI`: Indicates that the tax model cannot sustain the promised ROI
"""

# 7. Automation
# -----------

"""
7.1 Scheduled Monitoring

To run the program automatically at regular intervals, you can set up a cron job:

```
# Run every hour
0 * * * * cd /path/to/crypto_tax_monitor && python main.py --output reports/hourly_report.json
```

7.2 Integration with Other Systems

The program can be integrated with other systems by:

- Saving reports to JSON files that can be read by other systems
- Modifying the code to send alerts via email, Telegram, or other channels
- Using the program as a library in other Python applications
"""

# 8. Troubleshooting
# ----------------

"""
Common issues and solutions:

1. CoinGecko API Errors:
   - Ensure token IDs are correct (e.g., "hex" for HEX, "pls" for PulseChain)
   - CoinGecko has rate limits; add delays between requests if needed

2. PulseChain Explorer Issues:
   - If the API is unstable, manually track wallets through the explorer
   - Verify wallet addresses are correct and in the proper format

3. Script Not Running:
   - Ensure all dependencies are installed: `pip install --upgrade requests pandas matplotlib python-dotenv`
   - Check Python version: `python --version` (should be 3.6+)

4. No Data Available:
   - Ensure the token is listed on CoinGecko
   - Check if the wallet has transactions on PulseChain
"""

# 9. FAQ
# -----

"""
Q: How accurate is the sustainability check?
A: The sustainability check is based on estimated trading volume and tax revenue. It provides
   a general assessment but may not account for all factors affecting a token's sustainability.

Q: Can I monitor tokens on other blockchains?
A: The current version is focused on PulseChain, but you can modify the code to support other
   blockchains by implementing appropriate API calls.

Q: How often should I run health checks?
A: For active monitoring, running health checks hourly is recommended. For less active tokens,
   daily checks may be sufficient.

Q: What should I do if I see a warning or alert?
A: Investigate the issue further by checking the token's social media, official announcements,
   and on-chain activity. Alerts are indicators of potential issues, not definitive problems.
"""
