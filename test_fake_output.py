"""
Test script to demonstrate the realistic fake output
"""

import asyncio
import random
import os

async def demo_fake_output():
    """Demonstrate the realistic fake output"""
    print("=" * 50)
    print("Football Ticket Bot - Fake Output Demo")
    print("=" * 50)
    print("NOTE: This is a demonstration of the fake output format")
    print()
    
    # Simulate the fake output directly
    print("Target match: Arsenal vs Tottenham")
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

if __name__ == "__main__":
    asyncio.run(demo_fake_output())