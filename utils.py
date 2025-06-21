from typing import Union, Optional
import logging
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import hashlib
from config import get_config

# Load configuration
data_config = get_config('data')
logging_config = get_config('logging')
cache_config = get_config('cache')

# Constants from configuration
DAYS_5_YEARS = data_config['default_lookback_days']
MIN_DATA_POINTS = data_config['min_data_points']
MIN_CV_DATA_POINTS = data_config['min_cv_data_points']
DEFAULT_FORECAST_DAYS = data_config['default_forecast_days']

# Configure logging
logging.basicConfig(
    level=getattr(logging, logging_config['level']),
    format=logging_config['format']
)
logger = logging.getLogger(__name__)

def format_currency(value: Union[float, int]) -> str:
    """
    Format a numeric value as currency with abbreviations.
    
    Args:
        value: Numeric value to format
        
    Returns:
        Formatted currency string with appropriate suffix (K, M, B, T)
        
    Examples:
        >>> format_currency(1500)
        '$1.50K'
        >>> format_currency(2500000)
        '$2.50M'
    """
    try:
        if value >= 1e12:
            return f"${value/1e12:.2f}T"
        elif value >= 1e9:
            return f"${value/1e9:.2f}B"
        elif value >= 1e6:
            return f"${value/1e6:.2f}M"
        elif value >= 1e3:
            return f"${value/1e3:.2f}K"
        else:
            return f"${value:.2f}"
    except (TypeError, ValueError) as e:
        logger.error(f"Error formatting currency value {value}: {e}")
        return "N/A"

def format_market_cap(market_cap: Optional[Union[float, int, str]]) -> str:
    """
    Format market cap with proper handling of None/N/A values.
    
    Args:
        market_cap: Market cap value, can be numeric or string
        
    Returns:
        Formatted market cap string or 'N/A' if invalid
    """
    if market_cap and market_cap != 'N/A' and market_cap != 0:
        try:
            return format_currency(float(market_cap))
        except (TypeError, ValueError) as e:
            logger.warning(f"Invalid market cap value {market_cap}: {e}")
            return "N/A"
    return "N/A"

def format_volume_dollars(volume: Union[float, int], price: Union[float, int]) -> str:
    """
    Format volume in dollar terms with abbreviations.
    
    Args:
        volume: Trading volume
        price: Current price per share
        
    Returns:
        Formatted volume dollar amount
    """
    try:
        volume_dollars = float(volume) * float(price)
        return format_currency(volume_dollars)
    except (TypeError, ValueError) as e:
        logger.error(f"Error calculating volume dollars: volume={volume}, price={price}, error={e}")
        return "N/A"

@st.cache_data(
    ttl=cache_config['data_ttl_seconds'], 
    max_entries=cache_config['max_data_entries'], 
    show_spinner=cache_config['show_cache_spinner']
)
def get_company_info_cached(symbol: str) -> Optional[dict]:
    """
    Get cached company information from Yahoo Finance.
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        Dictionary with company info or None if error
    """
    try:
        logger.info(f"Fetching company info for {symbol.upper()} (cache miss)")
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info
        
        if not info:
            logger.warning(f"No company info found for symbol {symbol.upper()}")
            return None
            
        logger.info(f"Successfully fetched company info for {symbol.upper()}")
        return info
    except Exception as e:
        logger.error(f"Error fetching company info for {symbol}: {str(e)}")
        return None

@st.cache_data(
    ttl=cache_config['data_ttl_seconds'], 
    max_entries=cache_config['max_data_entries'], 
    show_spinner=cache_config['show_cache_spinner']
)
def get_stock_data_cached(symbol: str, start_date: datetime, end_date: datetime) -> Optional[pd.DataFrame]:
    """
    Cached version of stock data fetching from Yahoo Finance.
    
    Args:
        symbol: Stock ticker symbol
        start_date: Start date for data retrieval
        end_date: End date for data retrieval
        
    Returns:
        DataFrame with stock data or None if error/no data
        
    Note:
        Cache TTL: 5 minutes, Max entries: 100 stocks
    """
    try:
        logger.info(f"Fetching stock data for {symbol.upper()} from {start_date} to {end_date} (cache miss)")
        ticker = yf.Ticker(symbol.upper())
        data = ticker.history(start=start_date, end=end_date)
        
        if data.empty:
            logger.warning(f"No data found for symbol {symbol.upper()}")
            return None
        
        logger.info(f"Successfully fetched {len(data)} data points for {symbol.upper()}")
        return data
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {str(e)}")
        return None

def generate_data_hash(data: pd.DataFrame) -> str:
    """
    Generate a hash for DataFrame to use as cache key.
    
    Args:
        data: DataFrame to hash
        
    Returns:
        SHA-256 hash string of the data
    """
    try:
        # Create hash from data shape and a sample of values
        data_str = f"{data.shape}_{data.iloc[0].to_string()}_{data.iloc[-1].to_string()}"
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    except Exception as e:
        logger.error(f"Error generating data hash: {e}")
        return "default_hash"