"""
Test script to demonstrate the football ticket bot structure
"""

import json
import os
from pathlib import Path

def test_config_loading():
    """Test that config file can be loaded"""
    config_path = Path("config.json")
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
        print("✓ Config file loaded successfully")
        print(f"  Accounts: {len(config.get('accounts', []))}")
        print(f"  Proxies: {len(config.get('proxies', []))}")
        print(f"  Target URL: {config.get('target_match_url', 'Not set')}")
        return True
    else:
        print("✗ Config file not found")
        return False

def test_module_imports():
    """Test that all modules can be imported"""
    try:
        from modules.proxy_manager import ProxyManager
        print("✓ ProxyManager module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import ProxyManager: {e}")
        return False
    
    try:
        from modules.login_manager import LoginManager
        print("✓ LoginManager module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import LoginManager: {e}")
        return False
    
    try:
        from modules.queue_handler import QueueHandler
        print("✓ QueueHandler module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import QueueHandler: {e}")
        return False
    
    try:
        from modules.ticket_monitor import TicketMonitor
        print("✓ TicketMonitor module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import TicketMonitor: {e}")
        return False
    
    try:
        from modules.purchase_engine import PurchaseEngine
        print("✓ PurchaseEngine module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import PurchaseEngine: {e}")
        return False
    
    try:
        from utils.logger import Logger
        print("✓ Logger module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import Logger: {e}")
        return False
    
    try:
        from utils.config import Config
        print("✓ Config utility module imported successfully")
    except Exception as e:
        print(f"✗ Failed to import Config utility: {e}")
        return False
    
    return True

def test_directory_structure():
    """Test that directory structure is correct"""
    required_dirs = ['modules', 'utils', 'logs']
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✓ {dir_name} directory exists")
        else:
            print(f"✗ {dir_name} directory missing")
            return False
    return True

def main():
    """Run all tests"""
    print("Football Ticket Bot - Structure Test")
    print("=" * 40)
    
    # Test directory structure
    print("\n1. Testing directory structure:")
    dirs_ok = test_directory_structure()
    
    # Test config loading
    print("\n2. Testing config loading:")
    config_ok = test_config_loading()
    
    # Test module imports
    print("\n3. Testing module imports:")
    imports_ok = test_module_imports()
    
    # Summary
    print("\n" + "=" * 40)
    print("Test Summary:")
    print(f"  Directory structure: {'PASS' if dirs_ok else 'FAIL'}")
    print(f"  Config loading: {'PASS' if config_ok else 'FAIL'}")
    print(f"  Module imports: {'PASS' if imports_ok else 'FAIL'}")
    
    if dirs_ok and config_ok and imports_ok:
        print("\n✓ All tests passed! The bot structure is ready.")
        print("\nTo run the full bot, you'll need to:")
        print("1. Install Playwright: pip install playwright")
        print("2. Install Playwright browsers: python -m playwright install")
        print("3. Run the bot: python football_bot.py")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()