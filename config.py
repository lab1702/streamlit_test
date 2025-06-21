"""
Configuration settings for the Stock Analysis Hub application.
"""
import os
from typing import Dict, Any

# Application Configuration
APP_CONFIG: Dict[str, Any] = {
    "page_title": "Stock Analysis Hub",
    "page_icon": "📈",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Data Configuration
DATA_CONFIG: Dict[str, Any] = {
    "default_lookback_days": int(os.getenv("DEFAULT_LOOKBACK_DAYS", "1825")),  # 5 years
    "min_data_points": int(os.getenv("MIN_DATA_POINTS", "100")),
    "min_cv_data_points": int(os.getenv("MIN_CV_DATA_POINTS", "730")),  # 2 years
    "default_forecast_days": int(os.getenv("DEFAULT_FORECAST_DAYS", "30")),
    "max_forecast_days": int(os.getenv("MAX_FORECAST_DAYS", "90")),
    "min_forecast_days": int(os.getenv("MIN_FORECAST_DAYS", "7"))
}

# Prophet Model Configuration
PROPHET_CONFIG: Dict[str, Any] = {
    "weekly_seasonality": False,
    "daily_seasonality": False,
    "yearly_seasonality": True,
    "seasonality_mode": "multiplicative",
    "changepoint_prior_scale": 0.05,
    "seasonality_prior_scale": 10.0
}

# Cross Validation Configuration
CV_CONFIG: Dict[str, Any] = {
    "initial_days": int(os.getenv("CV_INITIAL_DAYS", "365")),
    "period_days": int(os.getenv("CV_PERIOD_DAYS", "90")),
    "horizon_days": int(os.getenv("CV_HORIZON_DAYS", "30"))
}

# Chart Configuration
CHART_CONFIG: Dict[str, Any] = {
    "dashboard_height": int(os.getenv("DASHBOARD_CHART_HEIGHT", "700")),
    "forecast_height": int(os.getenv("FORECAST_CHART_HEIGHT", "600")),
    "volume_opacity": float(os.getenv("VOLUME_OPACITY", "0.8")),
    "candlestick_increasing_color": os.getenv("CANDLESTICK_UP_COLOR", "#00D4AA"),
    "candlestick_decreasing_color": os.getenv("CANDLESTICK_DOWN_COLOR", "#FF6692")
}

# Logging Configuration
LOGGING_CONFIG: Dict[str, Any] = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
    "file_path": os.getenv("LOG_FILE_PATH", None)  # None means console only
}

# API Configuration
API_CONFIG: Dict[str, Any] = {
    "yfinance_timeout": int(os.getenv("YFINANCE_TIMEOUT", "30")),
    "max_retries": int(os.getenv("API_MAX_RETRIES", "3")),
    "retry_delay": float(os.getenv("API_RETRY_DELAY", "1.0"))
}

# Cache Configuration
CACHE_CONFIG: Dict[str, Any] = {
    "data_ttl_seconds": int(os.getenv("CACHE_DATA_TTL_SECONDS", "3600")),  # 1 hour for stock data
    "model_ttl_seconds": int(os.getenv("CACHE_MODEL_TTL_SECONDS", "3600")),  # 1 hour for Prophet models
    "forecast_ttl_seconds": int(os.getenv("CACHE_FORECAST_TTL_SECONDS", "3600")),  # 1 hour for forecasts
    "max_data_entries": int(os.getenv("CACHE_MAX_DATA_ENTRIES", "100")),  # Max cached stock data
    "max_model_entries": int(os.getenv("CACHE_MAX_MODEL_ENTRIES", "20")),  # Max cached models
    "max_forecast_entries": int(os.getenv("CACHE_MAX_FORECAST_ENTRIES", "50")),  # Max cached forecasts
    "enabled": os.getenv("CACHE_ENABLED", "true").lower() == "true",
    "show_cache_spinner": os.getenv("CACHE_SHOW_SPINNER", "false").lower() == "true"
}

def get_config(section: str = None) -> Dict[str, Any]:
    """
    Get configuration for a specific section or all configurations.
    
    Args:
        section: Configuration section name (e.g., 'data', 'prophet', 'chart')
                If None, returns all configurations
    
    Returns:
        Dictionary containing the requested configuration
    """
    all_configs = {
        "app": APP_CONFIG,
        "data": DATA_CONFIG,
        "prophet": PROPHET_CONFIG,
        "cv": CV_CONFIG,
        "chart": CHART_CONFIG,
        "logging": LOGGING_CONFIG,
        "api": API_CONFIG,
        "cache": CACHE_CONFIG
    }
    
    if section is None:
        return all_configs
    
    return all_configs.get(section, {})