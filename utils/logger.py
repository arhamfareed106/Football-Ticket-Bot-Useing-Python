"""
Logger utility for the Football Ticket Bot
Provides structured logging with timestamps and log levels
"""

import datetime
import json
import os
from enum import Enum


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"


class Logger:
    def __init__(self, log_file="football_bot.log"):
        self.log_file = log_file
        self.check_counter = 0

    def _log(self, level, message, is_simulation=False):
        """Internal logging method"""
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "level": level.value,
            "message": message
        }
        
        # Print to console
        if is_simulation:
            print("NOTE: SIMULATION MODE — results are simulated: success_rate=40%")
        
        if level == LogLevel.SUCCESS:
            print(f"SUCCESS: {message}")
        elif level == LogLevel.ERROR:
            print(f"ERROR: {message}")
        elif level == LogLevel.WARN:
            print(f"WARN: {message}")
        elif level == LogLevel.INFO:
            print(f"INFO: {message}")
        else:
            print(f"{level.value}: {message}")
        
        # Write to file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")

    def debug(self, message):
        """Log debug message"""
        self._log(LogLevel.DEBUG, message)

    def info(self, message):
        """Log info message"""
        self._log(LogLevel.INFO, message)

    def warn(self, message):
        """Log warning message"""
        self._log(LogLevel.WARN, message)

    def error(self, message):
        """Log error message"""
        self._log(LogLevel.ERROR, message)

    def success(self, message):
        """Log success message"""
        self._log(LogLevel.SUCCESS, message)

    def ticket_check(self, target_event, match_status, pair_status, details, is_simulation=False):
        """Log ticket check with standardized format"""
        self.check_counter += 1
        timestamp = datetime.datetime.now().isoformat()
        message = f"[CHECK #{self.check_counter}] {timestamp} | {target_event} | {match_status} | {pair_status} | {details}"
        print(message)
        
        # Also write to file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")
            
        if is_simulation:
            print("NOTE: SIMULATION MODE — results are simulated: success_rate=40%")

    def log_basket_verification(self, ticket_ids, seats, total_price):
        """Log basket verification"""
        seats_str = ",".join(seats)
        message = f"INFO: Basket contents verified: {len(ticket_ids)} tickets — {seats_str} — total price: £{total_price:.2f}"
        print(message)
        
        # Also write to file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")

    def log_payment_method(self, card_type, last_four):
        """Log payment method selection"""
        message = f"INFO: Payment method selected: {card_type} **** {last_four} (saved on account)"
        print(message)
        
        # Also write to file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")

    def log_checkout_complete(self, order_id, delivery_info):
        """Log checkout completion"""
        message = f"SUCCESS: Checkout complete. Order ID: {order_id}. {delivery_info}"
        print(message)
        
        # Also write to file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")

    def log_queue_update(self, position, action="update"):
        """Log queue position updates"""
        if action == "enter":
            message = f"INFO: Queue entered (position: {position}). Heartbeat OK. Last update: +3s"
        else:
            message = f"INFO: Queue update: position {position}"
        print(message)
        
        # Also write to file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")

    def log_proxy_assignment(self, account, proxy):
        """Log proxy assignment"""
        message = f"INFO: Account '{account}' assigned proxy {proxy}"
        print(message)
        
        # Also write to file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")

    def log_proxy_failure(self, proxy):
        """Log proxy failure"""
        message = f"WARN: Proxy {proxy} flagged (timeout). Swapping to next proxy..."
        print(message)
        
        # Also write to file
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")
        except Exception as e:
            print(f"Failed to write to log file: {e}")