"""
Crypto Tax Economy Health Monitoring Program

This program monitors the health of crypto tax economies including Finvesta and other tokens.
It tracks wallet activities, price movements, trading volumes, and performs sustainability checks.
"""

import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import os
from dotenv import load_dotenv
import time
import json

# Load environment variables
load_dotenv()

class CryptoMonitor:
    def __init__(self):
        """Initialize the CryptoMonitor with default settings."""
        self.tokens = ["hex", "pls"]  # Default tokens to monitor
        self.wallets = {}  # Dictionary to store wallet addresses
        self.data_cache = {}  # Cache for API responses
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
        self.pulsechain_base_url = "https://scan.pulsechain.com/api"
        
    def add_token(self, token_id, token_name=None):
        """Add a token to the monitoring list."""
        if token_id not in self.tokens:
            self.tokens.append(token_id)
            print(f"Added {token_name or token_id} to monitoring list.")
    
    def add_wallet(self, name, address):
        """Add a wallet address to monitor."""
        self.wallets[name] = address
        print(f"Added wallet '{name}' with address {address} to monitoring list.")
    
    def get_token_data(self, token_id, days=30, vs_currency="usd"):
        """
        Fetch price and volume data for a token from CoinGecko.
        
        Args:
            token_id: CoinGecko token ID (e.g., "hex" for HEX)
            days: Number of days of historical data to fetch
            vs_currency: Currency to compare against (default: USD)
            
        Returns:
            DataFrame with timestamp, price, and volume data
        """
        cache_key = f"{token_id}_{days}_{vs_currency}"
        if cache_key in self.data_cache:
            return self.data_cache[cache_key]
            
        url = f"{self.coingecko_base_url}/coins/{token_id}/market_chart?vs_currency={vs_currency}&days={days}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
                volumes = pd.DataFrame(data["total_volumes"], columns=["timestamp", "volume"])
                
                # Convert timestamp from milliseconds to datetime
                prices["date"] = pd.to_datetime(prices["timestamp"], unit="ms")
                volumes["date"] = pd.to_datetime(volumes["timestamp"], unit="ms")
                
                # Merge price and volume data
                result = prices.merge(volumes, on=["timestamp", "date"])
                
                # Cache the result
                self.data_cache[cache_key] = result
                return result
            else:
                print(f"Error fetching data for {token_id}: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception when fetching data for {token_id}: {str(e)}")
            return None
    
    def get_pulsechain_wallet(self, wallet_address):
        """
        Fetch transaction data for a wallet on PulseChain.
        
        Args:
            wallet_address: The wallet address to check
            
        Returns:
            DataFrame with transaction data
        """
        url = f"{self.pulsechain_base_url}?module=account&action=txlist&address={wallet_address}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "1":
                    transactions = pd.DataFrame(data["result"])
                    # Convert timestamp to datetime
                    transactions["datetime"] = pd.to_datetime(transactions["timeStamp"], unit="s")
                    # Convert value from wei to ETH/PLS
                    transactions["value_eth"] = transactions["value"].astype(float) / 1e18
                    return transactions[["hash", "value", "value_eth", "from", "to", "timeStamp", "datetime"]]
                else:
                    print(f"Error fetching wallet data: {data.get('message', 'Unknown error')}")
                    return None
            else:
                print(f"Error fetching wallet data: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception when fetching wallet data: {str(e)}")
            return None
    
    def check_wallet_activity(self, wallet_name=None, wallet_address=None, threshold=0.05):
        """
        Check wallet activity and alert for large transactions.
        
        Args:
            wallet_name: Name of the wallet (if in self.wallets)
            wallet_address: Direct wallet address (alternative to wallet_name)
            threshold: Threshold for large transaction alerts (in ETH/PLS)
            
        Returns:
            Dictionary with wallet activity summary
        """
        if wallet_name and wallet_name in self.wallets:
            wallet_address = self.wallets[wallet_name]
        
        if not wallet_address:
            print("No wallet address provided.")
            return None
            
        transactions = self.get_pulsechain_wallet(wallet_address)
        if transactions is None or len(transactions) == 0:
            print(f"No transactions found for wallet {wallet_name or wallet_address}")
            return None
            
        # Get the latest transaction
        latest_tx = transactions.iloc[0]  # Assuming transactions are sorted by timestamp (newest first)
        
        # Calculate statistics
        total_txs = len(transactions)
        incoming_txs = transactions[transactions["to"].str.lower() == wallet_address.lower()]
        outgoing_txs = transactions[transactions["from"].str.lower() == wallet_address.lower()]
        
        # Check for large transactions
        large_txs = transactions[abs(transactions["value_eth"]) > threshold]
        
        # Prepare summary
        summary = {
            "wallet": wallet_name or wallet_address,
            "total_transactions": total_txs,
            "incoming_transactions": len(incoming_txs),
            "outgoing_transactions": len(outgoing_txs),
            "large_transactions": len(large_txs),
            "latest_transaction": {
                "hash": latest_tx["hash"],
                "value": latest_tx["value_eth"],
                "from": latest_tx["from"],
                "to": latest_tx["to"],
                "timestamp": latest_tx["datetime"].strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        
        # Alert for large outflows
        if len(large_txs) > 0:
            print(f"🚨 Found {len(large_txs)} large transactions for {wallet_name or wallet_address}")
            for _, tx in large_txs.iterrows():
                direction = "outgoing" if tx["from"].lower() == wallet_address.lower() else "incoming"
                print(f"  - {direction.upper()}: {abs(tx['value_eth'])} ETH/PLS on {tx['datetime'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        return summary
    
    def analyze_token_health(self, token_id):
        """
        Analyze the health of a token based on price and volume trends.
        
        Args:
            token_id: CoinGecko token ID
            
        Returns:
            Dictionary with token health metrics
        """
        data = self.get_token_data(token_id)
        if data is None or len(data) == 0:
            print(f"No data available for {token_id}")
            return None
            
        # Calculate metrics
        current_price = data["price"].iloc[-1]
        avg_price = data["price"].mean()
        price_change = (current_price - data["price"].iloc[0]) / data["price"].iloc[0] * 100
        
        current_volume = data["volume"].iloc[-1]
        avg_volume = data["volume"].mean()
        volume_change = (current_volume - data["volume"].iloc[0]) / data["volume"].iloc[0] * 100
        
        # Volume health check
        volume_health = "Normal"
        if current_volume < avg_volume * 0.5:
            volume_health = "Warning: Volume drop"
        elif current_volume > avg_volume * 2:
            volume_health = "High volume activity"
            
        # Price volatility
        price_volatility = data["price"].std() / avg_price * 100
        
        # Prepare health report
        health_report = {
            "token": token_id,
            "current_price": current_price,
            "price_change_30d": price_change,
            "price_volatility": price_volatility,
            "current_volume": current_volume,
            "volume_change_30d": volume_change,
            "volume_health": volume_health,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Print alerts
        if volume_health != "Normal":
            print(f"⚠️ {volume_health} for {token_id}: ${current_volume:.2f} (Avg: ${avg_volume:.2f})")
        
        return health_report
    
    def plot_token_data(self, token_id, save_path=None):
        """
        Create and save a plot of token price and volume.
        
        Args:
            token_id: CoinGecko token ID
            save_path: Path to save the plot image (optional)
            
        Returns:
            Path to saved image if save_path is provided
        """
        data = self.get_token_data(token_id)
        if data is None or len(data) == 0:
            print(f"No data available for {token_id}")
            return None
            
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        
        # Plot price
        ax1.plot(data["date"], data["price"], 'b-')
        ax1.set_title(f"{token_id.upper()} Price (USD)")
        ax1.set_ylabel("Price (USD)")
        ax1.grid(True)
        
        # Plot volume
        ax2.bar(data["date"], data["volume"], color='g', alpha=0.6)
        ax2.set_title(f"{token_id.upper()} Trading Volume (USD)")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Volume (USD)")
        ax2.grid(True)
        
        # Format the plot
        plt.tight_layout()
        
        # Save or show the plot
        if save_path:
            plt.savefig(save_path)
            plt.close()
            return save_path
        else:
            plt.show()
            plt.close()
            return None
    
    def check_sustainability(self, token_id, daily_volume, tax_rate, total_supply_value, daily_roi):
        """
        Check if the token's tax model is sustainable.
        
        Args:
            token_id: Token identifier
            daily_volume: Estimated daily trading volume
            tax_rate: Tax rate (e.g., 0.05 for 5%)
            total_supply_value: Total value of token supply
            daily_roi: Daily ROI promised/expected (e.g., 0.01 for 1%)
            
        Returns:
            Dictionary with sustainability metrics
        """
        daily_tax_revenue = daily_volume * tax_rate
        required_payouts = total_supply_value * daily_roi
        
        is_sustainable = daily_tax_revenue >= required_payouts
        sustainability_ratio = daily_tax_revenue / required_payouts if required_payouts > 0 else float('inf')
        
        sustainability_report = {
            "token": token_id,
            "daily_volume": daily_volume,
            "tax_rate": tax_rate,
            "daily_tax_revenue": daily_tax_revenue,
            "total_supply_value": total_supply_value,
            "daily_roi": daily_roi,
            "required_payouts": required_payouts,
            "is_sustainable": is_sustainable,
            "sustainability_ratio": sustainability_ratio,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if not is_sustainable:
            print(f"⚠️ Unsustainable ROI for {token_id}!")
            print(f"  - Daily tax revenue: ${daily_tax_revenue:.2f}")
            print(f"  - Required for {daily_roi*100}% daily ROI: ${required_payouts:.2f}")
            print(f"  - Sustainability ratio: {sustainability_ratio:.2f}")
        
        return sustainability_report
    
    def run_health_check(self, output_file=None):
        """
        Run a complete health check on all monitored tokens and wallets.
        
        Args:
            output_file: Path to save the health report (optional)
            
        Returns:
            Dictionary with complete health report
        """
        health_report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tokens": {},
            "wallets": {}
        }
        
        print(f"Running health check at {health_report['timestamp']}...")
        
        # Check tokens
        for token in self.tokens:
            print(f"Analyzing {token}...")
            token_health = self.analyze_token_health(token)
            if token_health:
                health_report["tokens"][token] = token_health
        
        # Check wallets
        for name, address in self.wallets.items():
            print(f"Checking wallet {name}...")
            wallet_activity = self.check_wallet_activity(wallet_name=name)
            if wallet_activity:
                health_report["wallets"][name] = wallet_activity
        
        # Save report if requested
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(health_report, f, indent=2)
            print(f"Health report saved to {output_file}")
        
        return health_report


# Example usage
if __name__ == "__main__":
    monitor = CryptoMonitor()
    
    # Add tokens to monitor (including Finvesta if available on CoinGecko)
    monitor.add_token("hex", "HEX")
    monitor.add_token("pulsechain", "PulseChain")
    # Add Finvesta and other tokens here
    # monitor.add_token("finvesta", "Finvesta")
    
    # Add project wallets to monitor
    # monitor.add_wallet("Project Treasury", "0x123...")
    # monitor.add_wallet("Dev Wallet", "0x456...")
    
    # Run health check
    health_report = monitor.run_health_check(output_file="health_report.json")
    
    # Example sustainability check
    # monitor.check_sustainability(
    #     token_id="finvesta",
    #     daily_volume=1000000,  # $1M
    #     tax_rate=0.05,  # 5%
    #     total_supply_value=10000000,  # $10M
    #     daily_roi=0.01  # 1%
    # )
    
    # Generate plots
    for token in monitor.tokens:
        monitor.plot_token_data(token, save_path=f"{token}_analysis.png")
