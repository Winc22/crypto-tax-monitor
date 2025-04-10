#!/usr/bin/env python3
"""
Main script for the Finvesta Ecosystem Monitoring Program

This script integrates the Finvesta ecosystem token information with the
crypto tax economy health monitoring program.
"""

import os
import sys
import json
from datetime import datetime
import argparse

# Import the monitoring classes
from crypto_monitor import CryptoMonitor
from finvesta_integration import FinvestaMonitor

# Import token configurations
from finvesta_tokens import FINVESTA_TOKENS

def setup_directories():
    """Create necessary directories for reports and plots."""
    os.makedirs("reports", exist_ok=True)
    os.makedirs("plots", exist_ok=True)

def configure_finvesta_monitor():
    """
    Configure the FinvestaMonitor with tokens from the Finvesta ecosystem.
    
    Returns:
        Configured FinvestaMonitor instance
    """
    # Create the monitor instance
    monitor = FinvestaMonitor()
    
    # Add tokens from the Finvesta ecosystem
    for token_id, token_info in FINVESTA_TOKENS.items():
        monitor.add_token(token_id, token_info["name"])
        
        # Set tax rate and ROI expectation
        if "tax_rate" in token_info:
            monitor.set_token_tax_rate(token_id, token_info["tax_rate"])
        
        if "daily_roi" in token_info:
            monitor.set_token_roi_expectation(token_id, token_info["daily_roi"])
        
        # Add token address as a wallet to monitor
        if token_info["address"]:
            monitor.add_wallet(f"{token_id}_contract", token_info["address"])
            monitor.add_project_wallet(token_id, f"{token_id}_contract", token_info["address"])
    
    return monitor

def analyze_token(monitor, token_id, check_sustainability=True, generate_plot=True):
    """
    Analyze a specific token in the Finvesta ecosystem.
    
    Args:
        monitor: FinvestaMonitor instance
        token_id: Token ID to analyze
        check_sustainability: Whether to check sustainability
        generate_plot: Whether to generate a plot
        
    Returns:
        Dictionary with analysis results
    """
    print(f"Analyzing {token_id}...")
    
    # Get token info
    token_info = FINVESTA_TOKENS.get(token_id)
    if not token_info:
        print(f"Token {token_id} not found in Finvesta ecosystem")
        return None
    
    # Analyze token health
    health = monitor.analyze_token_health(token_id)
    
    # Check sustainability if requested
    if check_sustainability:
        sustainability = monitor.check_token_sustainability(token_id)
        if health and sustainability:
            health["sustainability"] = sustainability
    
    # Generate plot if requested
    if generate_plot and health:
        plot_path = f"plots/{token_id}_analysis.png"
        monitor.plot_token_data(token_id, save_path=plot_path)
        health["plot"] = plot_path
    
    return health

def analyze_ecosystem(monitor, output_file=None):
    """
    Analyze the entire Finvesta ecosystem.
    
    Args:
        monitor: FinvestaMonitor instance
        output_file: Path to save the ecosystem report
        
    Returns:
        Dictionary with ecosystem analysis results
    """
    print("Analyzing Finvesta ecosystem...")
    
    # Run ecosystem analysis
    ecosystem = monitor.analyze_multi_token_ecosystem(list(FINVESTA_TOKENS.keys()))
    
    # Generate plots for all tokens
    if ecosystem:
        for token_id in FINVESTA_TOKENS.keys():
            plot_path = f"plots/{token_id}_analysis.png"
            try:
                monitor.plot_token_data(token_id, save_path=plot_path)
                if token_id in ecosystem["tokens"]:
                    ecosystem["tokens"][token_id]["plot"] = plot_path
            except Exception as e:
                print(f"Error generating plot for {token_id}: {str(e)}")
    
    # Save report if requested
    if output_file and ecosystem:
        with open(output_file, 'w') as f:
            json.dump(ecosystem, f, indent=2)
        print(f"Ecosystem report saved to {output_file}")
    
    return ecosystem

def check_token_relationships():
    """
    Analyze the relationships between tokens in the Finvesta ecosystem.
    
    Returns:
        Dictionary with token relationship analysis
    """
    relationships = {}
    
    # Find tokens that reward other tokens
    for token_id, token_info in FINVESTA_TOKENS.items():
        if "rewards" in token_info and token_info["rewards"]:
            for reward in token_info["rewards"]:
                if reward not in relationships:
                    relationships[reward] = {"rewarded_by": []}
                
                relationships[reward]["rewarded_by"].append({
                    "token": token_id,
                    "name": token_info["name"]
                })
    
    # Find tokens that are rewarded by other tokens
    for token_id in FINVESTA_TOKENS.keys():
        if token_id not in relationships:
            relationships[token_id] = {"rewarded_by": []}
    
    return relationships

def main():
    """Main function to run the Finvesta ecosystem monitoring program."""
    parser = argparse.ArgumentParser(description="Finvesta Ecosystem Monitoring Program")
    parser.add_argument("--token", help="Analyze a specific token in the Finvesta ecosystem")
    parser.add_argument("--list", action="store_true", help="List all tokens in the Finvesta ecosystem")
    parser.add_argument("--ecosystem", action="store_true", help="Analyze the entire Finvesta ecosystem")
    parser.add_argument("--relationships", action="store_true", help="Analyze token relationships")
    parser.add_argument("--sustainability", action="store_true", help="Check sustainability of tax models")
    parser.add_argument("--plot", action="store_true", help="Generate plots")
    parser.add_argument("--output", help="Save the report to a file")
    
    args = parser.parse_args()
    
    # Create necessary directories
    setup_directories()
    
    # List tokens if requested
    if args.list:
        print("Tokens in the Finvesta ecosystem:")
        for token_id, token_info in FINVESTA_TOKENS.items():
            print(f"- {token_info['name']} ({token_id})")
            print(f"  Address: {token_info['address']}")
            if "rewards" in token_info and token_info["rewards"]:
                print(f"  Rewards: {', '.join(token_info['rewards'])}")
            if "notes" in token_info and token_info["notes"]:
                print(f"  Notes: {token_info['notes']}")
            print()
        return
    
    # Configure the monitor
    monitor = configure_finvesta_monitor()
    
    # Process command-line arguments
    if args.token:
        # Analyze a specific token
        token_analysis = analyze_token(
            monitor, 
            args.token, 
            check_sustainability=args.sustainability,
            generate_plot=args.plot
        )
        
        if token_analysis:
            print(json.dumps(token_analysis, indent=2))
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(token_analysis, f, indent=2)
                print(f"Token analysis saved to {args.output}")
    
    elif args.relationships:
        # Analyze token relationships
        relationships = check_token_relationships()
        print("Token relationships in the Finvesta ecosystem:")
        
        for token_id, relation in relationships.items():
            if token_id in FINVESTA_TOKENS:
                token_name = FINVESTA_TOKENS[token_id]["name"]
            else:
                token_name = token_id.upper()
                
            print(f"- {token_name} ({token_id}):")
            
            if relation["rewarded_by"]:
                print(f"  Rewarded by:")
                for rewarding_token in relation["rewarded_by"]:
                    print(f"    - {rewarding_token['name']} ({rewarding_token['token']})")
            else:
                print(f"  Not rewarded by any token in the ecosystem")
            
            print()
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(relationships, f, indent=2)
            print(f"Relationship analysis saved to {args.output}")
    
    elif args.ecosystem:
        # Analyze the entire ecosystem
        ecosystem_analysis = analyze_ecosystem(monitor, args.output)
        
        if ecosystem_analysis:
            print("\nEcosystem health summary:")
            print(f"Total volume: ${ecosystem_analysis['ecosystem_metrics']['total_volume']:.2f}")
            print(f"Average price change: {ecosystem_analysis['ecosystem_metrics']['avg_price_change']:.2f}%")
            print(f"Sustainability score: {ecosystem_analysis['ecosystem_metrics']['sustainability_score']:.2f}")
            print(f"Health status: {ecosystem_analysis['ecosystem_metrics']['health_status']}")
    
    else:
        # Default behavior: run a basic health check on all tokens
        print("Running basic health check on all tokens in the Finvesta ecosystem...")
        
        results = {}
        for token_id in FINVESTA_TOKENS.keys():
            token_health = analyze_token(
                monitor, 
                token_id, 
                check_sustainability=args.sustainability,
                generate_plot=args.plot
            )
            
            if token_health:
                results[token_id] = token_health
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Health check results saved to {args.output}")


if __name__ == "__main__":
    main()
