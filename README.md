# ⚽ Football Ticket Bot

An advanced automated football ticket purchasing bot with anti-detection features, multi-account support, and proxy rotation. Specifically designed for high-demand matches like Arsenal vs Tottenham, but configurable for any football match.

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

## 📁 Project Structure

```
football-bot/
├── modules/
│   ├── proxy_manager.js/py
│   ├── login_manager.js/py
│   ├── queue_handler.js/py
│   ├── ticket_monitor.js/py
│   └── purchase_engine.js/py
├── utils/
│   ├── config.js/py
│   └── logger.js/py
├── templates/
│   ├── index.html
│   ├── config.html
│   └── logs.html
├── frontend.py
├── index.js / football_bot.py
├── config.json
├── requirements.txt
├── package.json
└── README.md
```

## ⚙️ Configuration

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

### Simulation Mode Configuration

```json
{
  "simulation_mode": true
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
  ]
}
```

### Retry Policy Configuration

```json
{
  "retry_policy": {
    "add_to_basket": 3,
    "checkout": 3
  }
}
```

## 🎭 Honest Simulation Mode

Simulation Mode produces deterministic demo logs without interacting with real websites.

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

## 🚀 Quick Start

### Python Version

```bash
pip install -r requirements.txt
playwright install
python frontend.py
python football_bot.py
```

### Node.js Version

```bash
npm install
npx playwright install
npm start
```

## 🎮 Web Frontend

Access the dashboard at `http://localhost:5000`.

## 📊 Logging Format

```
[CHECK #n] timestamp | event | match_status | pair_status | details
```

## 🧪 Testing Scripts

* `python test_ticket_check.py`
* `python demo_simulation.py`

## ⚠️ Compliance Notice

This bot is for educational and testing purposes only.

## 🛡️ Anti-Detection Features

* Human-like delays
* Typing simulation
* User agent rotation
* Proxy rotation

## 🔄 Error Recovery

* Retry logic
* Proxy failure handling
* Session timeout recovery

## 📈 Performance Features

* Concurrent accounts
* Smart proxy tracking
* Efficient monitoring

## 🛠️ Development

Supports both Python and Node.js implementations.
