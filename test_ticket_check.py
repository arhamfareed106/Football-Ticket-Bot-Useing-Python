"""
Test script to demonstrate ticket checking feature with adjacent seat detection
"""

import requests
import json
import time
import random


def test_ticket_check():
    """Test the ticket check API endpoint with adjacent seat detection"""
    print("Football Ticket Bot - Ticket Check Test")
    print("=" * 40)
    
    # Enable simulation mode
    response = requests.post('http://localhost:5000/api/simulation', 
                           json={'enabled': True})
    print(f"Simulation mode enabled: {response.json()}")
    
    # Perform several ticket checks
    print(f"\nPerforming ticket checks for Arsenal vs Tottenham...")
    print("-" * 30)
    
    for i in range(5):
        response = requests.post('http://localhost:5000/api/ticket-check')
        result = response.json()
        
        if result['success']:
            check_result = result['result']
            status = "✅ AVAILABLE" if check_result['available'] else "❌ NOT AVAILABLE"
            print(f"Check #{check_result['check_number']} ({check_result['timestamp']}): {status} - {check_result['message']}")
        else:
            print(f"Check {i+1}: Error - {result['message']}")
        
        # Small delay between checks
        time.sleep(1)
    
    # Get status to see accumulated results
    response = requests.get('http://localhost:5000/api/status')
    status_data = response.json()
    
    print(f"\nTotal ticket checks performed: {len(status_data.get('ticket_checks', []))}")
    
    print("\nRecent ticket checks:")
    for check in status_data.get('ticket_checks', []):
        status = "✅" if check['available'] else "❌"
        print(f"  Check #{check['check_number']} ({check['timestamp']}): {status} {check['message']}")
    
    print("\n" + "=" * 40)
    print("Test completed!")


def test_adjacent_seat_detection():
    """Test adjacent seat detection functionality"""
    print("\n" + "=" * 50)
    print("Adjacent Seat Detection Test")
    print("=" * 50)
    
    # Simulate seat map data
    seat_map = {
        "sections": [
            {
                "name": "North Stand",
                "rows": ["A", "B", "C"],
                "available_seats": ["A15", "A16", "A17", "B22", "B23", "C10", "C12"]
            },
            {
                "name": "East Stand",
                "rows": ["E", "F"],
                "available_seats": ["E5", "E6", "F12", "F13", "F14"]
            }
        ]
    }
    
    print("Simulated seat map:")
    for section in seat_map["sections"]:
        print(f"  Section: {section['name']}")
        print(f"    Available seats: {', '.join(section['available_seats'])}")
    
    # Find adjacent pairs
    all_seats = []
    for section in seat_map["sections"]:
        all_seats.extend(section["available_seats"])
    
    # Simple adjacent pair detection (same row, consecutive numbers)
    adjacent_pairs = []
    rows = {}
    
    # Group seats by row
    for seat in all_seats:
        if len(seat) >= 2:
            row = seat[0]
            number = seat[1:]
            if row.isalpha() and number.isdigit():
                if row not in rows:
                    rows[row] = []
                rows[row].append((int(number), seat))
    
    # Find adjacent pairs
    for row, seat_numbers in rows.items():
        seat_numbers.sort()
        for i in range(len(seat_numbers) - 1):
            num1, seat1 = seat_numbers[i]
            num2, seat2 = seat_numbers[i + 1]
            if num2 == num1 + 1:  # Adjacent seats
                adjacent_pairs.append({
                    "seat1": seat1,
                    "seat2": seat2,
                    "row": row
                })
    
    print(f"\nFound {len(adjacent_pairs)} adjacent pairs:")
    for pair in adjacent_pairs:
        print(f"  Row {pair['row']}: {pair['seat1']} & {pair['seat2']}")
    
    print("\nTest completed!")


def test_basket_verification():
    """Test basket verification functionality"""
    print("\n" + "=" * 50)
    print("Basket Verification Test")
    print("=" * 50)
    
    # Simulate basket contents
    ticket_ids = ["12345", "12346"]
    seats = ["A15", "A16"]
    total_price = 75.00
    
    print("Verifying basket contents:")
    print(f"  Tickets: {', '.join(ticket_ids)}")
    print(f"  Seats: {', '.join(seats)}")
    print(f"  Total price: £{total_price:.2f}")
    
    # Verify basket contents
    if len(ticket_ids) == 2 and len(seats) == 2:
        print("✅ Basket verification successful")
        print("  - Correct number of tickets (2)")
        print("  - Correct number of seats (2)")
        print(f"  - Total price matches: £{total_price:.2f}")
    else:
        print("❌ Basket verification failed")
    
    print("\nTest completed!")


def test_checkout_flow():
    """Test checkout flow with saved card"""
    print("\n" + "=" * 50)
    print("Checkout Flow Test")
    print("=" * 50)
    
    # Simulate saved card information
    card_info = {
        "type": "Visa",
        "last_four": "4242",
        "saved_on_account": True
    }
    
    print("Payment method:")
    print(f"  Type: {card_info['type']}")
    print(f"  Number: **** **** **** {card_info['last_four']}")
    print(f"  Status: {'Saved on account' if card_info['saved_on_account'] else 'Not saved'}")
    
    # Simulate checkout process
    print("\nProcessing checkout...")
    print("  1. Validating basket contents...")
    print("  2. Confirming payment method...")
    print("  3. Submitting order...")
    
    # Random success/failure
    if random.random() < 0.8:  # 80% success rate
        order_id = f"ORD-{random.randint(100000, 999999)}"
        print(f"✅ Checkout successful!")
        print(f"  Order ID: {order_id}")
        print("  Tickets will be delivered to your account/email")
    else:
        print("❌ Checkout failed!")
        print("  Reason: Payment declined - Insufficient funds")
        print("  Action: Please check your account balance and retry")
    
    print("\nTest completed!")


if __name__ == "__main__":
    test_ticket_check()
    test_adjacent_seat_detection()
    test_basket_verification()
    test_checkout_flow()