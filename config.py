"""
Crypto Tax Economy Health Monitoring Program - Configuration

This file contains configuration settings for the crypto tax economy monitoring program.
Update these settings with your specific token and wallet information.
"""

# Token configuration
TOKENS = {
    # Format: "coingecko_id": {"name": "Display Name", "tax_rate": 0.05, "daily_roi": 0.01}
    "hex": {"name": "HEX", "tax_rate": 0.05, "daily_roi": 0.01},
    "pls": {"name": "PulseChain", "tax_rate": 0.05, "daily_roi": 0.01},
    "finvesta": {"name": "Finvesta", "tax_rate": 0.05, "daily_roi": 0.01},
    # Add other tokens here
    # "token1": {"name": "Token1", "tax_rate": 0.05, "daily_roi": 0.01},
    # "token2": {"name": "Token2", "tax_rate": 0.05, "daily_roi": 0.01},
}

# Wallet configuration
WALLETS = {
    # Format: "wallet_name": {"address": "0x...", "token": "token_id"}
    # "finvesta_treasury": {"address": "0x123...", "token": "finvesta"},
    # "finvesta_development": {"address": "0x456...", "token": "finvesta"},
    # Add other wallets here
}

# Monitoring configuration
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

# Output configuration
OUTPUT_CONFIG = {
    "save_reports": True,  # Whether to save health reports
    "report_directory": "reports",  # Directory to save reports
    "generate_plots": True,  # Whether to generate plots
    "plot_directory": "plots",  # Directory to save plots
}
