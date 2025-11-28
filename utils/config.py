"""
Configuration utility for the Football Ticket Bot
Handles loading and saving configuration from JSON file
"""

import json
import os
from pathlib import Path


class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default config if file doesn't exist
            default_config = {
                "target_event": {
                    "name": "Arsenal vs Tottenham",
                    "event_id": "98765",
                    "url": "https://ticketexchange.com/match/arsenal-vs-tottenham-2025-11-30"
                },
                "accounts": [],
                "proxies": [],
                "refresh_interval_ms": 3000,
                "max_retries": 3,
                "delay_between_actions_ms": 500,
                "retry_policy": {
                    "add_to_basket": 3,
                    "checkout": 3
                },
                "simulation_mode": False
            }
            self.config = default_config
            self.save_config()
            return default_config
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}

    def save_config(self):
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    @property
    def target_event(self):
        """Get target event configuration"""
        return self.config.get("target_event", {})

    @property
    def accounts(self):
        """Get accounts list"""
        return self.config.get("accounts", [])

    @property
    def proxies(self):
        """Get proxies list"""
        return self.config.get("proxies", [])

    @property
    def refresh_interval_ms(self):
        """Get refresh interval in milliseconds"""
        return self.config.get("refresh_interval_ms", 3000)

    @property
    def max_retries(self):
        """Get maximum retries"""
        return self.config.get("max_retries", 3)

    @property
    def delay_between_actions_ms(self):
        """Get delay between actions in milliseconds"""
        return self.config.get("delay_between_actions_ms", 500)

    @property
    def retry_policy(self):
        """Get retry policy"""
        return self.config.get("retry_policy", {
            "add_to_basket": 3,
            "checkout": 3
        })

    @property
    def simulation_mode(self):
        """Get simulation mode flag"""
        return self.config.get("simulation_mode", False)