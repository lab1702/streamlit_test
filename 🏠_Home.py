import streamlit as st
from datetime import datetime, timedelta
from utils import DAYS_5_YEARS, logger, get_company_info_cached
from typing import Any

st.set_page_config(
    page_title="Stock Analysis Hub",
    page_icon="📈",
    layout="wide"
)

with st.sidebar:
    st.header("Stock Controls")
    
    stock_symbol = st.text_input("Stock Symbol", placeholder="Enter stock ticker (e.g., AAPL)")
    
    # Display company name if symbol is entered
    if stock_symbol:
        try:
            company_info = get_company_info_cached(stock_symbol)
            if company_info:
                company_name = company_info.get('longName', company_info.get('shortName', 'N/A'))
                st.markdown("**Company Name**")
                st.markdown(f"**{company_name}**")
            else:
                st.markdown("**Company Name**")
                st.markdown("*Company not found*")
        except:
            st.markdown("**Company Name**")
            st.markdown("*Loading...*")
    else:
        st.markdown("**Company Name**")
        st.markdown("*Enter a symbol above*")
    
    st.divider()
    
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

## Getting Started
1. **Start by entering a stock symbol** → Look to the sidebar on the left and enter a stock ticker symbol (e.g., AAPL, GOOGL, TSLA)
2. Select your preferred date range (default: 5 years of historical data)
3. Navigate to the **Dashboard** page to view real-time stock data and charts
4. Use the **Forecast** page to predict future price movements with AI

## Available Pages:

""")

st.markdown("### 📊 Dashboard")
st.page_link("pages/1_📊_Dashboard.py", label="→ Go to Dashboard")
st.markdown("""
- Real-time stock data visualization
- Interactive candlestick charts
- Volume analysis with bar charts
- Key financial metrics display
""")

st.markdown("### 🔮 Forecast")
st.page_link("pages/2_🔮_Forecast.py", label="→ Go to Forecast")
st.markdown("""
- Stock price forecasting using Facebook's Prophet algorithm
- Configurable forecast periods (7-90 days) with confidence intervals
- Trend and seasonality decomposition analysis
- Cross validation with performance metrics (MAE, MAPE, RMSE)
- Residual analysis for prediction accuracy assessment
- Intelligent model caching for instant predictions

*Note: All forecasts are for educational purposes only and should not be used for investment decisions.*
""")