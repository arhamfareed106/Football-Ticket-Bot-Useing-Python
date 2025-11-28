/**
 * Purchase Engine Module
 * Handles the automated checkout process including adjacent seat selection and payment
 */

class PurchaseEngine {
  constructor(proxyManager) {
    this.proxyManager = proxyManager;
    // Check if we're in simulation mode
    this.simulationMode = process.env.BOT_SIMULATION === 'true';
  }

  /**
   * Purchase adjacent tickets using saved payment method
   */
  async purchaseAdjacentTickets(page, ticketCount = 2) {
    try {
      console.log(`Attempting to purchase ${ticketCount} adjacent tickets...`);
      
      if (this.simulationMode) {
        // In simulation mode, randomly succeed or fail
        if (Math.random() < 0.7) { // 70% success rate in simulation
          console.log("Successfully purchased adjacent tickets in simulation mode");
          return {
            success: true,
            message: "Successfully purchased 2 adjacent tickets",
            orderId: `SIM-${Math.floor(Math.random() * 90000) + 10000}`,
            totalAmount: "£75.00"
          };
        } else {
          console.warn("Failed to purchase adjacent tickets in simulation mode");
          return {
            success: false,
            error: "Payment declined - Insufficient funds"
          };
        }
      }
      
      // In real implementation, we would:
      // 1. Navigate to ticket selection page
      // 2. Detect and select adjacent seats
      // 3. Add tickets to basket
      // 4. Proceed to checkout
      // 5. Use saved payment method
      // 6. Confirm purchase
      
      // For now, we'll return a failure in non-simulation mode
      return {
        success: false,
        error: "Real mode not implemented - requires Playwright browser automation"
      };
    } catch (error) {
      return { success: false, error: `Purchase error: ${error.message}` };
    }
  }

  /**
   * Select adjacent seats from available options
   */
  async selectAdjacentSeats(page, ticketCount) {
    try {
      if (this.simulationMode) {
        // Simulate seat selection
        const seats = [
          {seat1: "A15", seat2: "A16", section: "North Stand", price: "£37.50"},
          {seat1: "B22", seat2: "B23", section: "East Stand", price: "£37.50"}
        ];
        const selected = seats.length > 0 ? seats[Math.floor(Math.random() * seats.length)] : null;
        
        if (selected) {
          console.log(`Selected adjacent seats: ${selected.seat1} and ${selected.seat2}`);
          return {
            success: true,
            seats: selected
          };
        } else {
          return {
            success: false,
            error: "No adjacent seats available"
          };
        }
      }
      
      // In real implementation, we would:
      // 1. Parse the seating map
      // 2. Identify adjacent available seats
      // 3. Select the seats
      // 4. Add to basket
      
      return {
        success: false,
        error: "Real mode not implemented"
      };
    } catch (error) {
      return { success: false, error: `Seat selection error: ${error.message}` };
    }
  }

  /**
   * Complete checkout using saved payment card
   */
  async checkoutWithSavedCard(page) {
    try {
      if (this.simulationMode) {
        // Simulate checkout process
        if (Math.random() < 0.8) { // 80% success rate in simulation
          console.log("Checkout completed successfully with saved card");
          return {
            success: true,
            message: "Payment processed successfully",
            orderId: `SIM-${Math.floor(Math.random() * 90000) + 10000}`,
            totalAmount: "£75.00"
          };
        } else {
          console.warn("Checkout failed - payment declined");
          return {
            success: false,
            error: "Payment declined - Insufficient funds"
          };
        }
      }
      
      // In real implementation, we would:
      // 1. Navigate to checkout page
      // 2. Select saved payment method
      // 3. Confirm payment details
      // 4. Submit payment
      // 5. Wait for confirmation
      
      return {
        success: false,
        error: "Real mode not implemented"
      };
    } catch (error) {
      return { success: false, error: `Checkout error: ${error.message}` };
    }
  }

  /**
   * Execute the full purchase flow for tickets (legacy method for compatibility)
   */
  async purchaseTickets(page, ticketCount = 2) {
    try {
      console.log(`Attempting to purchase ${ticketCount} tickets...`);
      
      // Step 1: Select adjacent seats
      const seatSelectionResult = await this.selectAdjacentSeats(page, ticketCount);
      
      if (!seatSelectionResult.success) {
        return { success: false, error: `Seat selection failed: ${seatSelectionResult.error}` };
      }
      
      console.log('Seats selected successfully');
      
      // Step 2: Add to cart
      const addToCartResult = await this.addToCart(page);
      
      if (!addToCartResult.success) {
        return { success: false, error: `Add to cart failed: ${addToCartResult.error}` };
      }
      
      console.log('Tickets added to cart');
      
      // Step 3: Proceed to checkout
      const checkoutResult = await this.proceedToCheckout(page);
      
      if (!checkoutResult.success) {
        return { success: false, error: `Checkout initiation failed: ${checkoutResult.error}` };
      }
      
      console.log('Proceeded to checkout');
      
      // Step 4: Fill checkout form
      const formFillResult = await this.fillCheckoutForm(page);
      
      if (!formFillResult.success) {
        return { success: false, error: `Form filling failed: ${formFillResult.error}` };
      }
      
      console.log('Checkout form filled');
      
      // Step 5: Handle payment (modular)
      const paymentResult = await this.handlePayment(page);
      
      if (!paymentResult.success) {
        return { success: false, error: `Payment failed: ${paymentResult.error}` };
      }
      
      console.log('Payment processed successfully');
      
      // Step 6: Confirm purchase
      const confirmResult = await this.confirmPurchase(page);
      
      if (!confirmResult.success) {
        return { success: false, error: `Confirmation failed: ${confirmResult.error}` };
      }
      
      console.log('Purchase confirmed successfully');
      
      return { success: true };
    } catch (error) {
      return { success: false, error: `Purchase error: ${error.message}` };
    }
  }

  /**
   * Select adjacent seats on the seating map
   */
  async selectAdjacentSeatsLegacy(page, ticketCount) {
    try {
      // Wait for seating map to load
      await page.waitForSelector('.seating-map, .seat-chart, .venue-layout', { timeout: 15000 });
      
      // Look for available seats
      const availableSeats = await page.$$('.seat.available, [data-status="available"]');
      
      if (availableSeats.length < ticketCount) {
        return { success: false, error: `Not enough available seats. Found: ${availableSeats.length}, Needed: ${ticketCount}` };
      }
      
      // Try to find adjacent seats
      const adjacentSeats = await this.findAdjacentSeats(page, availableSeats, ticketCount);
      
      if (!adjacentSeats || adjacentSeats.length < ticketCount) {
        return { success: false, error: 'Could not find adjacent seats' };
      }
      
      // Click on the seats to select them
      for (const seat of adjacentSeats) {
        await seat.click();
        await this.randomDelay(200, 500); // Human-like delay
      }
      
      // Verify seats were selected
      const selectedSeats = await page.$$('.seat.selected, [data-selected="true"]');
      
      if (selectedSeats.length !== ticketCount) {
        return { success: false, error: `Seat selection mismatch. Selected: ${selectedSeats.length}, Expected: ${ticketCount}` };
      }
      
      return { success: true };
    } catch (error) {
      return { success: false, error: `Seat selection error: ${error.message}` };
    }
  }

  /**
   * Find adjacent seats from the available seats
   */
  async findAdjacentSeats(page, availableSeats, ticketCount) {
    try {
      // This is a simplified implementation
      // In a real scenario, you'd need to analyze the seating chart structure
      
      // For now, just return the first N seats as a placeholder
      return availableSeats.slice(0, ticketCount);
    } catch (error) {
      console.error(`Error finding adjacent seats: ${error.message}`);
      return null;
    }
  }

  /**
   * Add selected tickets to cart
   */
  async addToCart(page) {
    try {
      // Look for add to cart button
      const addToCartButton = await page.$('#add-to-cart, .add-to-cart, [data-action="add-to-cart"]');
      
      if (!addToCartButton) {
        return { success: false, error: 'Add to cart button not found' };
      }
      
      // Click the button
      await addToCartButton.click();
      
      // Wait for confirmation or cart update
      await Promise.race([
        page.waitForSelector('.cart-added, .added-to-cart, .success-message', { timeout: 10000 }),
        page.waitForNavigation({ waitUntil: 'networkidle', timeout: 10000 })
      ]);
      
      return { success: true };
    } catch (error) {
      return { success: false, error: `Add to cart error: ${error.message}` };
    }
  }

  /**
   * Proceed to checkout page
   */
  async proceedToCheckout(page) {
    try {
      // Look for checkout button
      const checkoutButton = await page.$('#checkout, .checkout-button, [data-action="checkout"]');
      
      if (!checkoutButton) {
        // Sometimes the checkout option is in a dropdown or requires clicking cart first
        const cartButton = await page.$('.cart-icon, .view-cart, #cart');
        if (cartButton) {
          await cartButton.click();
          await page.waitForSelector('#checkout, .checkout-button', { timeout: 5000 });
          checkoutButton = await page.$('#checkout, .checkout-button');
        }
      }
      
      if (!checkoutButton) {
        return { success: false, error: 'Checkout button not found' };
      }
      
      // Click the checkout button
      await checkoutButton.click();
      
      // Wait for checkout page to load
      await page.waitForNavigation({ waitUntil: 'networkidle', timeout: 15000 });
      
      // Verify we're on checkout page
      const checkoutElements = await page.$$('.checkout-form, .payment-info, .billing-address');
      
      if (checkoutElements.length === 0) {
        // Check URL
        const currentUrl = page.url().toLowerCase();
        const checkoutIndicators = ['checkout', 'payment', 'billing'];
        const isCheckoutPage = checkoutIndicators.some(indicator => 
          currentUrl.includes(indicator)
        );
        
        if (!isCheckoutPage) {
          return { success: false, error: 'Failed to navigate to checkout page' };
        }
      }
      
      return { success: true };
    } catch (error) {
      return { success: false, error: `Checkout error: ${error.message}` };
    }
  }

  /**
   * Fill the checkout form with user information
   */
  async fillCheckoutForm(page) {
    try {
      // Fill billing information
      // Note: In a real implementation, you would get this from a config file or secure storage
      const formData = {
        firstName: 'John',
        lastName: 'Smith',
        email: 'john.smith@example.com',
        phone: '555-123-4567',
        address: '123 Main St',
        city: 'Anytown',
        state: 'CA',
        zipCode: '12345',
        country: 'USA'
      };
      
      // Fill form fields with human-like typing
      await this.humanType(page, '#first-name, #firstName, [name="firstName"]', formData.firstName);
      await this.randomDelay(200, 500);
      
      await this.humanType(page, '#last-name, #lastName, [name="lastName"]', formData.lastName);
      await this.randomDelay(200, 500);
      
      await this.humanType(page, '#email, [name="email"]', formData.email);
      await this.randomDelay(200, 500);
      
      await this.humanType(page, '#phone, #phoneNumber, [name="phone"]', formData.phone);
      await this.randomDelay(200, 500);
      
      await this.humanType(page, '#address, #street, [name="address"]', formData.address);
      await this.randomDelay(200, 500);
      
      await this.humanType(page, '#city, [name="city"]', formData.city);
      await this.randomDelay(200, 500);
      
      await this.humanType(page, '#state, #region, [name="state"]', formData.state);
      await this.randomDelay(200, 500);
      
      await this.humanType(page, '#zip, #zipcode, #postalCode, [name="zip"]', formData.zipCode);
      await this.randomDelay(200, 500);
      
      // Handle country selection if it's a dropdown
      const countrySelector = await page.$('#country, [name="country"]');
      if (countrySelector) {
        // Check if it's a select dropdown
        const tagName = await page.evaluate(el => el.tagName.toLowerCase(), countrySelector);
        if (tagName === 'select') {
          await page.selectOption('#country, [name="country"]', formData.country);
        } else {
          await this.humanType(page, '#country, [name="country"]', formData.country);
        }
      }
      
      return { success: true };
    } catch (error) {
      return { success: false, error: `Form filling error: ${error.message}` };
    }
  }

  /**
   * Handle payment processing
   */
  async handlePayment(page) {
    try {
      // This is a modular placeholder - in a real implementation,
      // you would integrate with a payment service or handle manual payment
      
      // Look for payment method options
      const cardPaymentOption = await page.$('#credit-card, .card-payment, [data-method="card"]');
      const paypalOption = await page.$('#paypal, .paypal-payment');
      
      if (cardPaymentOption) {
        // Select credit card payment
        await cardPaymentOption.click();
        await this.randomDelay(500, 1000);
        
        // Fill card details (NEVER store real card details in code!)
        // In practice, you would prompt the user or integrate with a secure payment service
        await this.fillCardDetails(page);
      } else if (paypalOption) {
        // Handle PayPal payment
        await paypalOption.click();
        // Redirect to PayPal would happen here
        return { success: false, error: 'PayPal payment requires manual intervention' };
      } else {
        // Check for other payment methods or manual handling
        return { success: false, error: 'Unsupported payment method - manual intervention required' };
      }
      
      return { success: true };
    } catch (error) {
      return { success: false, error: `Payment error: ${error.message}` };
    }
  }

  /**
   * Fill credit card details (placeholder - never use real data in code!)
   */
  async fillCardDetails(page) {
    try {
      // NOTE: This is a placeholder. Never put real card details in code!
      // In a real implementation, you would either:
      // 1. Prompt the user to enter details manually
      // 2. Integrate with a secure payment service
      // 3. Use tokenized payment methods
      
      console.log('Payment details required - manual intervention needed');
      return { success: false, error: 'Manual payment details entry required' };
    } catch (error) {
      return { success: false, error: `Card details error: ${error.message}` };
    }
  }

  /**
   * Confirm the purchase
   */
  async confirmPurchase(page) {
    try {
      // Look for confirm/submit button
      const confirmButton = await page.$('#confirm, #submit, .confirm-purchase, [type="submit"]');
      
      if (!confirmButton) {
        return { success: false, error: 'Confirm button not found' };
      }
      
      // Check for captchas
      const captcha = await page.$('.captcha, #recaptcha, .g-recaptcha');
      if (captcha) {
        return { success: false, error: 'Captcha detected - manual intervention required' };
      }
      
      // Click confirm button
      await confirmButton.click();
      
      // Wait for confirmation page or success message
      await Promise.race([
        page.waitForSelector('.confirmation, .success, .order-confirmed', { timeout: 20000 }),
        page.waitForNavigation({ waitUntil: 'networkidle', timeout: 20000 })
      ]);
      
      // Check for success indicators
      const successElements = await page.$$('.confirmation, .success-message, .order-confirmed, .thank-you');
      
      if (successElements.length > 0) {
        return { success: true };
      }
      
      // Check page content for success messages
      const content = await page.content();
      const successIndicators = ['confirmed', 'successful', 'thank you', 'order placed'];
      const lowerContent = content.toLowerCase();
      
      const isSuccess = successIndicators.some(indicator => 
        lowerContent.includes(indicator)
      );
      
      return { success: isSuccess };
    } catch (error) {
      return { success: false, error: `Confirmation error: ${error.message}` };
    }
  }

  /**
   * Simulate human-like typing with random delays
   */
  async humanType(page, selector, text) {
    try {
      await page.focus(selector);
      
      for (const char of text) {
        await page.type(selector, char, { delay: this.randomInt(50, 150) });
      }
    } catch (error) {
      // Fallback: direct fill if typing fails
      await page.fill(selector, text);
    }
  }

  /**
   * Generate a random delay between min and max milliseconds
   */
  async randomDelay(min, max) {
    const delay = this.randomInt(min, max);
    return new Promise(resolve => setTimeout(resolve, delay));
  }

  /**
   * Generate a random integer between min and max (inclusive)
   */
  randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }
}

module.exports = { PurchaseEngine };