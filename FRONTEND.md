# Football Ticket Bot Frontend

A simple web interface for the Football Ticket Bot built with Flask.

## Features

- **Dashboard**: Overview of bot status and statistics
- **Configuration**: Web-based configuration management
- **Logs**: Real-time activity monitoring
- **Bot Control**: Start/stop functionality

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the frontend:
   ```bash
   python frontend.py
   ```

3. Access the web interface at http://localhost:5000

## Pages

### Dashboard
- Shows bot status (Running/Stopped)
- Displays account and proxy counts
- Shows recent activity logs
- Provides start/stop controls

### Configuration
- Edit target match URL
- Configure refresh intervals
- Manage account credentials
- Add/remove proxy servers

### Logs
- View detailed bot activity
- Auto-refresh every 5 seconds
- Manual refresh option

## API Endpoints

- `GET /api/status` - Get bot status
- `POST /api/start` - Start the bot
- `POST /api/stop` - Stop the bot
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration
- `GET /api/logs` - Get activity logs

## Security Note

⚠️ This frontend is for development purposes only. Do not expose it to public networks without proper authentication and security measures.

## Usage

1. Navigate to http://localhost:5000
2. Configure accounts and proxies in the Configuration page
3. Set your target match URL
4. Start the bot from the Dashboard
5. Monitor activity in the Logs page