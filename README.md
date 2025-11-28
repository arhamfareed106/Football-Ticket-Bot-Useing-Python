# ⚽ Football Ticket Bot

An advanced automated football ticket purchasing bot with anti-detection features, multi-account support, and proxy rotation. Specifically designed for high-demand matches like Arsenal vs Tottenham, but configurable for any football match.

## 🌟 Why This Bot Stands Out

Unlike typical ticket bots, this project focuses on **real-world usability** with features that mimic human behavior to avoid detection while providing comprehensive automation. Whether you're a developer looking to learn about web automation or a fan wanting to secure tickets fairly, this bot offers both power and safety through its simulation mode.

## 🎯 Key Features

### 🔥 Advanced Automation
- **🎯 Smart Target Validation** - Ensures correct event targeting with immediate failure feedback
- **🎟️ Adjacent Seat Finder** - Sophisticated seat map analysis to locate pairs of seats together
- **🛒 Secure Basket Handling** - Adds tickets with verification to prevent checkout errors
- **💳 One-Click Checkout** - Completes purchases using saved payment methods
- **🔁 Persistent Queue Management** - Maintains position in virtual queues with heartbeat technology
- **🔐 Account-Specific Proxies** - Rotates unique proxies per account with health monitoring
- **📋 Structured Logging** - Standardized formats for easy integration with monitoring systems
- **🎭 Safe Simulation Mode** - Test all features without touching real ticketing sites

### 🏆 Core Capabilities
- **👥 Multi-Account Operation** - Run multiple membership accounts simultaneously for better chances
- **🔄 Intelligent Proxy Rotation** - Automatic switching to healthy proxies when others fail
- **⏰ Continuous Monitoring** - 24/7 scanning for ticket releases with customizable intervals
- **🕵️ Anti-Detection System** - Human-like delays and behavior patterns to avoid bot detection
- **🛡️ Robust Error Recovery** - Automatic retries and fallback mechanisms for network issues
- **🌐 Web-Based Dashboard** - Easy-to-use interface for configuration and monitoring

## 📁 Project Structure

```
football-bot/
├── modules/
│   ├── proxy_manager.js/py      # Proxy rotation and IP management
│   ├── login_manager.js/py      # Account login and session management
│   ├── queue_handler.js/py      # Virtual queue system handling
│   ├── ticket_monitor.js/py     # Ticket availability monitoring
│   └── purchase_engine.js/py    # Automated checkout and purchase
├── utils/
│   ├── config.js/py             # Configuration management
│   └── logger.js/py             # Logging utilities
├── templates/                   # Web frontend templates
│   ├── index.html
│   ├── config.html
│   └── logs.html
├── frontend.py                  # Web interface (Flask)
├── index.js / football_bot.py   # Main bot entry points
├── config.json                  # Configuration file
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies
└── README.md                    # This file
```

## ⚙️ Configuration

### Target Event Configuration
The bot enforces correct target match validation. Configure the target event in `config.json`:

```json
{
  "target_event": {
    "name": "Arsenal vs Tottenham",
    "event_id": "98765",
    "url": "https://ticketexchange.com/match/arsenal-vs-tottenham-2025-11-30"
  }
}
```

### Simulation Mode Configuration
Enable simulation mode for deterministic demo output:

```json
{
  "simulation_mode": true
}
```

### Account and Proxy Configuration
Configure accounts with unique proxies:

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
  ]
}
```

### Retry Policy Configuration
Configure retry policies for different operations:

```json
{
  "retry_policy": {
    "add_to_basket": 3,
    "checkout": 3
  }
}
```

## 🎭 Honest Simulation Mode

The bot includes a Simulation Mode that produces deterministic, richly detailed success logs for demo purposes. Simulation Mode is explicitly labeled so logs cannot be mistaken for real purchases.

### Enabling Simulation Mode
Set `"simulation_mode": true` in `config.json` to enable Simulation Mode.

### Simulation Mode Behavior
When `simulation_mode` is true, the bot runs a deterministic demo sequence (no network requests, no Playwright) and prints the exact demo output:

```
NOTE: SIMULATION MODE — This is a simulated run and NOT a real purchase.
Target match: Arsenal vs Tottenham
Checking for adjacent seats...
Pair found: Block 32, Row 10, Seats 145–146
Adding tickets 12345 & 12346 to basket...
Basket confirmed with 2 tickets
Proceeding to checkout with saved card...
Checkout successful — Order ID: #######
```

### Live Mode Behavior
When `simulation_mode` is false (live mode), the bot behaves exactly as before (requires Playwright). Live mode never prints simulated checkout success messages. If Playwright is not installed or headless browsers unavailable, it prints an informational line and aborts real checks:

```
Real mode: No ticket check performed (requires Playwright).
```

## 🚀 Quick Start

### Python Version
```bash
# Install dependencies
pip install -r requirements.txt
playwright install

# Start web frontend (recommended for testing)
python frontend.py

# Or run bot directly
python football_bot.py
```

### Node.js Version
```bash
# Install dependencies
npm install
npx playwright install

# Run bot
npm start
```

## 🎮 Web Frontend

Access the web interface at `http://localhost:5000` to:
- Configure accounts and proxies
- Enable simulation mode for safe testing
- Monitor ticket checks and bot activity
- View logs in real-time

### Simulation Mode in Web Frontend
Enable simulation mode in the web interface for safe testing without real websites:
- Produces deterministic demo output
- No network requests
- No Playwright requirements
- Safe environment to test all features

## 📊 Logging Format

The bot uses a standardized logging format for client consumption:

```
[CHECK #n] timestamp ISO8601 | target_event | match_status | pair_status | details
```

Example successful run:
```
INFO: Target match loaded: Arsenal vs Tottenham (event_id: 98765, url: https://ticketexchange.com/match/arsenal-vs-tottenham-2025-11-30)
[CHECK #221] 2025-11-21T14:29:18+05:00 | Arsenal vs Tottenham | AVAILABLE | PAIR_FOUND | A15&A16, Block: North Stand, ticket_ids:12345,12346
INFO: Adding tickets 12345,12346 to basket...
INFO: Basket contents verified: 2 tickets — A15,A16 — total price: £120.00
INFO: Payment method selected: Visa **** 4242 (saved on account)
SUCCESS: Checkout complete. Order ID: ORD-20251121-0001
```

Simulation mode indicator:
```
NOTE: SIMULATION MODE — results are simulated: success_rate=40%
```

## 🧪 Testing Scripts

### Ticket Check Demo
```bash
python test_ticket_check.py
```

### Simulation Demo
```bash
python demo_simulation.py
```

## ⚠️ Compliance Notice

This bot is for **educational and testing purposes only**. Do not use it to violate ticketing platform terms of service or engage in unfair purchasing practices.

The use of automated ticket purchasing bots may violate the Better Online Ticket Sales (BOTS) Act in the United States and similar laws in other jurisdictions. Use at your own risk and ensure compliance with all applicable laws and regulations.

## 🛡️ Anti-Detection Features

- Random delays between actions
- Human-like typing simulation
- User agent rotation
- Session maintenance
- Proxy rotation with failure tracking
- Queue position monitoring

## 🔄 Error Recovery

- Automatic retry on failed operations
- Proxy failure detection and rotation
- Session timeout handling
- Queue position recovery
- Network error resilience

## 📈 Performance Features

- **Concurrent Account Processing** - Use all accounts simultaneously
- **Smart Proxy Management** - Avoid failed proxies, track usage
- **Efficient Monitoring** - Configurable refresh intervals
- **Session Persistence** - Maintain login sessions
- **Queue Optimization** - Stay in queue without losing position

## 🛠️ Development

### Python Modules
- `football_bot.py` - Main bot controller
- `modules/ticket_monitor.py` - Ticket and seat detection
- `modules/purchase_engine.py` - Checkout and payment processing
- `modules/queue_handler.py` - Queue management
- `modules/proxy_manager.py` - Proxy rotation
- `modules/login_manager.py` - Account management
- `frontend.py` - Web interface

### Node.js Modules
- `index.js` - Main bot controller
- `modules/ticket_monitor.js` - Ticket and seat detection
- `modules/purchase_engine.js` - Checkout and payment processing
- `modules/queue_handler.js` - Queue management
- `modules/proxy_manager.js` - Proxy rotation
- `modules/login_manager.js` - Account management

## 📝 Notes

- This is a demonstration/educational tool only
- Always respect website terms of service
- Use simulation mode for testing
- Configure realistic delays to avoid detection
- Monitor logs for debugging and optimization#   F o o t b a l l - T i c k e t - B o t - U s e i n g - P y t h o n  
 