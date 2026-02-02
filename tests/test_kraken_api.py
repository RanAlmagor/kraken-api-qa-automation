"""
QA Automation Tests for Kraken API
Tests various endpoints and validates responses
"""

import pytest
from utils.kraken_api import KrakenAPI


@pytest.fixture
def api():
    """Create KrakenAPI instance for testing"""
    return KrakenAPI()


class TestKrakenAPI:
    """Test suite for Kraken API endpoints"""
    
    def test_get_server_time(self, api):
        """Test that server time endpoint returns valid response"""
        response = api.get_server_time()
        
        # Validate response structure
        assert "error" in response, "Response should contain 'error' field"
        assert "result" in response, "Response should contain 'result' field"
        
        # Validate no errors
        assert len(response["error"]) == 0, "Should not have errors"
        
        # Validate result contains expected fields
        assert "unixtime" in response["result"], "Result should contain unixtime"
        assert "rfc1123" in response["result"], "Result should contain rfc1123"
        
        # Validate unixtime is reasonable (greater than 2020)
        assert response["result"]["unixtime"] > 1577836800, "Unix time should be after 2020"
    
    def test_get_ticker_btc_valid(self, api):
        """Test getting BTC/USD ticker with valid pair"""
        response = api.get_ticker("XXBTZUSD")
        
        # Validate response structure
        assert "error" in response
        assert "result" in response
        assert len(response["error"]) == 0
        
        # Validate ticker data exists
        assert len(response["result"]) > 0, "Result should contain ticker data"
        
        # Get ticker data (first item in result)
        ticker_data = list(response["result"].values())[0]
        
        # Validate required fields exist
        assert "c" in ticker_data, "Should contain current price"
        assert "v" in ticker_data, "Should contain volume"
        assert "h" in ticker_data, "Should contain high price"
        assert "l" in ticker_data, "Should contain low price"
        
        # Validate price is reasonable
        current_price = float(ticker_data["c"][0])
        assert current_price > 0, "Price should be positive"
        assert current_price < 1000000, "Price should be realistic"
    
    def test_get_ticker_invalid_pair(self, api):
        """Test getting ticker with invalid pair (negative test)"""
        response = api.get_ticker("INVALIDPAIR123")
        
        # Should return error for invalid pair
        assert "error" in response
        assert len(response["error"]) > 0, "Should have error for invalid pair"
    
    def test_get_ohlc_btc(self, api):
        """Test getting OHLC (candlestick) data for BTC"""
        response = api.get_ohlc("XXBTZUSD", interval=1)
        
        # Validate response structure
        assert "error" in response
        assert "result" in response
        assert len(response["error"]) == 0
        
        # Validate OHLC data exists
        assert len(response["result"]) > 0
        
        # Get OHLC data
        pair_key = list(response["result"].keys())[0]
        ohlc_data = response["result"][pair_key]
        
        # Validate we have candles
        assert len(ohlc_data) > 0, "Should have OHLC candles"
        
        # Validate first candle structure (should have 8 elements)
        first_candle = ohlc_data[0]
        assert len(first_candle) == 8, "Candle should have 8 elements"
        
        # Validate OHLC values are positive
        open_price = float(first_candle[1])
        high_price = float(first_candle[2])
        low_price = float(first_candle[3])
        close_price = float(first_candle[4])
        
        assert open_price > 0
        assert high_price > 0
        assert low_price > 0
        assert close_price > 0
        
        # Validate high >= low
        assert high_price >= low_price, "High should be >= low"
    
    def test_get_order_book(self, api):
        """Test getting order book (market depth)"""
        response = api.get_order_book("XXBTZUSD", count=5)
        
        # Validate response
        assert "error" in response
        assert "result" in response
        assert len(response["error"]) == 0
        
        # Get order book data
        pair_key = list(response["result"].keys())[0]
        order_book = response["result"][pair_key]
        
        # Validate asks and bids exist
        assert "asks" in order_book, "Should have asks"
        assert "bids" in order_book, "Should have bids"
        
        # Validate asks structure
        asks = order_book["asks"]
        assert len(asks) > 0, "Should have at least one ask"
        
        first_ask = asks[0]
        assert len(first_ask) >= 2, "Ask should have price and volume"
        
        ask_price = float(first_ask[0])
        ask_volume = float(first_ask[1])
        
        assert ask_price > 0, "Ask price should be positive"
        assert ask_volume > 0, "Ask volume should be positive"
        
        # Validate bids structure
        bids = order_book["bids"]
        assert len(bids) > 0, "Should have at least one bid"
        
        first_bid = bids[0]
        bid_price = float(first_bid[0])
        bid_volume = float(first_bid[1])
        
        assert bid_price > 0, "Bid price should be positive"
        assert bid_volume > 0, "Bid volume should be positive"
        
        # Validate bid < ask (market spread)
        assert bid_price < ask_price, "Bid should be lower than ask"
    
    def test_get_asset_pairs(self, api):
        """Test getting available trading pairs"""
        response = api.get_asset_pairs()
        
        # Validate response
        assert "error" in response
        assert "result" in response
        assert len(response["error"]) == 0
        
        # Validate we have pairs
        pairs = response["result"]
        assert len(pairs) > 0, "Should have trading pairs"
        
        # Validate BTC/USD pair exists
        assert any("XBT" in pair and "USD" in pair for pair in pairs.keys()), \
            "Should have BTC/USD pair"