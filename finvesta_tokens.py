"""
Finvesta Ecosystem Token Configuration

This file contains configuration settings for the Finvesta ecosystem tokens
provided by the user. Update these settings with your specific token information.
"""

# Finvesta ecosystem token configuration
FINVESTA_TOKENS = {
    # Format: "token_id": {"name": "Display Name", "address": "0x...", "tax_rate": 0.05, "daily_roi": 0.01, "rewards": ["reward1", "reward2"]}
    
    # Beast
    "beast": {
        "name": "Beast",
        "address": "0xdc60f0EE40bEd3078614bE202555d2f07d38166e",
        "tax_rate": 0.05,  # Estimated, update with actual value
        "daily_roi": 0.01,  # Estimated, update with actual value
        "rewards": ["pls", "missor", "remember", "gas_money"],
        "notes": "Rewards can change"
    },
    
    # Dominance
    "dominance": {
        "name": "Dominance",
        "address": "0x116D162d729E27E2E1D6478F1d2A8AEd9C7a2beA",
        "tax_rate": 0.05,
        "daily_roi": 0.01,  # Estimated, update with actual value
        "rewards": ["pwbtc"],
        "notes": "pWBTC printer. 5% tax: 2.1% pwbtc rewards, 1.4% pulse distributed to eco buybacks, 1% auto LP stacker and 0.5% self burn."
    },
    
    # Ese Baby
    "ese_baby": {
        "name": "Ese Baby",
        "address": "0x6d664cb8F9DB9C5BCB7190c954d5b45F67f2d809",
        "tax_rate": 0.05,  # Estimated, update with actual value
        "daily_roi": 0.01,  # Estimated, update with actual value
        "rewards": ["gbaby"],
        "notes": "Rewards in Gbaby, most bullish token of the Atropa ecosystem with a price target of $14800."
    },
    
    # Flexboost
    "flexboost": {
        "name": "Flexboost",
        "address": "0x406A63a837AC947ec0C2f0E6673e8Ef481cA7807",
        "tax_rate": 0.05,  # Estimated, update with actual value
        "daily_roi": 0.005,  # Lower ROI as it pays rewards slower
        "rewards": ["variable"],
        "notes": "Flexboost is the Flexmas for builders. It can boost the liquidity and rewards from any (struggling) rewardtoken. It pays rewards much slower than other tokens."
    },
    
    # Flexmas
    "flexmas": {
        "name": "Flexmas",
        "address": "0x5ED5882164277cec6D5Ae6f420721b199C0e5693",
        "tax_rate": 0.05,  # Estimated, update with actual value
        "daily_roi": 0.01,  # Estimated, update with actual value
        "rewards": ["variable"],
        "notes": "Flexible rewards that change every Friday. Need to interact (buy/sell a lil bit) with the contract every time the rewards change in order to keep receiving rewards."
    },
    
    # Missor
    "missor": {
        "name": "Missor",
        "address": "0x063E79CF6A555dac9033EAa3c61A8f02F1020759",
        "tax_rate": 0.05,  # Estimated, update with actual value
        "daily_roi": 0.02,  # Higher ROI as it "gives one of the best rewards payout"
        "rewards": ["finvesta"],
        "notes": "OGwebchef ecosystem's bestie! Gives one of the best rewards payout. Rewards in Finvesta."
    },
    
    # Nana
    "nana": {
        "name": "Nana",
        "address": "0x5Db83315591bD3c121700890E03B8fE6Fe40a486",
        "tax_rate": 0.05,  # Estimated, update with actual value
        "daily_roi": 0.01,  # Estimated, update with actual value
        "rewards": ["affection"],
        "notes": "Launched by OG to help support the Affection minters. Rewards in Affection."
    },
    
    # Raise it up
    "raise_it_up": {
        "name": "Raise it up",
        "address": "0xA9D27362ff93f1BCEAa8290FFC36b6D98f4669b9",
        "tax_rate": 0.30,  # 30% sell and transfer tax
        "buy_tax": 0.0,    # 0% buy tax
        "daily_roi": 0.02,  # Higher ROI due to high tax
        "rewards": ["pls"],
        "notes": "0% buytax, 30% sell- and transfertax: 29.99% PLS rewards, 0.01% selfburn."
    },
    
    # Remember
    "remember": {
        "name": "Remember",
        "address": "0xC506af3eA272dAFBE1A8E39d9C3446E03637bB12",
        "tax_rate": 0.05,  # Estimated, update with actual value
        "daily_roi": 0.01,  # Estimated, update with actual value
        "rewards": ["pls"],
        "notes": "The flagship printer that rewards in PLS. Most (if not all) future launches from OG and Hums will benefit Remember in some way."
    },
    
    # Savant
    "savant": {
        "name": "Savant",
        "address": "0x041a80B38D3a5B4dbB30e56440cA8F0C8DFA6412",
        "tax_rate": 0.02,
        "daily_roi": 0.005,  # Lower ROI due to lower tax
        "rewards": ["plsx"],
        "notes": "2% tax?? Rewards in PLSX"
    },
    
    # Sursum
    "sursum": {
        "name": "Sursum",
        "address": "0x121ed41dee86741193f8856ec0cfb38158a7cbaa",
        "tax_rate": 0.05,  # Estimated, update with actual value
        "daily_roi": 0.01,  # Estimated, update with actual value
        "rewards": ["up", "upx"],
        "notes": "Rewards Up and Upx."
    },
    
    # World's Greatest pDAI Printer (WGPP)
    "wgpp": {
        "name": "World's Greatest pDAI Printer",
        "address": "0x770cfa2fb975e7bcaedde234d92c3858c517adca",
        "tax_rate": 0.05,  # Estimated, update with actual value
        "daily_roi": 0.01,  # Estimated, update with actual value
        "rewards": ["pdai"],
        "notes": "The name says it all."
    },
    
    # Mnemonics
    "mnemonics": {
        "name": "Mnemonics",
        "address": "0x578Cd5Aed5e8F06a5b7959caaFc6213e954F434E",
        "tax_rate": 0.05,  # Estimated, update with actual value
        "daily_roi": 0.01,  # Estimated, update with actual value
        "rewards": ["remember"],
        "notes": "The Remember Stacking Machine! Holding Mnemonics automatically stacks Remember, which generates PLS rewards. Boosts Remember's liquidity and price appreciation."
    },
    
    # Gas Money
    "gas_money": {
        "name": "Gas Money",
        "address": "0x042b48a98B37042D58Bc8defEEB7cA4eC76E6106",
        "tax_rate": 0.05,  # Estimated, update with actual value
        "daily_roi": 0.01,  # Estimated, update with actual value
        "rewards": ["pls"],
        "notes": "Rewards: PLS – Instant payouts, no waiting. Built to boost Mnemonics & Remember holders' payouts!"
    },
    
    # Finvesta (placeholder, update with actual address when available)
    "finvesta": {
        "name": "Finvesta",
        "address": "",  # Update with actual address
        "tax_rate": 0.05,  # Estimated, update with actual value
        "daily_roi": 0.01,  # Estimated, update with actual value
        "rewards": [],  # Update with actual rewards
        "notes": "Main token in the ecosystem"
    }
}
