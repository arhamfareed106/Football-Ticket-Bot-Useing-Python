"""
Login Manager Module
Handles account authentication and browser session management
"""

import asyncio
import random
from playwright.async_api import async_playwright


class LoginManager:
    def __init__(self, proxy_manager):
        self.proxy_manager = proxy_manager
        self.browsers = {}  # Store browser instances by account username
        self.pages = {}     # Store page instances by account username

    async def initialize_browsers(self):
        """Initialize Playwright browsers for all accounts"""
        # We'll create browsers on-demand for each login attempt
        # This approach is more memory-efficient
        pass

    async def login(self, account):
        """Login to an account using Playwright with anti-detection measures"""
        try:
            # Get a proxy for this account
            proxy = self.proxy_manager.get_next_proxy()
            
            async with async_playwright() as p:
                # Configure browser with anti-detection settings
                browser_options = {
                    "headless": False,  # Set to True for production
                }
                
                # Add proxy if available
                if proxy:
                    browser_options["proxy"] = {
                        "server": proxy
                    }
                
                # Create a new browser instance
                browser = await p.chromium.launch(**browser_options)
                
                # Create a new page
                page = await browser.new_page()
                
                # Set realistic viewport size
                await page.set_viewport_size({
                    "width": 1366,
                    "height": 768
                })
                
                # Set realistic user agent
                await page.set_user_agent(self.get_random_user_agent())
                
                # Set realistic headers
                await page.set_extra_http_headers({
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                })
                
                # Navigate to login page
                await page.goto("https://official-ticket-exchange.com/login", wait_until="networkidle")
                
                # Add some human-like delays
                await self.random_delay(1000, 2000)
                
                # Fill in credentials with human-like typing
                await self.human_type(page, "#username", account["username"])
                await self.random_delay(500, 1000)
                await self.human_type(page, "#password", account["password"])
                await self.random_delay(500, 1000)
                
                # Click login button
                await page.click("#login-button")
                
                # Wait for navigation or error
                try:
                    await page.wait_for_timeout(10000)  # Wait for potential navigation
                except:
                    pass
                
                # Check if login was successful
                is_logged_in = await self.check_login_status(page)
                
                if is_logged_in:
                    # Store browser and page for this account
                    self.browsers[account["username"]] = browser
                    self.pages[account["username"]] = page
                    
                    return {
                        "success": True,
                        "browser": browser,
                        "page": page
                    }
                else:
                    # Close browser on failed login
                    await browser.close()
                    return {
                        "success": False,
                        "error": "Login failed - invalid credentials or captcha required"
                    }
        except Exception as error:
            return {
                "success": False,
                "error": f"Login error: {str(error)}"
            }

    async def check_login_status(self, page):
        """Check if the current page shows a successful login"""
        try:
            # Look for elements that indicate successful login
            dashboard_element = await page.query_selector(".dashboard, .user-profile, .account-menu")
            logout_button = await page.query_selector("a[href*='logout'], button.logout")
            
            return dashboard_element is not None or logout_button is not None
        except Exception as error:
            return False

    async def logout(self, account):
        """Logout from an account"""
        try:
            page = self.pages.get(account["username"])
            browser = self.browsers.get(account["username"])
            
            if page:
                # Try to navigate to logout URL
                try:
                    await page.goto("https://official-ticket-exchange.com/logout", wait_until="networkidle")
                except:
                    pass  # Ignore errors
                
                self.pages.pop(account["username"], None)
            
            if browser:
                await browser.close()
                self.browsers.pop(account["username"], None)
            
            return {"success": True}
        except Exception as error:
            return {"success": False, "error": str(error)}

    async def close_all_browsers(self):
        """Close all browser instances"""
        for username, browser in self.browsers.items():
            try:
                await browser.close()
            except:
                # Ignore errors when closing
                pass
        
        self.browsers.clear()
        self.pages.clear()

    async def human_type(self, page, selector, text):
        """Simulate human-like typing with random delays"""
        await page.focus(selector)
        
        for char in text:
            await page.type(selector, char, delay=self.random_int(50, 150))

    async def random_delay(self, min_ms, max_ms):
        """Generate a random delay between min and max milliseconds"""
        delay = self.random_int(min_ms, max_ms)
        await asyncio.sleep(delay / 1000)

    def random_int(self, min_val, max_val):
        """Generate a random integer between min and max (inclusive)"""
        return random.randint(min_val, max_val)

    def get_random_user_agent(self):
        """Get a random realistic user agent"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        return random.choice(user_agents)