/**
 * Login Manager Module
 * Handles account authentication and browser session management
 */

const { chromium } = require('playwright');

class LoginManager {
  constructor(proxyManager) {
    this.proxyManager = proxyManager;
    this.browsers = new Map(); // Store browser instances by account username
    this.pages = new Map(); // Store page instances by account username
  }

  /**
   * Initialize Playwright browsers for all accounts
   */
  async initializeBrowsers() {
    // We'll create browsers on-demand for each login attempt
    // This approach is more memory-efficient
  }

  /**
   * Login to an account using Playwright with anti-detection measures
   */
  async login(account) {
    try {
      // Get a proxy for this account
      const proxy = this.proxyManager.getNextProxy();
      
      // Configure browser with anti-detection settings
      const browserOptions = {
        headless: false, // Set to true for production
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-blink-features=AutomationControlled',
          '--disable-extensions',
          '--disable-plugins',
          '--disable-images',
          '--disable-javascript', // Enable JavaScript when needed
        ]
      };
      
      // Add proxy if available
      if (proxy) {
        browserOptions.proxy = {
          server: proxy
        };
      }
      
      // Create a new browser instance
      const browser = await chromium.launch(browserOptions);
      
      // Create a new page
      const page = await browser.newPage();
      
      // Set realistic viewport size
      await page.setViewportSize({
        width: 1366,
        height: 768
      });
      
      // Set realistic user agent
      await page.setUserAgent(this.getRandomUserAgent());
      
      // Set realistic headers
      await page.setExtraHTTPHeaders({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
      });
      
      // Navigate to login page
      await page.goto('https://official-ticket-exchange.com/login', {
        waitUntil: 'networkidle'
      });
      
      // Add some human-like delays
      await this.randomDelay(1000, 2000);
      
      // Fill in credentials with human-like typing
      await this.humanType(page, '#username', account.username);
      await this.randomDelay(500, 1000);
      await this.humanType(page, '#password', account.password);
      await this.randomDelay(500, 1000);
      
      // Click login button
      await page.click('#login-button');
      
      // Wait for navigation or error
      await Promise.race([
        page.waitForNavigation({ waitUntil: 'networkidle' }),
        page.waitForSelector('.error-message', { timeout: 10000 })
      ]);
      
      // Check if login was successful
      const isLoggedIn = await this.checkLoginStatus(page);
      
      if (isLoggedIn) {
        // Store browser and page for this account
        this.browsers.set(account.username, browser);
        this.pages.set(account.username, page);
        
        return {
          success: true,
          browser: browser,
          page: page
        };
      } else {
        // Close browser on failed login
        await browser.close();
        return {
          success: false,
          error: 'Login failed - invalid credentials or captcha required'
        };
      }
    } catch (error) {
      return {
        success: false,
        error: `Login error: ${error.message}`
      };
    }
  }

  /**
   * Check if the current page shows a successful login
   */
  async checkLoginStatus(page) {
    try {
      // Look for elements that indicate successful login
      const dashboardElement = await page.$('.dashboard, .user-profile, .account-menu');
      const logoutButton = await page.$('a[href*="logout"], button.logout');
      
      return !!dashboardElement || !!logoutButton;
    } catch (error) {
      return false;
    }
  }

  /**
   * Logout from an account
   */
  async logout(account) {
    try {
      const page = this.pages.get(account.username);
      const browser = this.browsers.get(account.username);
      
      if (page) {
        // Try to navigate to logout URL
        await page.goto('https://official-ticket-exchange.com/logout', {
          waitUntil: 'networkidle'
        }).catch(() => {}); // Ignore errors
        
        this.pages.delete(account.username);
      }
      
      if (browser) {
        await browser.close();
        this.browsers.delete(account.username);
      }
      
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Close all browser instances
   */
  async closeAllBrowsers() {
    for (const [username, browser] of this.browsers) {
      try {
        await browser.close();
      } catch (error) {
        // Ignore errors when closing
      }
    }
    
    this.browsers.clear();
    this.pages.clear();
  }

  /**
   * Simulate human-like typing with random delays
   */
  async humanType(page, selector, text) {
    await page.focus(selector);
    
    for (const char of text) {
      await page.type(selector, char, { delay: this.randomInt(50, 150) });
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
}

module.exports = { LoginManager };