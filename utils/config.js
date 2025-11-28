/**
 * Configuration Utility
 * Loads and manages bot configuration
 */

const fs = require('fs');
const path = require('path');

class Config {
  constructor(configPath = null) {
    this.configPath = configPath || path.join(__dirname, '..', 'config.json');
    this.config = this.loadConfig();
  }

  /**
   * Load configuration from file
   */
  loadConfig() {
    try {
      if (fs.existsSync(this.configPath)) {
        const configFile = fs.readFileSync(this.configPath, 'utf8');
        return JSON.parse(configFile);
      } else {
        console.warn(`Configuration file not found at ${this.configPath}. Using defaults.`);
        return this.getDefaultConfig();
      }
    } catch (error) {
      console.error(`Error loading configuration: ${error.message}. Using defaults.`);
      return this.getDefaultConfig();
    }
  }

  /**
   * Get default configuration
   */
  getDefaultConfig() {
    return {
      accounts: [],
      proxies: [],
      target_match_url: '',
      refresh_interval_ms: 5000,
      max_retries: 3,
      delay_between_actions_ms: 1000
    };
  }

  /**
   * Get accounts configuration
   */
  get accounts() {
    return this.config.accounts || [];
  }

  /**
   * Get proxies configuration
   */
  get proxies() {
    return this.config.proxies || [];
  }

  /**
   * Get target match URL
   */
  get target_match_url() {
    return this.config.target_match_url || '';
  }

  /**
   * Get refresh interval in milliseconds
   */
  get refresh_interval_ms() {
    return this.config.refresh_interval_ms || 5000;
  }

  /**
   * Get maximum retries
   */
  get max_retries() {
    return this.config.max_retries || 3;
  }

  /**
   * Get delay between actions in milliseconds
   */
  get delay_between_actions_ms() {
    return this.config.delay_between_actions_ms || 1000;
  }

  /**
   * Validate configuration
   */
  validate() {
    const errors = [];
    
    if (!this.accounts || this.accounts.length === 0) {
      errors.push('No accounts configured');
    }
    
    if (!this.target_match_url) {
      errors.push('No target match URL configured');
    }
    
    if (this.refresh_interval_ms < 1000) {
      errors.push('Refresh interval too short (minimum 1000ms)');
    }
    
    return {
      valid: errors.length === 0,
      errors: errors
    };
  }

  /**
   * Save configuration to file
   */
  saveConfig() {
    try {
      const configString = JSON.stringify(this.config, null, 2);
      fs.writeFileSync(this.configPath, configString, 'utf8');
      return true;
    } catch (error) {
      console.error(`Error saving configuration: ${error.message}`);
      return false;
    }
  }

  /**
   * Update configuration
   */
  update(newConfig) {
    this.config = { ...this.config, ...newConfig };
    return this.saveConfig();
  }
}

module.exports = { Config };