/**
 * Logger Utility
 * Handles logging for the football ticket bot
 */

const fs = require('fs');
const path = require('path');

class Logger {
  constructor(logToFile = true) {
    this.logToFile = logToFile;
    this.logFilePath = path.join(__dirname, '..', 'logs', 'bot.log');
    
    // Create logs directory if it doesn't exist
    const logsDir = path.join(__dirname, '..', 'logs');
    if (!fs.existsSync(logsDir)) {
      fs.mkdirSync(logsDir, { recursive: true });
    }
  }

  /**
   * Log an info message
   */
  info(message) {
    this.log('INFO', message);
  }

  /**
   * Log a warning message
   */
  warn(message) {
    this.log('WARN', message);
  }

  /**
   * Log an error message
   */
  error(message) {
    this.log('ERROR', message);
  }

  /**
   * Log a debug message
   */
  debug(message) {
    this.log('DEBUG', message);
  }

  /**
   * Generic log function
   */
  log(level, message) {
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] [${level}] ${message}`;
    
    // Log to console
    console.log(logMessage);
    
    // Log to file if enabled
    if (this.logToFile) {
      this.writeToFile(logMessage);
    }
  }

  /**
   * Write log message to file
   */
  writeToFile(message) {
    try {
      const logLine = `${message}\n`;
      fs.appendFileSync(this.logFilePath, logLine);
    } catch (error) {
      // Don't let logging errors crash the application
      console.error(`Failed to write to log file: ${error.message}`);
    }
  }

  /**
   * Get the path to the log file
   */
  getLogFilePath() {
    return this.logFilePath;
  }
}

module.exports = { Logger };