/**
 * Ticket Monitor Module
 * Handles monitoring for ticket availability and detecting adjacent seats
 */

const axios = require('axios');

class TicketMonitor {
  constructor() {
    this.lastCheckTime = null;
    this.lastAvailableTickets = null;
    // Check if we're in simulation mode
    this.simulationMode = process.env.BOT_SIMULATION === 'true';
  }

  /**
   * Check if tickets are available for the target match
   */
  async checkAvailability(targetUrl, proxy = null) {
    try {
      // If in simulation mode, randomly return true to simulate ticket detection
      if (this.simulationMode) {
        // 30% chance of detecting tickets
        return Math.random() < 0.3;
      }
      
      // Method 1: Direct page check using Playwright (more reliable)
      // This would be called from the main bot with a page instance
      
      // Method 2: HTTP request check (faster but less reliable)
      const config = {
        url: targetUrl,
        method: 'GET',
        timeout: 10000, // 10 second timeout
        headers: {
          'User-Agent': this.getRandomUserAgent(),
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.5',
          'Accept-Encoding': 'gzip, deflate',
          'Connection': 'keep-alive',
          'Upgrade-Insecure-Requests': '1',
        }
      };
      
      // Add proxy if provided
      if (proxy) {
        config.proxy = this.parseProxy(proxy);
      }
      
      const response = await axios(config);
      
      // Analyze response for ticket availability indicators
      const responseBody = response.data;
      
      // Look for common indicators of available tickets
      const availabilityIndicators = [
        'tickets available',
        'buy now',
        'add to cart',
        'select seats',
        'ticket purchase',
        '"availability":"available"',
        '"in_stock":true',
        'data-available="true"'
      ];
      
      // Look for sold out indicators (negative check)
      const soldOutIndicators = [
        'sold out',
        'out of stock',
        'not available',
        '"availability":"sold_out"',
        '"in_stock":false',
        'data-available="false"'
      ];
      
      const lowerBody = responseBody.toLowerCase();
      
      // Check if sold out first
      const isSoldOut = soldOutIndicators.some(indicator => 
        lowerBody.includes(indicator)
      );
      
      if (isSoldOut) {
        return false;
      }
      
      // Check for availability indicators
      const hasAvailableTickets = availabilityIndicators.some(indicator => 
        lowerBody.includes(indicator)
      );
      
      // Also check for ticket quantity or price information
      const ticketPattern = /(\d+)\s*tickets?\s*available/i;
      const match = responseBody.match(ticketPattern);
      
      if (match) {
        const ticketCount = parseInt(match[1], 10);
        return ticketCount > 0;
      }
      
      return hasAvailableTickets;
    } catch (error) {
      // Network errors or timeouts don't necessarily mean no tickets
      // Log the error but don't treat it as "no tickets available"
      console.warn(`Monitoring error: ${error.message}`);
      return false; // Conservative approach - assume not available on error
    }
  }

  /**
   * Detect adjacent seats in the seating map
   * Returns a list of adjacent seat pairs
   */
  async detectAdjacentSeats(page) {
    if (this.simulationMode) {
      // In simulation mode, randomly generate adjacent seat pairs
      if (Math.random() < 0.4) { // 40% chance of finding adjacent seats
        return [
          {seat1: "A15", seat2: "A16", section: "North Stand"},
          {seat1: "B22", seat2: "B23", section: "East Stand"}
        ];
      } else {
        return [];
      }
    }
    
    // In real implementation, we would:
    // 1. Parse the seating map on the page
    // 2. Identify available seats
    // 3. Find adjacent pairs (same row, consecutive numbers)
    // 4. Return list of adjacent pairs
    
    return [];
  }

  /**
   * Get the current seating map from the page
   * Returns structured seating data
   */
  async getSeatingMap(page) {
    if (this.simulationMode) {
      // Simulate a seating map
      return {
        sections: [
          {
            name: "North Stand",
            rows: ["A", "B", "C", "D"],
            availableSeats: ["A15", "A16", "B22", "B23", "C10", "C12"]
          },
          {
            name: "East Stand",
            rows: ["E", "F", "G"],
            availableSeats: ["E5", "E6", "F12", "F13"]
          }
        ]
      };
    }
    
    // In real implementation, we would:
    // 1. Extract seating information from the page
    // 2. Parse the data into a structured format
    // 3. Return the seating map
    
    return {sections: []};
  }

  /**
   * Monitor tickets continuously and notify when available
   */
  async monitorContinuously(targetUrl, proxy = null, callback, intervalMs = 5000) {
    console.log(`Starting continuous monitoring for ${targetUrl}`);
    
    while (true) {
      try {
        const isAvailable = await this.checkAvailability(targetUrl, proxy);
        
        if (isAvailable) {
          console.log('TICKETS AVAILABLE! Notifying callback...');
          if (callback) {
            callback(true);
          }
          return true; // Stop monitoring after first detection
        } else {
          console.log('No tickets available yet. Waiting...');
        }
        
        // Wait before next check
        await this.sleep(intervalMs);
      } catch (error) {
        console.error(`Monitoring error: ${error.message}`);
        // Continue monitoring despite errors
        await this.sleep(intervalMs);
      }
    }
  }

  /**
   * Parse proxy string into axios proxy configuration
   */
  parseProxy(proxyString) {
    if (!proxyString) return null;
    
    try {
      const url = new URL(proxyString);
      return {
        protocol: url.protocol.replace(':', ''),
        host: url.hostname,
        port: url.port ? parseInt(url.port, 10) : 
               url.protocol === 'https:' ? 443 : 80,
        auth: url.username ? {
          username: url.username,
          password: url.password
        } : undefined
      };
    } catch (error) {
      console.warn(`Invalid proxy format: ${proxyString}`);
      return null;
    }
  }

  /**
   * Get a random realistic user agent
   */
  getRandomUserAgent() {
    const userAgents = [
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
      'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ];
    
    return userAgents[Math.floor(Math.random() * userAgents.length)];
  }

  /**
   * Utility function to sleep for specified milliseconds
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

module.exports = { TicketMonitor };