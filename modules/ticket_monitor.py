"""
Ticket Monitor Module
Handles monitoring for ticket availability and detecting adjacent seats
"""

import asyncio
import os
import random
import time
import re
from utils.logger import Logger


class TicketMonitor:
    def __init__(self):
        self.logger = Logger()
        self.last_check_time = None
        self.last_available_tickets = None
        # Check if we're in simulation mode
        self.simulation_mode = os.environ.get('BOT_SIMULATION', 'false').lower() == 'true'

    async def check_availability(self, target_url, proxy=None):
        """Check if tickets are available for the target match"""
        self.logger.info(f"Checking ticket availability for {target_url}")
        
        # If in simulation mode, run the deterministic demo sequence
        if self.simulation_mode or os.getenv('SIMULATION_MODE', 'false').lower() == 'true':
            # 30% chance of detecting tickets in simulation mode
            is_available = random.random() < 0.3
            
            if is_available:
                # Return a simulated adjacent seat pair
                blocks = ["North Stand", "South Stand", "East Stand", "West Stand", "Block 32", "VIP Section"]
                rows = ["A", "B", "C", "D", "E", "10", "15", "20"]
                seat_num = random.randint(100, 200)
                
                return {
                    'available': True,
                    'block': random.choice(blocks),
                    'row': random.choice(rows),
                    'seat1': seat_num,
                    'seat2': seat_num + 1
                }
            else:
                return {'available': False}
        
        # In real implementation, we would use Playwright to check availability
        # This is a placeholder for the actual implementation
        try:
            # 1. Navigate to the target URL using Playwright
            # 2. Check for ticket availability
            # 3. Look for adjacent seat pairs
            # 4. Return True if adjacent seats are found
            pass
        except Exception as error:
            self.logger.error(f"Error checking ticket availability: {str(error)}")
            return {"success": False, "error": str(error)}

    async def find_adjacent_seats(self, page):
        """
        Find adjacent seats in the seating map
        Args:
            page: Playwright page object
        Returns:
            dict: Adjacent seat pair information or None if not found
        """
        if self.simulation_mode:
            # In simulation mode, randomly generate adjacent seat pairs
            if random.random() < 0.4:  # 40% chance of finding adjacent seats
                pairs = [
                    {"seat1": "A15", "seat2": "A16", "block": "North Stand", "ticket_ids": ["12345", "12346"]},
                    {"seat1": "B22", "seat2": "B23", "block": "East Stand", "ticket_ids": ["12347", "12348"]}
                ]
                selected_pair = random.choice(pairs)
                self.logger.info(f"Pair found: Block: {selected_pair['block']}, Row: {selected_pair['seat1'][0]}, Seats: {selected_pair['seat1']} & {selected_pair['seat2']} (ticket_ids: {','.join(selected_pair['ticket_ids'])})")
                return [selected_pair]
            else:
                # Log top 5 nearest options when no pairs found
                single_seats = [
                    {"block": "North Stand", "row": "A", "seat": "A15", "ticket_id": "12345"},
                    {"block": "North Stand", "row": "A", "seat": "A17", "ticket_id": "12349"},
                    {"block": "East Stand", "row": "B", "seat": "B22", "ticket_id": "12347"},
                    {"block": "East Stand", "row": "B", "seat": "B24", "ticket_id": "12350"},
                    {"block": "West Stand", "row": "C", "seat": "C10", "ticket_id": "12351"}
                ]
                self.logger.warn("No adjacent pair available. Top single seats:")
                for seat in single_seats[:5]:
                    self.logger.warn(f"  Block {seat['block']} Row {seat['row']} Seat {seat['seat']} (ticket_id: {seat['ticket_id']})")
                return []
        
        # In real implementation, we would:
        # 1. Parse the seating map on the page
        # 2. Identify available seats
        # 3. Find adjacent pairs (same row, consecutive numbers)
        # 4. Return list of adjacent pairs
        
        return []

    def parse_seat_map(self, seat_data):
        """
        Parse seat map data to find adjacent seats
        Args:
            seat_data: Raw seat map data from API or page
        Returns:
            list: List of adjacent seat pairs
        """
        if not seat_data:
            return []
            
        # Group seats by row
        rows = {}
        for seat in seat_data:
            # Extract row (first letter) and seat number
            match = re.match(r'^([A-Z])(\d+)$', seat)
            if match:
                row, number = match.groups()
                if row not in rows:
                    rows[row] = []
                rows[row].append((int(number), seat))
        
        # Find adjacent pairs in each row
        pairs = []
        for row, seat_numbers in rows.items():
            # Sort by seat number
            seat_numbers.sort()
            
            # Find consecutive numbers
            for i in range(len(seat_numbers) - 1):
                num1, seat1 = seat_numbers[i]
                num2, seat2 = seat_numbers[i + 1]
                
                if num2 == num1 + 1:  # Adjacent seats
                    pairs.append({
                        "seat1": seat1,
                        "seat2": seat2,
                        "row": row,
                        "numbers": [num1, num2]
                    })
        
        return pairs
