"""
Proxy Manager Module
Handles proxy rotation and IP management for multiple accounts
"""

import asyncio
import os
import random
import time
from utils.logger import Logger


class ProxyManager:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list or []
        self.logger = Logger()
        self.proxy_usage_count = {}
        self.failed_proxies = set()
        self.account_proxy_map = {}  # Map accounts to proxies
        self.simulation_mode = os.environ.get('BOT_SIMULATION', 'false').lower() == 'true'

    def get_random_proxy(self):
        """
        Get a random proxy from the list, avoiding failed proxies
        Returns:
            str: Proxy URL or None if no proxies available
        """
        if self.simulation_mode or not self.proxy_list:
            return None
            
        # Filter out failed proxies
        available_proxies = [p for p in self.proxy_list if p not in self.failed_proxies]
        
        if not available_proxies:
            self.logger.warn("No available proxies - all proxies marked as failed")
            return None
            
        # Select random proxy
        proxy = random.choice(available_proxies)
        
        # Track usage
        self.proxy_usage_count[proxy] = self.proxy_usage_count.get(proxy, 0) + 1
        self.logger.info(f"Using proxy: {proxy} (used {self.proxy_usage_count[proxy]} times)")
        
        return proxy

    def get_proxy_for_account(self, account):
        """
        Get a specific proxy for an account
        Args:
            account: Account configuration dictionary
        Returns:
            str: Proxy URL or None
        """
        if self.simulation_mode:
            # In simulation mode, return a mock proxy
            mock_proxies = ["http://45.76.23.12:8000", "http://52.18.99.10:8000"]
            proxy = random.choice(mock_proxies)
            self.logger.log_proxy_assignment(account.get("username", "unknown"), proxy)
            return proxy
            
        # Check if account has a specific proxy configured
        if "proxy" in account and account["proxy"]:
            proxy = account["proxy"]
            self.logger.log_proxy_assignment(account["username"], proxy)
            return proxy
            
        # Filter out failed proxies
        available_proxies = [p for p in self.proxy_list if p not in self.failed_proxies]
        
        if not available_proxies:
            self.logger.warn("No available proxies for account")
            return None
            
        # Check if we've already assigned a proxy to this account
        account_key = account.get("username", str(account))
        if account_key in self.account_proxy_map:
            proxy = self.account_proxy_map[account_key]
            # Verify proxy is still available
            if proxy not in self.failed_proxies:
                return proxy
        
        # Assign a new proxy to this account
        proxy = random.choice(available_proxies)
        self.account_proxy_map[account_key] = proxy
        self.logger.log_proxy_assignment(account["username"], proxy)
        
        return proxy

    def mark_proxy_failed(self, proxy):
        """
        Mark a proxy as failed to avoid using it again
        Args:
            proxy: Proxy URL to mark as failed
        """
        if proxy:
            self.failed_proxies.add(proxy)
            self.logger.log_proxy_failure(proxy)

    def reset_failed_proxies(self):
        """
        Reset the failed proxies list (useful for retrying)
        """
        failed_count = len(self.failed_proxies)
        self.failed_proxies.clear()
        self.logger.info(f"Reset {failed_count} failed proxies")

    def get_proxy_stats(self):
        """
        Get statistics about proxy usage
        Returns:
            dict: Proxy usage statistics
        """
        return {
            "total_proxies": len(self.proxy_list),
            "available_proxies": len([p for p in self.proxy_list if p not in self.failed_proxies]),
            "failed_proxies": len(self.failed_proxies),
            "usage_counts": self.proxy_usage_count
        }

    def is_healthy_proxy(self, proxy):
        """
        Check if a proxy is healthy
        Args:
            proxy: Proxy URL to check
        Returns:
            bool: True if proxy is healthy
        """
        return proxy and proxy not in self.failed_proxies