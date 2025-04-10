#!/usr/bin/env python3
"""
Crypto Tax Economy Health Monitoring Program - Main Script

This script provides a command-line interface for the crypto tax economy
health monitoring program, with specific support for Finvesta and other tokens.

Usage:
    python main.py [options]

Options:
    --token TOKEN_ID    Analyze a specific token
    --wallet WALLET     Check a specific wallet
    --output FILE       Save the health report to a file
    --plot              Generate plots for all monitored tokens
    --check-all         Run a complete health check on all tokens and wallets
    --finvesta          Run Finvesta-specific health check
    --sustainability    Check sustainability of tax models
    --config FILE       Use a custom configuration file
    --help              Show this help message
"""

import argparse
import os
import json
import sys
from datetime import datetime

# Import the monitoring classes
from crypto_monitor import CryptoMonitor
from finvesta_integration import FinvestaMonitor

# Import configuration
from config import TOKENS, WALLETS, MONITORING_CONFIG, OUTPUT_CONFIG


def setup_directories():
    """Create necessary directories for reports and plots."""
    if OUTPUT_CONFIG["save_reports"]:
        os.makedirs(OUTPUT_CONFIG["report_directory"], exist_ok=True)
    
    if OUTPUT_CONFIG["generate_plots"]:
        os.makedirs(OUTPUT_CONFIG["plot_directory"], exist_ok=True)


def configure_monitor(use_finvesta=False):
    """
    Configure the monitor with tokens and wallets from the config file.
    
    Args:
        use_finvesta: Whether to use the FinvestaMonitor (True) or CryptoMonitor (False)
        
    Returns:
        Configured monitor instance
    """
    # Create the appropriate monitor instance
    monitor = FinvestaMonitor() if use_finvesta else CryptoMonitor()
    
    # Add tokens from configuration
    for token_id, token_info in TOKENS.items():
        monitor.add_token(token_id, token_info["name"])
        
        # Set tax rate and ROI expectation if using FinvestaMonitor
        if use_finvesta:
            monitor.set_token_tax_rate(token_id, token_info["tax_rate"])
            monitor.set_token_roi_expectation(token_id, token_info["daily_roi"])
    
    # Add wallets from configuration
    for wallet_name, wallet_info in WALLETS.items():
        monitor.add_wallet(wallet_name, wallet_info["address"])
        
        # Add as project wallet if using FinvestaMonitor
        if use_finvesta and "token" in wallet_info:
            monitor.add_project_wallet(
                wallet_info["token"],
                wallet_name,
                wallet_info["address"]
            )
    
    return monitor


def save_report(report, filename=None):
    """
    Save a report to a file.
    
    Args:
        report: Report data to save
        filename: Filename to save to (optional)
    """
    if not OUTPUT_CONFIG["save_reports"]:
        return
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{OUTPUT_CONFIG['report_directory']}/health_report_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to {filename}")


def main():
    """Main function to parse arguments and run the program."""
    parser = argparse.ArgumentParser(description="Crypto Tax Economy Health Monitoring Program")
    parser.add_argument("--token", help="Analyze a specific token")
    parser.add_argument("--wallet", help="Check a specific wallet")
    parser.add_argument("--output", help="Save the health report to a file")
    parser.add_argument("--plot", action="store_true", help="Generate plots for all monitored tokens")
    parser.add_argument("--check-all", action="store_true", help="Run a complete health check on all tokens and wallets")
    parser.add_argument("--finvesta", action="store_true", help="Run Finvesta-specific health check")
    parser.add_argument("--sustainability", action="store_true", help="Check sustainability of tax models")
    parser.add_argument("--config", help="Use a custom configuration file")
    
    args = parser.parse_args()
    
    # Create necessary directories
    setup_directories()
    
    # Use custom configuration file if specified
    if args.config:
        try:
            exec(open(args.config).read())
            print(f"Using custom configuration from {args.config}")
        except Exception as e:
            print(f"Error loading custom configuration: {str(e)}")
            sys.exit(1)
    
    # Determine whether to use FinvestaMonitor
    use_finvesta = args.finvesta or "finvesta" in TOKENS
    
    # Configure the monitor
    monitor = configure_monitor(use_finvesta)
    
    # Process command-line arguments
    if args.token:
        print(f"Analyzing token: {args.token}")
        token_health = monitor.analyze_token_health(args.token)
        print(json.dumps(token_health, indent=2))
        
        if args.sustainability:
            print(f"Checking sustainability for {args.token}")
            if use_finvesta:
                sustainability = monitor.check_token_sustainability(args.token)
            else:
                # Use default values for demonstration
                sustainability = monitor.check_sustainability(
                    token_id=args.token,
                    daily_volume=1000000,  # $1M
                    tax_rate=TOKENS.get(args.token, {}).get("tax_rate", 0.05),
                    total_supply_value=10000000,  # $10M
                    daily_roi=TOKENS.get(args.token, {}).get("daily_roi", 0.01)
                )
            print(json.dumps(sustainability, indent=2))
        
        if args.plot:
            plot_path = f"{OUTPUT_CONFIG['plot_directory']}/{args.token}_analysis.png"
            monitor.plot_token_data(args.token, save_path=plot_path)
            print(f"Plot saved to {plot_path}")
        
        if args.output:
            save_report(token_health, args.output)
    
    elif args.wallet:
        print(f"Checking wallet: {args.wallet}")
        if args.wallet in WALLETS:
            wallet_address = WALLETS[args.wallet]["address"]
            wallet_activity = monitor.check_wallet_activity(wallet_name=args.wallet)
        else:
            wallet_activity = monitor.check_wallet_activity(wallet_address=args.wallet)
        
        print(json.dumps(wallet_activity, indent=2))
        
        if args.output:
            save_report(wallet_activity, args.output)
    
    elif args.finvesta:
        print("Running Finvesta-specific health check...")
        if not use_finvesta:
            print("Error: Finvesta-specific health check requires FinvestaMonitor.")
            print("Please add Finvesta to the TOKENS configuration.")
            sys.exit(1)
        
        health_report = monitor.run_finvesta_health_check()
        print(json.dumps(health_report, indent=2))
        
        if args.plot:
            for token in monitor.tokens:
                plot_path = f"{OUTPUT_CONFIG['plot_directory']}/{token}_analysis.png"
                monitor.plot_token_data(token, save_path=plot_path)
                print(f"Plot saved to {plot_path}")
        
        if args.output:
            save_report(health_report, args.output)
    
    elif args.check_all:
        print("Running complete health check on all tokens and wallets...")
        health_report = monitor.run_health_check()
        print(json.dumps(health_report, indent=2))
        
        if args.plot:
            for token in monitor.tokens:
                plot_path = f"{OUTPUT_CONFIG['plot_directory']}/{token}_analysis.png"
                monitor.plot_token_data(token, save_path=plot_path)
                print(f"Plot saved to {plot_path}")
        
        if args.output:
            save_report(health_report, args.output)
    
    else:
        # Default behavior: run a basic health check
        print("Running basic health check...")
        health_report = monitor.run_health_check()
        print(json.dumps(health_report, indent=2))
        
        if args.output:
            save_report(health_report, args.output)


if __name__ == "__main__":
    main()
