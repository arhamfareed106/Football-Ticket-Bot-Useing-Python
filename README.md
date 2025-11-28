# ⚽ Football Ticket Bot

An advanced automated football ticket purchasing bot with anti-detection features, multi-account support, and proxy rotation. Specifically designed for high-demand matches like Arsenal vs Tottenham, but configurable for any football match.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue" alt="Python 3.7+" />
  <img src="https://img.shields.io/badge/Node.js-LTS-brightgreen" alt="Node.js LTS" />
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License" />
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue" alt="Cross Platform" />
</p>

## 📚 Table of Contents

- [Why This Bot Stands Out](#-why-this-bot-stands-out)
- [Key Features](#-key-features)
- [Architecture Overview](#-architecture-overview)
- [Configuration Guide](#-configuration-guide)
- [Safe Simulation Mode](#-safe-simulation-mode)
- [Quick Start Guide](#-quick-start-guide)
- [Web Dashboard Features](#-web-dashboard-features)
- [Advanced Anti-Detection Features](#-advanced-anti-detection-features)
- [Intelligent Proxy Management](#-intelligent-proxy-management)
- [Robust Error Recovery](#-robust-error-recovery)
- [Testing & Development](#-testing--development)
- [Compliance Notice](#-compliance-notice)
- [Development Information](#-development-information)

## 🌟 Why This Bot Stands Out

Unlike typical ticket bots, this project focuses on real-world usability with features that mimic human behavior to avoid detection while providing comprehensive automation. Whether you're a developer looking to learn about web automation or a fan wanting to secure tickets fairly, this bot offers both power and safety through its simulation mode.

## 🎯 Key Features

### 🔥 Advanced Automation

* Smart Target Validation
* Adjacent Seat Finder
* Secure Basket Handling
* One-Click Checkout
* Persistent Queue Management
* Account-Specific Proxies
* Structured Logging
* Safe Simulation Mode

### 🏆 Core Capabilities

* Multi-Account Operation
* Intelligent Proxy Rotation
* Continuous Monitoring
* Anti-Detection System
* Robust Error Recovery
* Web-Based Dashboard
* Dual-Stack Implementation (Python & Node.js)
* Modular Architecture

## 🏗️ Architecture Overview

This bot features a modular, dual-stack architecture supporting both Python and Node.js implementations:

```
football-ticket-bot/
├── modules/                 # Core functionality modules
│   ├── proxy_manager.py     # Proxy rotation and IP management
│   ├── login_manager.py     # Account authentication system
│   ├── queue_handler.py     # Virtual queue management
│   ├── ticket_monitor.py    # Ticket availability monitoring
│   └── purchase_engine.py   # Automated checkout process
├── utils/                   # Utility modules
│   ├── config.py            # Configuration management
│   └── logger.py            # Structured logging system
├── templates/               # Web dashboard templates
│   ├── index.html           # Main dashboard
│   ├── config.html          # Configuration page
│   └── logs.html            # Activity logs page
├── frontend.py              # Web dashboard (Flask)
├── football_bot.py          # Main Python bot
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
└── package.json             # Node.js dependencies
```

## ⚙️ Configuration Guide

The bot is configured through a single `config.json` file that controls all aspects of its operation:

### Target Event Configuration

```json
{
  "target_event": {
    "name": "Arsenal vs Tottenham",
    "event_id": "98765",
    "url": "https://ticketexchange.com/match/arsenal-vs-tottenham-2025-11-30"
  }
}
```

### Account and Proxy Configuration

```json
{
  "accounts": [
    {
      "username": "arsenal_fan@gmail.com",
      "password": "Gunners2025!",
      "proxy": "http://45.76.23.12:8000"
    },
    {
      "username": "spurs_supporter@gmail.com",
      "password": "ComeOnYouSpurs!",
      "proxy": "http://52.18.99.10:8000"
    }
  ],
  "proxies": [
    "http://45.76.23.12:8000",
    "http://52.18.99.10:8000"
  ]
}
```

### Performance & Retry Configuration

```json
{
  "refresh_interval_ms": 3000,
  "max_retries": 3,
  "delay_between_actions_ms": 500,
  "retry_policy": {
    "add_to_basket": 3,
    "checkout": 3
  },
  "simulation_mode": true
}
```

## 🎮 Safe Simulation Mode

Before risking real purchases, test the bot in Simulation Mode which produces deterministic demo logs without interacting with real websites.

### Web Dashboard Visualization

<p align="center">
  <img src="https://placehold.co/600x300/2c3e50/ffffff?text=Football+Ticket+Bot+Dashboard" alt="Web Dashboard" />
  <br />
  <em>Web-based dashboard for monitoring and controlling the bot</em>
</p>

### Demo Output Example

```
NOTE: SIMULATION MODE — This is a simulated run.
Target match: Arsenal vs Tottenham
Checking for adjacent seats...
Pair found: Block 32, Row 10, Seats 145–146
Adding tickets 12345 & 12346 to basket...
Basket confirmed with 2 tickets
Proceeding to checkout...
Checkout successful — Order ID: #######
```

## 🚀 Quick Start Guide

### Python Version

1. Install dependencies:
```bash
pip install -r requirements.txt
playwright install
```

2. Configure the bot by editing `config.json`

3. Start the web dashboard:
```bash
python frontend.py
```

4. In a new terminal, run the bot:
```bash
python football_bot.py
```

### Node.js Version

1. Install dependencies:
```bash
npm install
npx playwright install
```

2. Configure the bot by editing `config.json`

3. Start the bot:
```bash
npm start
```

### Accessing the Web Interface

Once the frontend is running, access the dashboard at `http://localhost:5000` to monitor activity, configure settings, and control the bot.

## 🌐 Web Dashboard Features

The bot includes a comprehensive web dashboard for easy monitoring and control:

* **Real-time Status Monitoring** - Track bot activity and performance
* **Configuration Management** - Edit settings through a user-friendly interface
* **Activity Logs** - View detailed logs of all bot actions
* **Simulation Toggle** - Switch between safe simulation and live mode
* **Manual Ticket Checks** - Trigger immediate availability checks
* **Account Statistics** - Monitor account and proxy usage

## 🛡️ Advanced Anti-Detection Features

To avoid detection by ticketing platforms, the bot implements multiple human-like behaviors:

* **Human-like Delays** - Randomized wait times between actions (100ms-1500ms)
* **Realistic Typing Simulation** - Variable speed typing with natural pauses
* **User Agent Rotation** - Rotates through realistic browser user agents
* **Proxy Rotation** - IP diversity through configurable proxy lists
* **Cookie Persistence** - Maintains session cookies like a real browser
* **Mouse Movement Simulation** - Natural cursor movements and click patterns
* **Rate Limiting** - Controls request frequency to avoid suspicion
* **CAPTCHA Handling** - Manual or automated CAPTCHA resolution

## 🔧 Intelligent Proxy Management

The bot features sophisticated proxy handling to maximize success rates:

* **Account-Specific Proxies** - Each account uses a dedicated proxy
* **Health Monitoring** - Automatic detection of failed proxies
* **Automatic Rotation** - Seamless switching to backup proxies
* **Usage Tracking** - Statistics on proxy performance
* **Residential Support** - Compatible with residential proxy services

## 🔄 Robust Error Recovery

Built-in resilience ensures the bot can handle various failure scenarios:

* **Auto Re-login** - Restores sessions after expiration
* **Queue Restoration** - Maintains position after connection issues
* **Proxy Retry System** - Fallback mechanisms for proxy failures
* **Purchase Reattempts** - Multiple attempts with different accounts
* **Session Management** - Persistent cookies and authentication
* **Comprehensive Logging** - Detailed records of all activities and errors

## 🧪 Testing & Development

Several test scripts are included for development and verification:

* `python test_ticket_check.py` - Test ticket detection algorithms
* `python demo_simulation.py` - Run simulation mode demonstration
* `python test_full_flow.py` - Test complete purchase workflow
* `python simple_demo.py` - Quick demo without dependencies

## ⚠️ Compliance Notice

This bot is provided for educational and testing purposes only. Unauthorized use of automated bots to purchase tickets may violate terms of service of ticketing platforms and could result in account bans or legal consequences. Use at your own risk.

## 🛠️ Development Information

The project supports both Python and Node.js implementations with a modular architecture:

* **Language**: Python 3.7+ / Node.js
* **Framework**: Playwright for browser automation
* **Architecture**: Modular with async/await
* **Dependencies**: requests, playwright (Python) / axios, playwright (Node.js)
* **Configuration**: JSON-based settings

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

