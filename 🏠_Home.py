import streamlit as st
from datetime import datetime, timedelta
from utils import DAYS_5_YEARS

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
- Stock price forecasting using Facebook's Prophet
- 30-day price predictions with confidence intervals
- Trend and seasonality decomposition
- Historical vs predicted price visualization

## Getting Started
1. Navigate to the **Dashboard** page to view current stock data
2. Use the **Forecast** page to predict future price movements
3. Enter any stock ticker symbol (e.g., AAPL, GOOGL, TSLA) to begin analysis

*Note: All forecasts are for educational purposes only and should not be used for investment decisions.*
""")