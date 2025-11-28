# Football Ticket Bot (Python Version)

An automated football ticket buying bot with anti-detection features, multi-account support, and proxy rotation.

## ⚠️ DISCLAIMER

This bot is provided strictly for **educational and testing purposes only**. Unauthorized use of automated bots to purchase tickets may violate terms of service of ticketing platforms and could result in account bans or legal consequences. Use at your own risk.

## Features

1. **Ticket Monitoring** - Continuously monitors official ticket exchanges for new listings
2. **Multi-Account Support** - Uses multiple membership accounts simultaneously
3. **Queue Handling** - Automatically enters and waits in virtual queues
4. **Proxy Rotation** - Implements residential/rotating proxies for anonymity
5. **Automated Checkout** - Completes the entire purchase flow automatically
6. **Anti-Detection** - Uses Playwright with human-like behavior simulation
7. **Error Recovery** - Robust retry mechanisms and session restoration
8. **Comprehensive Logging** - Detailed logs of all bot activities

## Technical Architecture

```
football-ticket-bot/
├── config.json          # Configuration file
├── football_bot.py      # Main bot entry point
├── requirements.txt     # Python dependencies
├── README_PYTHON.md     # Python setup and usage instructions
├── modules/
│   ├── __init__.py           # Package initializer
│   ├── login_manager.py      # Account authentication
│   ├── proxy_manager.py      # Proxy rotation system
│   ├── queue_handler.py      # Virtual queue management
│   ├── ticket_monitor.py     # Ticket availability monitoring
│   └── purchase_engine.py    # Automated purchase workflow
├── utils/
│   ├── __init__.py           # Package initializer
│   ├── config.py             # Configuration loader
│   └── logger.py             # Logging utility
└── logs/
    └── bot.log              # Activity logs
```

## Prerequisites

- Python 3.7 or higher
- pip (Python Package Installer)
- Valid accounts on the target ticket exchange
- Residential or rotating proxy service

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```bash
   playwright install
   ```

## Configuration

1. Edit `config.json` with your account details:
   ```json
   {
     "accounts": [
       {
         "username": "your_main_account",
         "password": "your_password"
       },
       {
         "username": "your_linked_account",
         "password": "your_password"
       }
     ],
     "proxies": [
       "http://proxy1:port",
       "http://proxy2:port"
     ],
     "target_match_url": "https://official-ticket-exchange.com/match/12345",
     "refresh_interval_ms": 5000,
     "max_retries": 3,
     "delay_between_actions_ms": 1000
   }
   ```

## Proxy Setup

1. Subscribe to a residential proxy service (recommended providers):
   - BrightData
   - Oxylabs
   - SmartProxy

2. Configure proxies in `config.json`:
   ```json
   "proxies": [
     "http://username:password@proxy-server:port",
     "http://username:password@proxy-server:port"
   ]
   ```

## Running the Bot

Start the bot with:
```bash
python football_bot.py
```

## How It Works

1. **Initialization**: Loads configuration and validates settings
2. **Monitoring**: Continuously checks for ticket availability
3. **Detection**: Instantly reacts when tickets are detected
4. **Authentication**: Logs into all configured accounts using proxies
5. **Queue Management**: Enters and waits in virtual queues
6. **Purchase**: Automatically selects adjacent seats and completes checkout
7. **Logging**: Records all activities and errors

## Anti-Detection Features

- Playwright browser automation
- Human-like mouse movements and typing
- Random delays between actions
- Rotating user agents and headers
- Cookie persistence
- Rate limiting control
- Proxy rotation per request

## Error Handling

- Auto re-login on session expiration
- Queue position recovery
- Proxy retry system
- Graceful handling of blocked requests
- Comprehensive error logging

## Customization

Modify the bot behavior by adjusting values in `config.json`:
- `refresh_interval_ms`: How often to check for tickets
- `max_retries`: Number of retry attempts for failed operations
- `delay_between_actions_ms`: Delay between automated actions

## Troubleshooting

1. **Installation Issues**:
   - Ensure Python 3.7+ is properly installed
   - Run `pip install -r requirements.txt` in the project directory

2. **Browser Issues**:
   - Run `playwright install` to install browsers

3. **Proxy Issues**:
   - Verify proxy format in config.json
   - Test proxies with external tools

4. **Login Issues**:
   - Check account credentials
   - Some sites may require CAPTCHA solving

## Legal Notice

Use of this bot may violate the terms of service of ticketing platforms. The developers are not responsible for any consequences arising from the use of this software. This tool is intended for educational purposes only.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.