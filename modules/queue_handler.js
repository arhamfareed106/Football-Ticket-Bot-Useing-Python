/**
 * Queue Handler Module
 * Handles virtual queue systems for high-demand ticket releases
 */

class QueueHandler {
  constructor(proxyManager) {
    this.proxyManager = proxyManager;
    // Check if we're in simulation mode
    this.simulationMode = process.env.BOT_SIMULATION === 'true';
  }

  /**
   * Enter the virtual queue for ticket purchase
   */
  async enterQueue(page, targetUrl) {
    try {
      if (this.simulationMode) {
        // In simulation mode, randomly succeed or fail to enter queue
        if (Math.random() < 0.9) { // 90% success rate in simulation
          console.log("Successfully entered queue in simulation mode");
          return {
            success: true,
            message: "Entered queue successfully",
            queuePosition: Math.floor(Math.random() * 4900) + 100
          };
        } else {
          console.warn("Failed to enter queue in simulation mode");
          return {
            success: false,
            error: "Queue is currently closed"
          };
        }
      }
      
      // Navigate to the target match page
      await page.goto(targetUrl, {
        waitUntil: 'networkidle'
      });
      
      // Check if queue system is active
      const queueButton = await page.$('#queue-button, .join-queue, [data-action="join-queue"]');
      
      if (queueButton) {
        // Click the queue button
        await queueButton.click();
        
        // Wait for queue confirmation or redirect
        await Promise.race([
          page.waitForSelector('.queue-position, .queue-status', { timeout: 15000 }),
          page.waitForNavigation({ waitUntil: 'networkidle', timeout: 15000 })
        ]);
        
        return { success: true };
      } else {
        // No queue system detected, possibly direct access
        return { success: true };
      }
    } catch (error) {
      return { success: false, error: `Failed to enter queue: ${error.message}` };
    }
  }

  /**
   * Wait in queue until access is granted
   */
  async waitForAccess(page) {
    try {
      if (this.simulationMode) {
        // Simulate waiting in queue
        const waitTime = Math.floor(Math.random() * 25) + 5; // Wait 5-30 seconds in simulation
        console.log(`Simulating queue wait for ${waitTime} seconds`);
        
        // Simulate periodic queue position updates
        for (let i = 0; i < waitTime; i++) {
          if (i % 5 === 0) { // Every 5 seconds
            const position = Math.max(1, Math.floor(Math.random() * 1000) - i*10);
            console.log(`Queue position: ${position}`);
          }
          await this.sleep(1000);
        }
        
        // Randomly grant or deny access
        if (Math.random() < 0.8) { // 80% success rate in simulation
          console.log("Access granted to purchase tickets");
          return {
            success: true,
            message: "Access granted",
            waitTimeSeconds: waitTime
          };
        } else {
          console.warn("Access denied - queue timed out");
          return {
            success: false,
            error: "Queue timed out - please try again later"
          };
        }
      }
      
      let attempts = 0;
      const maxAttempts = 120; // 10 minutes with 5-second intervals
      
      while (attempts < maxAttempts) {
        // Check queue position
        const positionElement = await page.$('.queue-position, .position-number');
        const positionText = positionElement ? await positionElement.textContent() : '';
        
        // Log queue position
        if (positionText) {
          console.log(`Queue position: ${positionText.trim()}`);
        }
        
        // Check if access has been granted
        const accessGranted = await this.checkAccessGranted(page);
        if (accessGranted) {
          return { success: true };
        }
        
        // Check for errors or queue loss
        const queueLost = await this.checkQueueLoss(page);
        if (queueLost) {
          return { success: false, error: 'Lost position in queue' };
        }
        
        // Keep session alive
        await this.keepSessionAlive(page);
        
        // Wait before next check
        await this.sleep(5000); // 5 seconds
        attempts++;
      }
      
      return { success: false, error: 'Timeout waiting for queue access' };
    } catch (error) {
      return { success: false, error: `Error waiting for access: ${error.message}` };
    }
  }

  /**
   * Check if access to purchase has been granted
   */
  async checkAccessGranted(page) {
    try {
      // Look for indicators that access has been granted
      const purchaseButton = await page.$('#purchase-button, .buy-tickets, [data-action="buy"]');
      const ticketSelection = await page.$('.seat-map, .ticket-selection, .seating-chart');
      const countdownTimer = await page.$('.countdown-timer, .access-timer');
      
      return !!purchaseButton || !!ticketSelection || !!countdownTimer;
    } catch (error) {
      return false;
    }
  }

  /**
   * Check if we've lost our position in the queue
   */
  async checkQueueLoss(page) {
    try {
      // Look for indicators of queue loss
      const queueLostMessage = await page.$('.queue-lost, .session-expired, .timeout-error');
      const errorMessage = await page.$('.error-message, .alert-danger');
      
      if (errorMessage) {
        const errorText = await errorMessage.textContent();
        const queueLossIndicators = [
          'queue', 'expired', 'timeout', 'session', 'position lost'
        ];
        
        const lowerErrorText = errorText.toLowerCase();
        return queueLossIndicators.some(indicator => 
          lowerErrorText.includes(indicator)
        );
      }
      
      return !!queueLostMessage;
    } catch (error) {
      return false;
    }
  }

  /**
   * Keep the session alive while in queue
   */
  async keepSessionAlive(page) {
    try {
      // Refresh page periodically to keep session alive
      // But do it carefully to not lose queue position
      
      // Send a heartbeat request if available
      await page.evaluate(() => {
        // Look for keep-alive endpoints
        const scripts = Array.from(document.scripts);
        const keepAliveScript = scripts.find(script => 
          script.src && (script.src.includes('heartbeat') || script.src.includes('keepalive'))
        );
        
        if (keepAliveScript) {
          // In a real implementation, we would make the actual request
          // This is just a placeholder
          console.log('Keeping session alive...');
        }
      });
      
      // Alternatively, we could refresh the page carefully
      // await page.reload({ waitUntil: 'networkidle' });
      
      return true;
    } catch (error) {
      // Don't fail the entire process if keep-alive fails
      console.warn(`Warning: Failed to keep session alive: ${error.message}`);
      return true;
    }
  }

  /**
   * Refresh the queue page safely without losing position
   */
  async safeRefresh(page) {
    try {
      // Store current URL
      const currentUrl = page.url();
      
      // Reload the page
      await page.reload({
        waitUntil: 'networkidle',
        timeout: 30000
      });
      
      // Verify we're still in the queue or have access
      const accessGranted = await this.checkAccessGranted(page);
      const inQueue = await page.$('.queue-position, .queue-status');
      
      if (accessGranted || inQueue) {
        return { success: true };
      } else {
        return { success: false, error: 'Lost queue position after refresh' };
      }
    } catch (error) {
      return { success: false, error: `Failed to refresh: ${error.message}` };
    }
  }

  /**
   * Utility function to sleep for specified milliseconds
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

module.exports = { QueueHandler };