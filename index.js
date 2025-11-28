/**
 * Main entry point for the Football Ticket Bot
 * This bot automates the process of monitoring and purchasing football tickets
 * with anti-detection features and multi-account support
 * Specifically targets Arsenal vs Tottenham match
 */

const fs = require('fs');
const path = require('path');

// Import bot modules
const { ProxyManager } = require('./modules/proxy_manager');
const { LoginManager } = require('./modules/login_manager');
const { QueueHandler } = require('./modules/queue_handler');
const { TicketMonitor } = require('./modules/ticket_monitor');
const { PurchaseEngine } = require('./modules/purchase_engine');
const { Logger } = require('./utils/logger');
const { Config } = require('./utils/config');

class FootballTicketBot {
  constructor() {
    this.config = new Config();
    this.logger = new Logger();
    this.proxyManager = new ProxyManager(this.config.proxies);
    this.loginManager = new LoginManager(this.proxyManager);
    this.queueHandler = new QueueHandler(this.proxyManager);
    this.ticketMonitor = new TicketMonitor();
    this.purchaseEngine = new PurchaseEngine(this.proxyManager);
    
    this.accounts = this.config.accounts;
    this.targetMatchUrl = this.config.target_match_url;
    this.isRunning = false;
  }

  /**
   * Initialize the bot and all its components
   */
  async initialize() {
    this.logger.info('Initializing Football Ticket Bot for Arsenal vs Tottenham...');
    
    try {
      // Initialize Playwright browsers for each account
      await this.loginManager.initializeBrowsers();
      
      // Validate configuration
      if (!this.accounts || this.accounts.length === 0) {
        throw new Error('No accounts configured');
      }
      
      if (!this.targetMatchUrl) {
        throw new Error('No target match URL configured');
      }
      
      this.logger.info(`Bot initialized with ${this.accounts.length} accounts`);
      this.logger.info('Targeting match: Arsenal vs Tottenham');
      return true;
    } catch (error) {
      this.logger.error(`Failed to initialize bot: ${error.message}`);
      return false;
    }
  }

  /**
   * Main bot execution loop
   */
  async run() {
    this.isRunning = true;
    this.logger.info('Starting Football Ticket Bot for Arsenal vs Tottenham...');
    
    while (this.isRunning) {
      try {
        // Monitor for ticket availability
        const ticketsAvailable = await this.ticketMonitor.checkAvailability(
          this.targetMatchUrl,
          this.proxyManager.getRandomProxy()
        );
        
        if (ticketsAvailable) {
          this.logger.info('Arsenal vs Tottenham tickets detected! Initiating purchase process...');
          
          // Attempt purchase with all accounts
          const purchaseResult = await this.attemptPurchase();
          
          if (purchaseResult.success) {
            this.logger.info('Purchase successful for Arsenal vs Tottenham tickets!');
            // Optionally stop the bot after successful purchase
            // this.stop();
          } else {
            this.logger.warn(`Purchase failed: ${purchaseResult.error}`);
          }
        } else {
          this.logger.info('No Arsenal vs Tottenham tickets available yet. Waiting...');
        }
        
        // Wait before next check
        await this.sleep(this.config.refresh_interval_ms);
      } catch (error) {
        this.logger.error(`Error in main loop: ${error.message}`);
        await this.sleep(5000); // Wait 5 seconds before retrying
      }
    }
  }

  /**
   * Attempt to purchase tickets using all configured accounts
   */
  async attemptPurchase() {
    try {
      // Login to all accounts
      const loggedInAccounts = [];
      for (const account of this.accounts) {
        try {
          const loginResult = await this.loginManager.login(account);
          if (loginResult.success) {
            loggedInAccounts.push({
              ...account,
              browser: loginResult.browser,
              page: loginResult.page
            });
            this.logger.info(`Successfully logged in as ${account.username}`);
          } else {
            this.logger.warn(`Failed to login as ${account.username}: ${loginResult.error}`);
          }
        } catch (error) {
          this.logger.error(`Error logging in as ${account.username}: ${error.message}`);
        }
      }
      
      if (loggedInAccounts.length === 0) {
        return { success: false, error: 'Failed to login to any accounts' };
      }
      
      // Enter queue with all accounts
      const queuedAccounts = [];
      for (const account of loggedInAccounts) {
        try {
          const queueResult = await this.queueHandler.enterQueue(
            account.page,
            this.targetMatchUrl
          );
          
          if (queueResult.success) {
            queuedAccounts.push(account);
            this.logger.info(`${account.username} entered queue successfully`);
          } else {
            this.logger.warn(`${account.username} failed to enter queue: ${queueResult.error}`);
          }
        } catch (error) {
          this.logger.error(`Error entering queue for ${account.username}: ${error.message}`);
        }
      }
      
      if (queuedAccounts.length === 0) {
        return { success: false, error: 'Failed to enter queue with any accounts' };
      }
      
      // Wait in queue for access
      const accountsWithAccess = [];
      for (const account of queuedAccounts) {
        try {
          const accessResult = await this.queueHandler.waitForAccess(account.page);
          
          if (accessResult.success) {
            accountsWithAccess.push(account);
            this.logger.info(`${account.username} gained access to ticket purchase`);
          } else {
            this.logger.warn(`${account.username} did not gain access: ${accessResult.error}`);
          }
        } catch (error) {
          this.logger.error(`Error waiting for access for ${account.username}: ${error.message}`);
        }
      }
      
      if (accountsWithAccess.length === 0) {
        return { success: false, error: 'No accounts gained access to purchase' };
      }
      
      // Attempt purchase with accounts that gained access
      let purchaseSuccess = false;
      let purchaseError = null;
      
      for (const account of accountsWithAccess) {
        try {
          // Purchase 2 adjacent tickets for Arsenal vs Tottenham
          const purchaseResult = await this.purchaseEngine.purchaseAdjacentTickets(
            account.page,
            2 // Number of adjacent tickets
          );
          
          if (purchaseResult.success) {
            purchaseSuccess = true;
            this.logger.info(`Successfully purchased 2 adjacent tickets with account ${account.username}`);
            break; // Stop after successful purchase
          } else {
            purchaseError = purchaseResult.error;
            this.logger.warn(`Purchase failed with account ${account.username}: ${purchaseResult.error}`);
          }
        } catch (error) {
          this.logger.error(`Error purchasing with account ${account.username}: ${error.message}`);
        }
      }
      
      // Clean up browser sessions
      for (const account of loggedInAccounts) {
        try {
          await this.loginManager.logout(account);
        } catch (error) {
          this.logger.error(`Error logging out account ${account.username}: ${error.message}`);
        }
      }
      
      return {
        success: purchaseSuccess,
        error: purchaseSuccess ? null : purchaseError
      };
    } catch (error) {
      this.logger.error(`Error in purchase attempt: ${error.message}`);
      return { success: false, error: error.message };
    }
  }

  /**
   * Stop the bot execution
   */
  stop() {
    this.isRunning = false;
    this.logger.info('Stopping Football Ticket Bot...');
    this.loginManager.closeAllBrowsers();
  }

  /**
   * Utility function to sleep for specified milliseconds
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Run the bot if this file is executed directly
if (require.main === module) {
  const bot = new FootballTicketBot();
  
  // Handle graceful shutdown
  process.on('SIGINT', () => {
    console.log('\nReceived SIGINT. Shutting down gracefully...');
    bot.stop();
    process.exit(0);
  });
  
  process.on('SIGTERM', () => {
    console.log('\nReceived SIGTERM. Shutting down gracefully...');
    bot.stop();
    process.exit(0);
  });
  
  // Initialize and start the bot
  bot.initialize().then(success => {
    if (success) {
      bot.run().catch(error => {
        console.error('Fatal error in bot execution:', error);
        bot.stop();
        process.exit(1);
      });
    } else {
      console.error('Failed to initialize bot. Exiting.');
      process.exit(1);
    }
  });
}

module.exports = { FootballTicketBot };