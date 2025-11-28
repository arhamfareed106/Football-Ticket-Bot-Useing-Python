/**
 * Proxy Manager Module
 * Handles proxy rotation and IP management for multiple accounts
 */

class ProxyManager {
  constructor(proxyList) {
    this.proxyList = proxyList || [];
    this.proxyUsageCount = {};
    this.failedProxies = new Set();
    // Check if we're in simulation mode
    this.simulationMode = process.env.BOT_SIMULATION === 'true';
  }

  /**
   * Get a random proxy from the list, avoiding failed proxies
   */
  getRandomProxy() {
    if (this.simulationMode || this.proxyList.length === 0) {
      return null;
    }
    
    // Filter out failed proxies
    const availableProxies = this.proxyList.filter(p => !this.failedProxies.has(p));
    
    if (availableProxies.length === 0) {
      console.warn("No available proxies - all proxies marked as failed");
      return null;
    }
    
    // Select random proxy
    const proxy = availableProxies[Math.floor(Math.random() * availableProxies.length)];
    
    // Track usage
    this.proxyUsageCount[proxy] = (this.proxyUsageCount[proxy] || 0) + 1;
    console.log(`Using proxy: ${proxy} (used ${this.proxyUsageCount[proxy]} times)`);
    
    return proxy;
  }

  /**
   * Get a specific proxy for an account (round-robin style)
   */
  getProxyForAccount(accountIndex) {
    if (this.simulationMode || this.proxyList.length === 0) {
      return null;
    }
    
    // Filter out failed proxies
    const availableProxies = this.proxyList.filter(p => !this.failedProxies.has(p));
    
    if (availableProxies.length === 0) {
      console.warn("No available proxies for account");
      return null;
    }
    
    // Assign proxy based on account index
    const proxyIndex = accountIndex % availableProxies.length;
    const proxy = availableProxies[proxyIndex];
    
    // Track usage
    this.proxyUsageCount[proxy] = (this.proxyUsageCount[proxy] || 0) + 1;
    console.log(`Assigned proxy to account ${accountIndex}: ${proxy}`);
    
    return proxy;
  }

  /**
   * Mark a proxy as failed to avoid using it again
   */
  markProxyFailed(proxy) {
    if (proxy) {
      this.failedProxies.add(proxy);
      console.warn(`Proxy marked as failed: ${proxy}`);
    }
  }

  /**
   * Reset the failed proxies list (useful for retrying)
   */
  resetFailedProxies() {
    const failedCount = this.failedProxies.size;
    this.failedProxies.clear();
    console.log(`Reset ${failedCount} failed proxies`);
  }

  /**
   * Get statistics about proxy usage
   */
  getProxyStats() {
    return {
      totalProxies: this.proxyList.length,
      availableProxies: this.proxyList.filter(p => !this.failedProxies.has(p)).length,
      failedProxies: this.failedProxies.size,
      usageCounts: this.proxyUsageCount
    };
  }

  /**
   * Add a new proxy to the list
   */
  addProxy(proxy) {
    if (proxy && !this.proxyList.includes(proxy)) {
      this.proxyList.push(proxy);
    }
  }

  /**
   * Remove a proxy from the list
   */
  removeProxy(proxy) {
    const index = this.proxyList.indexOf(proxy);
    if (index > -1) {
      this.proxyList.splice(index, 1);
      this.failedProxies.delete(proxy);
    }
  }

  /**
   * Get all proxies
   */
  getAllProxies() {
    return [...this.proxyList]; // Return a copy
  }

  /**
   * Check if any proxies are configured
   */
  hasProxies() {
    return this.proxyList.length > 0;
  }

  /**
   * Validate a proxy string format
   */
  static isValidProxy(proxyString) {
    if (!proxyString) return false;
    
    // Simple validation for http/https proxies
    const httpRegex = /^https?:\/\/[\w.-]+(:\d+)?$/;
    return httpRegex.test(proxyString);
  }
}

module.exports = { ProxyManager };