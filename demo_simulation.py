"""
Demo script to show ticket detection simulation with adjacent seat detection
"""

import asyncio
import os
import random
import time
from modules.ticket_monitor import TicketMonitor
from utils.logger import Logger
from utils.config import Config


async def demo_simulation_mode():
    """Demo the simulation mode with deterministic output"""
    print("=" * 60)
    print("Football Ticket Bot - Simulation Mode Demo")
    print("=" * 60)
    
    # Load config to check simulation mode
    config = Config()
    
    if not config.simulation_mode:
        print("ERROR: Simulation mode is not enabled in config.json")
        print("Please set 'simulation_mode': true in config.json and run again")
        return
    
    print("NOTE: SIMULATION MODE — This is a simulated run and NOT a real purchase.")
    print()
    
    # Simulate the exact demo sequence
    target_event = config.target_event
    print(f"Target match: {target_event['name']}")
    print()
    
    print("Checking for adjacent seats...")
    await asyncio.sleep(1)
    print()
    
    print("Pair found: Block 32, Row 10, Seats 145–146")
    print()
    
    print("Adding tickets to basket...")
    await asyncio.sleep(1)
    print()
    
    print("Basket confirmed with 2 tickets")
    print()
    
    print("Proceeding to checkout with saved card...")
    await asyncio.sleep(1)
    print()
    
    order_id = f"ORD-{random.randint(100000, 999999)}"
    print(f"Checkout successful — Order ID: {order_id}")
    print()
    
    print("=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(demo_simulation_mode())