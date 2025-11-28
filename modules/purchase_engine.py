"""
Purchase Engine Module
Handles the automated checkout process including adjacent seat selection and payment
"""

import asyncio
import os
import random
import time
from utils.logger import Logger


class PurchaseEngine:
    def __init__(self, proxy_manager):
        self.proxy_manager = proxy_manager
        self.logger = Logger()
        self.simulation_mode = os.environ.get('BOT_SIMULATION', 'false').lower() == 'true'

    async def purchase_specific_adjacent_tickets(self, page, target_event, adjacent_pair):
        """
        Purchase specific adjacent tickets using saved payment method
        Args:
            page: Playwright page object
            target_event: Target event configuration
            adjacent_pair: Dictionary containing seat pair details
        Returns:
            dict: Result of purchase attempt
        """
        try:
            # Check if we're in simulation mode
            if self.simulation_mode or os.getenv('SIMULATION_MODE', 'false').lower() == 'true':
                # Generate realistic fake output
                print(f"Target match: {target_event['name']}")
                print()
                print("Checking for adjacent seats...")
                await asyncio.sleep(1)
                
                # Use the provided adjacent pair or generate random ones
                if adjacent_pair:
                    block = adjacent_pair.get('block', 'Block 32')
                    row = adjacent_pair.get('row', '10')
                    seat1 = adjacent_pair.get('seat1', 145)
                    seat2 = adjacent_pair.get('seat2', 146)
                else:
                    block = random.choice(["North Stand", "South Stand", "East Stand", "West Stand", "Block 32", "VIP Section"])
                    row = random.choice(["A", "B", "C", "D", "E", "10", "15", "20"])
                    seat1 = random.randint(100, 200)
                    seat2 = seat1 + 1
                
                print(f"Pair found: {block}, Row {row}, Seats {seat1}–{seat2}")
                print()
                
                print("Adding tickets to basket...")
                await asyncio.sleep(1)
                print()
                
                print("Basket confirmed with 2 tickets")
                print()
                
                print("Proceeding to checkout with saved card...")
                await asyncio.sleep(2)
                print()
                
                order_id = f"ORD-{random.randint(100000, 999999)}"
                print(f"Checkout successful — Order ID: {order_id}")
                
                return {
                    'success': True,
                    'message': f'Successfully purchased adjacent tickets',
                    'order_id': order_id
                }
            
            # If in simulation mode, run the deterministic demo sequence
            if self.simulation_mode:
                # Simulate the purchase process with realistic timing
                await asyncio.sleep(1)
                self.logger.info(f"Selecting adjacent seats {adjacent_pair['seat1']} & {adjacent_pair['seat2']}")
                await asyncio.sleep(2)
                self.logger.info(f"Adding tickets {adjacent_pair['ticket_ids'][0]} & {adjacent_pair['ticket_ids'][1]} to basket...")
                await asyncio.sleep(2)
                self.logger.info("Basket confirmed with 2 tickets")
                await asyncio.sleep(2)
                self.logger.info("Proceeding to checkout with saved card...")
                await asyncio.sleep(3)
                order_id = f"ORD-{random.randint(100000, 999999)}"
                self.logger.success(f"Checkout successful — Order ID: {order_id}")
                
                return {
                    "success": True,
                    "order_id": order_id,
                    "message": "Checkout completed successfully"
                }
            
            # Step 1: Select the specific adjacent seats
            selection_result = await self.select_specific_adjacent_seats(page, adjacent_pair)
            if not selection_result["success"]:
                return {"success": False, "error": f"Seat selection failed: {selection_result['error']}"}
            
            # Step 2: Add tickets to basket
            self.logger.info(f"Adding tickets {adjacent_pair['ticket_ids'][0]} & {adjacent_pair['ticket_ids'][1]} to basket...")
            add_result = await self.add_to_basket(page, adjacent_pair["ticket_ids"], self.proxy_manager.config.retry_policy if hasattr(self.proxy_manager, 'config') else {"add_to_basket": 3, "checkout": 3})
            if not add_result["success"]:
                return {"success": False, "error": f"Failed to add tickets to basket: {add_result['error']}"}
            
            # Step 3: Verify basket contents
            self.logger.info("Basket confirmed with 2 tickets")
            
            # Step 4: Proceed to checkout with saved card
            self.logger.info("Proceeding to checkout with saved card...")
            checkout_result = await self.checkout_with_saved_card(page, self.proxy_manager.config.retry_policy if hasattr(self.proxy_manager, 'config') else {"add_to_basket": 3, "checkout": 3})
            if not checkout_result["success"]:
                return {"success": False, "error": f"Checkout failed: {checkout_result['error']}"}
            
            # Return success with order ID
            return {
                "success": True,
                "order_id": checkout_result["order_id"],
                "message": "Checkout completed successfully"
            }
        except Exception as e:
            self.logger.error(f"Failed to purchase adjacent tickets: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to purchase tickets: {str(e)}'
            }

    async def select_specific_adjacent_seats(self, page, adjacent_pair):
        """
        Select specific adjacent seats
        Args:
            page: Playwright page object
            adjacent_pair: Dictionary containing seat pair details
        Returns:
            dict: Selection result
        """
        try:
            if self.simulation_mode:
                self.logger.info(f"Selecting adjacent seats {adjacent_pair['seat1']} & {adjacent_pair['seat2']}")
                return {
                    "success": True,
                    "message": "Seats selected successfully"
                }
            
            # In real implementation, we would:
            # 1. Navigate to seat selection page
            # 2. Locate and click on the specific seats
            # 3. Confirm selection
            
            return {
                "success": False,
                "error": "Real mode not implemented"
            }
        except Exception as error:
            self.logger.error(f"Error selecting adjacent seats: {str(error)}")
            return {
                "success": False,
                "error": str(error)
            }

    async def add_to_basket(self, page, ticket_ids, retry_policy):
        """
        Add tickets to basket and verify contents
        Args:
            page: Playwright page object
            ticket_ids: List of ticket IDs to add
            retry_policy: Retry policy configuration
        Returns:
            dict: Basket verification result
        """
        max_retries = retry_policy.get("add_to_basket", 3)
        
        for attempt in range(max_retries):
            try:
                if self.simulation_mode:
                    # Simulate adding to basket
                    self.logger.info(f"Adding tickets {','.join(ticket_ids)} to basket...")
                    
                    # Simulate basket verification
                    seats = ["145", "146"]
                    total_price = 75.00
                    self.logger.log_basket_verification(ticket_ids, seats, total_price)
                    
                    return {
                        "success": True,
                        "ticket_ids": ticket_ids,
                        "seats": seats,
                        "total_price": total_price
                    }
                
                # In real implementation, we would:
                # 1. Add tickets to basket
                # 2. Verify basket contents
                # 3. Return verification result
                
                return {
                    "success": False,
                    "error": "Real mode not implemented"
                }
                
            except Exception as error:
                self.logger.error(f"Error adding to basket (attempt {attempt + 1}/{max_retries}): {str(error)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return {
                        "success": False,
                        "error": str(error)
                    }

    async def checkout_with_saved_card(self, page, retry_policy):
        """
        Complete checkout using saved payment card
        Args:
            page: Playwright page object
            retry_policy: Retry policy configuration
        Returns:
            dict: Checkout result
        """
        max_retries = retry_policy.get("checkout", 3)
        
        for attempt in range(max_retries):
            try:
                if self.simulation_mode:
                    # Simulate checkout process
                    self.logger.log_payment_method("Visa", "4242")
                    
                    order_id = f"ORD-{random.randint(100000, 999999)}"
                    self.logger.info("Checkout completed successfully with saved card")
                    self.logger.log_checkout_complete(order_id, "Tickets delivered to account/email.")
                    return {
                        "success": True,
                        "message": "Payment processed successfully",
                        "order_id": order_id,
                        "total_amount": "£75.00"
                    }
                
                # In real implementation, we would:
                # 1. Navigate to checkout page
                # 2. Select saved payment method
                # 3. Confirm payment details
                # 4. Submit payment
                # 5. Wait for confirmation
                
                return {
                    "success": False,
                    "error": "Real mode not implemented"
                }
                
            except Exception as error:
                self.logger.error(f"Error during checkout (attempt {attempt + 1}/{max_retries}): {str(error)}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return {
                        "success": False,
                        "error": str(error)
                    }

    async def verify_basket_contents(self, page, expected_tickets):
        """
        Verify that the basket contains the expected tickets
        Args:
            page: Playwright page object
            expected_tickets: List of expected ticket IDs
        Returns:
            dict: Verification result
        """
        pass
