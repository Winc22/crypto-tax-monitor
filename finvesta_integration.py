"""
Finvesta and Multi-Token Integration Module

This module extends the CryptoMonitor class to add specific support for Finvesta
and other tokens in the crypto tax economy monitoring system.
"""

import pandas as pd
import requests
from datetime import datetime
import json
import os
from crypto_monitor import CryptoMonitor

class FinvestaMonitor(CryptoMonitor):
    """Extended monitor with specific support for Finvesta and other tokens."""
    
    def __init__(self):
        """Initialize the FinvestaMonitor with Finvesta-specific settings."""
        super().__init__()
        # Add Finvesta to the default tokens list
        self.tokens = ["hex", "pls", "finvesta"]  # Will be updated when we get the correct CoinGecko ID
        
        # Dictionary to store token-specific tax rates
        self.tax_rates = {
            "finvesta": 0.05,  # Default 5% tax rate, to be updated with actual value
        }
        
        # Dictionary to store token-specific ROI expectations
        self.roi_expectations = {
            "finvesta": 0.01,  # Default 1% daily ROI, to be updated with actual value
        }
        
        # Dictionary to store token-specific project wallets
        self.project_wallets = {
            "finvesta": [],  # To be populated with actual wallet addresses
        }
        
        # Additional token-specific metrics
        self.token_metrics = {}
    
    def add_project_wallet(self, token_id, wallet_name, wallet_address):
        """
        Add a project wallet for a specific token.
        
        Args:
            token_id: Token identifier (e.g., "finvesta")
            wallet_name: Name of the wallet (e.g., "Treasury")
            wallet_address: Wallet address
        """
        if token_id not in self.project_wallets:
            self.project_wallets[token_id] = []
        
        wallet_info = {
            "name": wallet_name,
            "address": wallet_address
        }
        
        self.project_wallets[token_id].append(wallet_info)
        self.add_wallet(f"{token_id}_{wallet_name}", wallet_address)
        print(f"Added {wallet_name} wallet for {token_id}: {wallet_address}")
    
    def set_token_tax_rate(self, token_id, tax_rate):
        """
        Set the tax rate for a specific token.
        
        Args:
            token_id: Token identifier
            tax_rate: Tax rate (e.g., 0.05 for 5%)
        """
        self.tax_rates[token_id] = tax_rate
        print(f"Set tax rate for {token_id} to {tax_rate*100}%")
    
    def set_token_roi_expectation(self, token_id, daily_roi):
        """
        Set the ROI expectation for a specific token.
        
        Args:
            token_id: Token identifier
            daily_roi: Daily ROI expectation (e.g., 0.01 for 1%)
        """
        self.roi_expectations[token_id] = daily_roi
        print(f"Set daily ROI expectation for {token_id} to {daily_roi*100}%")
    
    def check_token_tax_distribution(self, token_id):
        """
        Check if the token's tax distribution matches the claimed distribution.
        
        Args:
            token_id: Token identifier
            
        Returns:
            Dictionary with tax distribution analysis
        """
        if token_id not in self.project_wallets or not self.project_wallets[token_id]:
            print(f"No project wallets defined for {token_id}")
            return None
        
        tax_distribution = {}
        
        # Analyze transactions for each project wallet
        for wallet_info in self.project_wallets[token_id]:
            wallet_name = wallet_info["name"]
            wallet_address = wallet_info["address"]
            
            transactions = self.get_pulsechain_wallet(wallet_address)
            if transactions is None or len(transactions) == 0:
                print(f"No transactions found for {token_id} {wallet_name} wallet")
                continue
            
            # Analyze incoming transactions (tax collection)
            incoming_txs = transactions[transactions["to"].str.lower() == wallet_address.lower()]
            
            # Calculate daily tax collection (last 7 days)
            if len(incoming_txs) > 0:
                incoming_txs["date"] = incoming_txs["datetime"].dt.date
                daily_tax = incoming_txs.groupby("date")["value_eth"].sum()
                
                tax_distribution[wallet_name] = {
                    "total_collected": incoming_txs["value_eth"].sum(),
                    "avg_daily_collection": daily_tax.mean(),
                    "last_7_days": daily_tax.tail(7).to_dict()
                }
        
        return {
            "token": token_id,
            "tax_rate": self.tax_rates.get(token_id, 0.05),
            "distribution": tax_distribution,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def check_token_sustainability(self, token_id, estimate_supply=True):
        """
        Check if the token's tax model is sustainable based on actual data.
        
        Args:
            token_id: Token identifier
            estimate_supply: Whether to estimate total supply value from market cap
            
        Returns:
            Dictionary with sustainability metrics
        """
        # Get token data
        token_data = self.get_token_data(token_id)
        if token_data is None or len(token_data) == 0:
            print(f"No data available for {token_id}")
            return None
        
        # Get the latest price and volume
        current_price = token_data["price"].iloc[-1]
        current_volume = token_data["volume"].iloc[-1]
        
        # Get the average daily volume (30 days)
        avg_daily_volume = token_data["volume"].mean()
        
        # Get the tax rate for this token
        tax_rate = self.tax_rates.get(token_id, 0.05)
        
        # Get the ROI expectation for this token
        daily_roi = self.roi_expectations.get(token_id, 0.01)
        
        # Estimate total supply value if requested
        total_supply_value = None
        if estimate_supply:
            # This is a rough estimation; ideally, we would get the actual market cap
            # For now, we'll use a placeholder value of 10x the daily volume
            total_supply_value = avg_daily_volume * 10
        else:
            # Use a default value for now
            total_supply_value = 10000000  # $10M
        
        # Check sustainability
        return self.check_sustainability(
            token_id=token_id,
            daily_volume=avg_daily_volume,
            tax_rate=tax_rate,
            total_supply_value=total_supply_value,
            daily_roi=daily_roi
        )
    
    def analyze_multi_token_ecosystem(self, token_ids=None):
        """
        Analyze the health of multiple tokens in an ecosystem.
        
        Args:
            token_ids: List of token IDs to analyze (default: self.tokens)
            
        Returns:
            Dictionary with ecosystem health metrics
        """
        if token_ids is None:
            token_ids = self.tokens
        
        ecosystem_health = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tokens": {},
            "ecosystem_metrics": {
                "total_volume": 0,
                "avg_price_change": 0,
                "sustainability_score": 0
            }
        }
        
        total_volume = 0
        price_changes = []
        sustainability_scores = []
        
        # Analyze each token
        for token_id in token_ids:
            print(f"Analyzing {token_id}...")
            
            # Get token health
            token_health = self.analyze_token_health(token_id)
            if token_health:
                ecosystem_health["tokens"][token_id] = token_health
                total_volume += token_health["current_volume"]
                price_changes.append(token_health["price_change_30d"])
            
            # Check sustainability
            sustainability = self.check_token_sustainability(token_id)
            if sustainability and sustainability["sustainability_ratio"] > 0:
                sustainability_scores.append(sustainability["sustainability_ratio"])
        
        # Calculate ecosystem metrics
        ecosystem_health["ecosystem_metrics"]["total_volume"] = total_volume
        ecosystem_health["ecosystem_metrics"]["avg_price_change"] = sum(price_changes) / len(price_changes) if price_changes else 0
        ecosystem_health["ecosystem_metrics"]["sustainability_score"] = sum(sustainability_scores) / len(sustainability_scores) if sustainability_scores else 0
        
        # Overall ecosystem health assessment
        if ecosystem_health["ecosystem_metrics"]["sustainability_score"] < 1:
            ecosystem_health["ecosystem_metrics"]["health_status"] = "Critical: Unsustainable"
        elif ecosystem_health["ecosystem_metrics"]["sustainability_score"] < 1.5:
            ecosystem_health["ecosystem_metrics"]["health_status"] = "Warning: Marginally Sustainable"
        else:
            ecosystem_health["ecosystem_metrics"]["health_status"] = "Healthy: Sustainable"
        
        return ecosystem_health
    
    def run_finvesta_health_check(self, output_file=None):
        """
        Run a complete health check focused on Finvesta and related tokens.
        
        Args:
            output_file: Path to save the health report (optional)
            
        Returns:
            Dictionary with complete health report
        """
        print("Running Finvesta ecosystem health check...")
        
        # Run the standard health check
        health_report = self.run_health_check()
        
        # Add Finvesta-specific checks
        health_report["finvesta_specific"] = {}
        
        # Check tax distribution for Finvesta
        if "finvesta" in self.tokens:
            tax_distribution = self.check_token_tax_distribution("finvesta")
            if tax_distribution:
                health_report["finvesta_specific"]["tax_distribution"] = tax_distribution
        
        # Analyze the entire ecosystem
        ecosystem_health = self.analyze_multi_token_ecosystem()
        health_report["ecosystem"] = ecosystem_health
        
        # Save report if requested
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(health_report, f, indent=2)
            print(f"Finvesta health report saved to {output_file}")
        
        return health_report


# Example usage (to be updated with actual values)
if __name__ == "__main__":
    monitor = FinvestaMonitor()
    
    # Add tokens to monitor
    # These will be updated with actual CoinGecko IDs
    monitor.add_token("hex", "HEX")
    monitor.add_token("pls", "PulseChain")
    monitor.add_token("finvesta", "Finvesta")
    # Add other tokens in the ecosystem
    # monitor.add_token("token1", "Token1")
    # monitor.add_token("token2", "Token2")
    
    # Set tax rates
    monitor.set_token_tax_rate("finvesta", 0.05)  # 5% tax
    
    # Set ROI expectations
    monitor.set_token_roi_expectation("finvesta", 0.01)  # 1% daily ROI
    
    # Add project wallets
    # monitor.add_project_wallet("finvesta", "Treasury", "0x123...")
    # monitor.add_project_wallet("finvesta", "Development", "0x456...")
    
    # Run Finvesta-specific health check
    health_report = monitor.run_finvesta_health_check(output_file="finvesta_health_report.json")
    
    # Generate plots for all tokens
    for token in monitor.tokens:
        monitor.plot_token_data(token, save_path=f"{token}_analysis.png")
