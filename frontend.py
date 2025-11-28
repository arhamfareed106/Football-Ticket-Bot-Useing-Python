"""
Simple web frontend for the Football Ticket Bot
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
import random
from pathlib import Path
import time

# Import our bot modules
from utils.config import Config
from modules.proxy_manager import ProxyManager

app = Flask(__name__)

# Global variables to store bot state
bot_config = Config()
bot_status = "Stopped"
bot_logs = []
simulation_mode = bot_config.simulation_mode
ticket_check_results = []  # Store ticket check results
check_counter = 0  # Counter for unique check numbers

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', 
                         config=bot_config,
                         status=bot_status,
                         logs=bot_logs[-10:],
                         simulation_mode=simulation_mode,
                         ticket_checks=ticket_check_results[-5:])  # Show last 5 ticket checks

@app.route('/config')
def config_page():
    """Configuration page"""
    return render_template('config.html', config=bot_config, simulation_mode=simulation_mode)

@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """API endpoint for configuration"""
    global bot_config
    
    if request.method == 'POST':
        try:
            # Update config with posted data
            data = request.get_json()
            
            # Update target event
            if 'target_event' in data:
                bot_config.config['target_event'] = data['target_event']
            
            # Update accounts
            if 'accounts' in data:
                bot_config.config['accounts'] = data['accounts']
            
            # Update proxies
            if 'proxies' in data:
                bot_config.config['proxies'] = data['proxies']
            
            # Update other settings
            for key in ['refresh_interval_ms', 'max_retries', 'delay_between_actions_ms', 'retry_policy', 'simulation_mode']:
                if key in data:
                    bot_config.config[key] = data[key]
            
            # Save config
            bot_config.save_config()
            
            bot_logs.append("Configuration updated successfully")
            return jsonify({'success': True, 'message': 'Configuration updated successfully'})
        except Exception as e:
            bot_logs.append(f"Error updating configuration: {str(e)}")
            return jsonify({'success': False, 'message': f'Error updating configuration: {str(e)}'})
    
    else:
        # Return current config
        return jsonify(bot_config.config)

@app.route('/api/start', methods=['POST'])
def api_start_bot():
    """API endpoint to start the bot"""
    global bot_status, bot_logs, simulation_mode
    
    try:
        # Update simulation mode from config
        simulation_mode = bot_config.simulation_mode
        
        # Set simulation mode environment variable
        if simulation_mode:
            os.environ['BOT_SIMULATION'] = 'true'
        else:
            os.environ['BOT_SIMULATION'] = 'false'
        
        # In a real implementation, this would start the bot
        bot_status = "Running"
        target_event = bot_config.target_event
        bot_logs.append(f"Bot started successfully for {target_event['name']}")
        if simulation_mode:
            bot_logs.append("⚠️ Simulation mode enabled")
        return jsonify({'success': True, 'message': 'Bot started successfully', 'status': bot_status})
    except Exception as e:
        bot_logs.append(f"Error starting bot: {str(e)}")
        return jsonify({'success': False, 'message': f'Error starting bot: {str(e)}'})

@app.route('/api/stop', methods=['POST'])
def api_stop_bot():
    """API endpoint to stop the bot"""
    global bot_status, bot_logs
    
    try:
        # In a real implementation, this would stop the bot
        bot_status = "Stopped"
        bot_logs.append("Bot stopped successfully")
        return jsonify({'success': True, 'message': 'Bot stopped successfully', 'status': bot_status})
    except Exception as e:
        bot_logs.append(f"Error stopping bot: {str(e)}")
        return jsonify({'success': False, 'message': f'Error stopping bot: {str(e)}'})

@app.route('/api/simulation', methods=['POST'])
def api_toggle_simulation():
    """API endpoint to toggle simulation mode"""
    global simulation_mode, bot_logs
    
    try:
        data = request.get_json()
        simulation_mode = data.get('enabled', False)
        
        # Update config
        bot_config.config['simulation_mode'] = simulation_mode
        bot_config.save_config()
        
        if simulation_mode:
            bot_logs.append("Simulation mode enabled")
        else:
            bot_logs.append("Simulation mode disabled")
            
        return jsonify({'success': True, 'message': f'Simulation mode {"enabled" if simulation_mode else "disabled"}', 'simulation_mode': simulation_mode})
    except Exception as e:
        bot_logs.append(f"Error toggling simulation mode: {str(e)}")
        return jsonify({'success': False, 'message': f'Error toggling simulation mode: {str(e)}'})

@app.route('/api/ticket-check', methods=['POST'])
def api_ticket_check():
    """API endpoint to perform a ticket check"""
    global ticket_check_results, bot_logs, check_counter
    
    try:
        # Increment check counter for unique numbering
        check_counter += 1
        
        # In simulation mode, run deterministic demo
        if simulation_mode:
            # Simulate the exact demo sequence for frontend display
            time.sleep(1)
            result = {
                'id': int(time.time() * 1000),  # Unique ID based on timestamp
                'check_number': check_counter,  # Sequential check number
                'timestamp': time.strftime('%H:%M:%S'),  # Human readable time
                'available': True,
                'message': 'TICKETS AVAILABLE! 🎟️ - Adjacent seats: 145 & 146 (Block 32)'
            }
            ticket_check_results.append(result)
            
            # Keep only last 10 results
            if len(ticket_check_results) > 10:
                ticket_check_results = ticket_check_results[-10:]
            
            # Add simulation log
            bot_logs.append("NOTE: SIMULATION MODE — This is a simulated run and NOT a real purchase.")
            bot_logs.append(f"Target match: Arsenal vs Tottenham")
            bot_logs.append("Checking for adjacent seats...")
            bot_logs.append("Pair found: Block 32, Row 10, Seats 145–146")
            bot_logs.append("Adding tickets 12345 & 12346 to basket...")
            bot_logs.append("Basket confirmed with 2 tickets")
            bot_logs.append("Proceeding to checkout with saved card...")
            order_id = f"ORD-{random.randint(100000, 999999)}"
            bot_logs.append(f"SUCCESS: Checkout successful — Order ID: {order_id}")
            
            return jsonify({'success': True, 'result': result})
        else:
            # In real mode, we would check actual ticket availability
            result = {
                'id': int(time.time() * 1000),  # Unique ID based on timestamp
                'check_number': check_counter,  # Sequential check number
                'timestamp': time.strftime('%H:%M:%S'),  # Human readable time
                'available': False,
                'message': 'Real mode: No ticket check performed (requires Playwright)'
            }
            ticket_check_results.append(result)
            
            # Keep only last 10 results
            if len(ticket_check_results) > 10:
                ticket_check_results = ticket_check_results[-10:]
            
            return jsonify({'success': True, 'result': result})
    except Exception as e:
        error_msg = f"Error checking tickets: {str(e)}"
        bot_logs.append(error_msg)
        return jsonify({'success': False, 'message': error_msg})

@app.route('/api/status')
def api_status():
    """API endpoint to get bot status"""
    return jsonify({
        'status': bot_status,
        'logs': bot_logs[-10:],  # Last 10 logs
        'simulation_mode': simulation_mode,
        'ticket_checks': ticket_check_results[-5:]  # Last 5 ticket checks
    })

@app.route('/logs')
def logs_page():
    """Logs page"""
    return render_template('logs.html', logs=bot_logs)

@app.route('/api/logs')
def api_logs():
    """API endpoint for logs"""
    return jsonify({'logs': bot_logs})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)