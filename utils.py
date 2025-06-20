# Constants
DAYS_5_YEARS = 1825
MIN_DATA_POINTS = 100

def format_currency(value):
    """Format a numeric value as currency with abbreviations."""
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

def format_market_cap(market_cap):
    """Format market cap with proper handling of None/N/A values."""
    if market_cap and market_cap != 'N/A':
        return format_currency(market_cap)
    return "N/A"