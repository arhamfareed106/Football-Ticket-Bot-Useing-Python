"""
Main entry point for the Football Ticket Bot
This bot automates the process of monitoring and purchasing football tickets
with anti-detection features and multi-account support
"""

import asyncio
import json
import os
import random
import time
from pathlib import Path

# Import bot modules
from modules.proxy_manager import ProxyManager
from modules.login_manager import LoginManager
from modules.queue_handler import QueueHandler
from modules.ticket_monitor import TicketMonitor
from modules.purchase_engine import PurchaseEngine
from utils.logger import Logger
from utils.config import Config


class FootballTicketBot:
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.proxy_manager = ProxyManager(self.config.proxies)
        self.login_manager = LoginManager(self.proxy_manager)
        self.queue_handler = QueueHandler(self.proxy_manager)
        self.ticket_monitor = TicketMonitor()
        self.purchase_engine = PurchaseEngine(self.proxy_manager)
        
        self.accounts = self.config.accounts
        self.target_match_url = self.config.target_match_url
        self.is_running = False

    async def initialize(self):
        """Initialize the bot and all its components"""
        self.logger.info("Initializing Football Ticket Bot...")
        
        try:
            # Initialize Playwright browsers for each account
            await self.login_manager.initialize_browsers()
            
            # Validate configuration
            if not self.accounts or len(self.accounts) == 0:
                raise Exception("No accounts configured")
            
            if not self.target_match_url:
                raise Exception("No target match URL configured")
            
            self.logger.info(f"Bot initialized with {len(self.accounts)} accounts")
            return True
        except Exception as error:
            self.logger.error(f"Failed to initialize bot: {str(error)}")
            return False

    async def run(self):
        """Main bot execution loop"""
        self.is_running = True
        self.logger.info("Starting Football Ticket Bot...")
        
        while self.is_running:
            try:
                # Monitor for ticket availability
                tickets_available = await self.ticket_monitor.check_availability(
                    self.target_match_url,
                    self.proxy_manager.get_random_proxy()
                )
                
                if tickets_available:
                    self.logger.info("Tickets detected! Initiating purchase process...")
                    
                    # Attempt purchase with all accounts
                    purchase_result = await self.attempt_purchase()
                    
                    if purchase_result["success"]:
                        self.logger.info("Purchase successful!")
                        # Optionally stop the bot after successful purchase
                        # self.stop()
                    else:
                        self.logger.warn(f"Purchase failed: {purchase_result['error']}")
                else:
                    self.logger.info("No tickets available yet. Waiting...")
                
                # Wait before next check
                await asyncio.sleep(self.config.refresh_interval_ms / 1000)
            except Exception as error:
                self.logger.error(f"Error in main loop: {str(error)}")
                await asyncio.sleep(5)  # Wait 5 seconds before retrying

    async def attempt_purchase(self):
        """Attempt to purchase tickets using all configured accounts"""
        try:
            # Login to all accounts
            logged_in_accounts = []
            for account in self.accounts:
                try:
                    login_result = await self.login_manager.login(account)
                    if login_result["success"]:
                        logged_in_accounts.append({
                            **account,
                            "browser": login_result["browser"],
                            "page": login_result["page"]
                        })
                        self.logger.info(f"Successfully logged in as {account['username']}")
                    else:
                        self.logger.warn(f"Failed to login as {account['username']}: {login_result['error']}")
                except Exception as error:
                    self.logger.error(f"Error logging in as {account['username']}: {str(error)}")
            
            if len(logged_in_accounts) == 0:
                return {"success": False, "error": "Failed to login to any accounts"}
            
            # Enter queue with all accounts
            queued_accounts = []
            for account in logged_in_accounts:
                try:
                    queue_result = await self.queue_handler.enter_queue(
                        account["page"],
                        self.target_match_url
                    )
                    
                    if queue_result["success"]:
                        queued_accounts.append(account)
                        self.logger.info(f"{account['username']} entered queue successfully")
                    else:
                        self.logger.warn(f"{account['username']} failed to enter queue: {queue_result['error']}")
                except Exception as error:
                    self.logger.error(f"Error entering queue for {account['username']}: {str(error)}")
            
            if len(queued_accounts) == 0:
                return {"success": False, "error": "Failed to enter queue with any accounts"}
            
            # Wait in queue for access
            accounts_with_access = []
            for account in queued_accounts:
                try:
                    access_result = await self.queue_handler.wait_for_access(account["page"])
                    
                    if access_result["success"]:
                        accounts_with_access.append(account)
                        self.logger.info(f"{account['username']} gained access to ticket purchase")
                    else:
                        self.logger.warn(f"{account['username']} did not gain access: {access_result['error']}")
                except Exception as error:
                    self.logger.error(f"Error waiting for access for {account['username']}: {str(error)}")
            
            if len(accounts_with_access) == 0:
                return {"success": False, "error": "No accounts gained access to purchase"}
            
            # Attempt purchase with accounts that gained access
            purchase_success = False
            purchase_error = None
            
            for account in accounts_with_access:
                try:
                    purchase_result = await self.purchase_engine.purchase_tickets(
                        account["page"],
                        2  # Number of adjacent tickets
                    )
                    
                    if purchase_result["success"]:
                        purchase_success = True
                        self.logger.info(f"Successfully purchased tickets with account {account['username']}")
                        break  # Stop after successful purchase
                    else:
                        purchase_error = purchase_result["error"]
                        self.logger.warn(f"Purchase failed with account {account['username']}: {purchase_result['error']}")
                except Exception as error:
                    self.logger.error(f"Error purchasing with account {account['username']}: {str(error)}")
            
            # Clean up browser sessions
            for account in logged_in_accounts:
                try:
                    await self.login_manager.logout(account)
                except Exception as error:
                    self.logger.error(f"Error logging out account {account['username']}: {str(error)}")
            
            return {
                "success": purchase_success,
                "error": None if purchase_success else purchase_error
            }
        except Exception as error:
            self.logger.error(f"Error in purchase attempt: {str(error)}")
            return {"success": False, "error": str(error)}

    def stop(self):
        """Stop the bot execution"""
        self.is_running = False
        self.logger.info("Stopping Football Ticket Bot...")
        self.login_manager.close_all_browsers()

    async def sleep(self, seconds):
        """Utility function to sleep for specified seconds"""
        await asyncio.sleep(seconds)


async def main():
    """Main function to run the bot"""
    bot = FootballTicketBot()
    
    # Initialize and start the bot
    success = await bot.initialize()
    if success:
        try:
            await bot.run()
        except KeyboardInterrupt:
            print("\nReceived interrupt. Shutting down gracefully...")
            bot.stop()
        except Exception as error:
            print(f"Fatal error in bot execution: {error}")
            bot.stop()
    else:
        print("Failed to initialize bot. Exiting.")


if __name__ == "__main__":
    asyncio.run(main())