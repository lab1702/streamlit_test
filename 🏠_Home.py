import streamlit as st
from datetime import datetime, timedelta
from utils import DAYS_5_YEARS, logger
from typing import Any

st.set_page_config(
    page_title="Stock Analysis Hub",
    page_icon="📈",
    layout="wide"
)

with st.sidebar:
    st.header("Stock Controls")
    
    stock_symbol = st.text_input("Stock Symbol", placeholder="Enter stock ticker (e.g., AAPL)")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=DAYS_5_YEARS))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    if 'stock_symbol' not in st.session_state:
        st.session_state.stock_symbol = ""
    if 'start_date' not in st.session_state:
        st.session_state.start_date = datetime.now() - timedelta(days=DAYS_5_YEARS)
    if 'end_date' not in st.session_state:
        st.session_state.end_date = datetime.now()
    
    st.session_state.stock_symbol = stock_symbol
    st.session_state.start_date = start_date
    st.session_state.end_date = end_date
    
    # Cache invalidation controls
    if st.button("🔄 Refresh Data", help="Clear cache and fetch fresh data"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Cache cleared! Fresh data will be loaded on next navigation.")
        logger.info(f"Cache manually cleared for {stock_symbol.upper() if stock_symbol else 'all symbols'}")

st.title("📈 Stock Analysis Hub")

st.markdown("""
Welcome to the Stock Analysis Hub! This application provides comprehensive stock market analysis tools.

## Available Pages:

### 📊 Dashboard
- Real-time stock data visualization
- Interactive candlestick charts
- Volume analysis with bar charts
- Key financial metrics display

### 🔮 Forecast
- Stock price forecasting using Facebook's Prophet algorithm
- Configurable forecast periods (7-90 days) with confidence intervals
- Trend and seasonality decomposition analysis
- Cross validation with performance metrics (MAE, MAPE, RMSE)
- Residual analysis for prediction accuracy assessment
- Intelligent model caching for instant predictions

## Getting Started
1. Enter a stock ticker symbol (e.g., AAPL, GOOGL, TSLA) in the sidebar
2. Select your preferred date range (default: 5 years of historical data)
3. Navigate to the **Dashboard** page to view real-time stock data and charts
4. Use the **Forecast** page to predict future price movements with AI
5. Click "🔄 Refresh Data" to clear cache and fetch fresh data when needed

## Performance Features
- **Smart Caching**: Data and models are cached to reduce API calls by ~90%
- **Instant Loading**: Subsequent visits load cached data immediately
- **Model Persistence**: Trained Prophet models are saved for faster predictions
- **Background Logging**: Comprehensive error tracking and performance monitoring

*Note: All forecasts are for educational purposes only and should not be used for investment decisions.*
""")