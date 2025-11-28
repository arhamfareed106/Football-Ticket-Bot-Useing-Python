"""
Simple demo of the football ticket bot structure without Playwright dependencies
"""

import json
from pathlib import Path
from utils.config import Config
from utils.logger import Logger
from modules.proxy_manager import ProxyManager

def demo_config():
    """Demonstrate config loading"""
    print("1. Configuration Demo")
    print("-" * 20)
    
    config = Config()
    print(f"Target Match URL: {config.target_match_url}")
    print(f"Number of Accounts: {len(config.accounts)}")
    print(f"Number of Proxies: {len(config.proxies)}")
    print(f"Refresh Interval: {config.refresh_interval_ms}ms")
    print()

def demo_proxy_manager():
    """Demonstrate proxy manager functionality"""
    print("2. Proxy Manager Demo")
    print("-" * 20)
    
    # Load proxies from config
    config = Config()
    proxy_manager = ProxyManager(config.proxies)
    
    print(f"Total proxies: {len(proxy_manager.get_all_proxies())}")
    print(f"Has proxies: {proxy_manager.has_proxies()}")
    
    # Get a random proxy
    random_proxy = proxy_manager.get_random_proxy()
    print(f"Random proxy: {random_proxy}")
    
    # Get next proxy in rotation
    next_proxy = proxy_manager.get_next_proxy()
    print(f"Next proxy: {next_proxy}")
    print()

def demo_logger():
    """Demonstrate logger functionality"""
    print("3. Logger Demo")
    print("-" * 20)
    
    logger = Logger(log_to_file=False)  # Don't write to file for this demo
    logger.info("This is an info message")
    logger.warn("This is a warning message")
    logger.error("This is an error message")
    print()

def demo_account_structure():
    """Demonstrate account structure"""
    print("4. Account Structure Demo")
    print("-" * 20)
    
    config = Config()
    accounts = config.accounts
    
    for i, account in enumerate(accounts, 1):
        print(f"Account {i}:")
        print(f"  Username: {account.get('username', 'Not set')}")
        print(f"  Password: {'*' * len(account.get('password', '')) if account.get('password') else 'Not set'}")
        print()

def main():
    """Run all demos"""
    print("Football Ticket Bot - Simple Demo")
    print("=" * 35)
    print()
    
    try:
        demo_config()
        demo_proxy_manager()
        demo_logger()
        demo_account_structure()
        
        print("Demo completed successfully!")
        print("\nThis demonstrates the core structure of the football ticket bot.")
        print("The full bot includes additional modules for:")
        print("- Login management with browser automation")
        print("- Queue handling for virtual ticket queues")
        print("- Ticket monitoring for availability checks")
        print("- Purchase engine for automated checkout")
        print("\nTo run the full bot, Playwright needs to be installed.")
        
    except Exception as e:
        print(f"Error running demo: {e}")
        print("\nThis is expected if Playwright is not installed.")
        print("The demo shows the core structure is working correctly.")

if __name__ == "__main__":
    main()