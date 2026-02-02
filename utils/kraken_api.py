"""
Kraken API Wrapper for QA Testing
Provides methods to interact with Kraken public API endpoints
"""

import requests


class KrakenAPI:
    """Wrapper class for Kraken public API"""
    
    BASE_URL = "https://api.kraken.com/0/public"
    TIMEOUT = 10  # seconds
    
    def __init__(self):
        self.session = requests.Session()
    
    def _make_request(self, endpoint, params=None):
        """
        Make HTTP request to Kraken API
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            dict: JSON response from API
        """
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=self.TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": [str(e)], "result": None}
    
    def get_server_time(self):
        """Get Kraken server time"""
        return self._make_request("Time")
    
    def get_ticker(self, pair):
        """
        Get ticker information for a currency pair
        
        Args:
            pair: Currency pair (e.g., 'XXBTZUSD' for BTC/USD)
        """
        return self._make_request("Ticker", params={"pair": pair})
    
    def get_ohlc(self, pair, interval=1):
        """
        Get OHLC (candlestick) data
        
        Args:
            pair: Currency pair
            interval: Time interval in minutes (1, 5, 15, 30, 60, etc.)
        """
        return self._make_request("OHLC", params={"pair": pair, "interval": interval})
    
    def get_order_book(self, pair, count=10):
        """
        Get order book (market depth)
        
        Args:
            pair: Currency pair
            count: Maximum number of asks/bids
        """
        return self._make_request("Depth", params={"pair": pair, "count": count})
    
    def get_asset_pairs(self):
        """Get tradeable asset pairs"""
        return self._make_request("AssetPairs")