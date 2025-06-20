import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Stock Forecast", layout="wide")

st.title("🔮 Stock Price Forecast")

stock_symbol = st.session_state.get('stock_symbol', '')
start_date = st.session_state.get('start_date', datetime.now() - timedelta(days=1825))
end_date = st.session_state.get('end_date', datetime.now())

with st.sidebar:
    st.header("Forecast Settings")
    forecast_days = st.slider("Forecast Days", min_value=7, max_value=90, value=30)

if stock_symbol:
    try:
        with st.spinner(f"Fetching data and generating forecast for {stock_symbol.upper()}..."):
            ticker = yf.Ticker(stock_symbol.upper())
            data = ticker.history(start=start_date, end=end_date)
            
            if data.empty:
                st.error(f"No data found for symbol '{stock_symbol.upper()}'. Please check the ticker symbol.")
            elif len(data) < 100:
                st.error(f"Insufficient data for forecasting. Please select a longer date range (at least 100 days).")
            else:
                df = data.reset_index()
                df_prophet = pd.DataFrame({
                    'ds': df['Date'].dt.tz_localize(None),
                    'y': df['Close']
                })
                
                model = Prophet(weekly_seasonality=False)
                model.fit(df_prophet)
                
                future = model.make_future_dataframe(periods=forecast_days)
                forecast = model.predict(future)
                
                col1, col2 = st.columns(2)
                with col1:
                    current_price = data['Close'][-1]
                    predicted_price = forecast['yhat'].iloc[-1]
                    st.metric("Current Price", f"${current_price:.2f}")
                with col2:
                    price_change = predicted_price - current_price
                    change_pct = (price_change / current_price) * 100
                    st.metric(
                        f"Predicted Price ({forecast_days}d)", 
                        f"${predicted_price:.2f}",
                        f"{price_change:+.2f} ({change_pct:+.1f}%)"
                    )
                
                fig = model.plot(forecast)
                st.pyplot(fig)
                
                st.subheader("Forecast Components")
                
                fig_components = model.plot_components(forecast)
                st.pyplot(fig_components)
                
                st.subheader("Forecast Data")
                forecast_display = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_days)
                forecast_display.columns = ['Date', 'Forecast', 'Lower Bound', 'Upper Bound']
                forecast_display['Date'] = forecast_display['Date'].dt.date
                for col in ['Forecast', 'Lower Bound', 'Upper Bound']:
                    forecast_display[col] = forecast_display[col].round(2)
                st.dataframe(forecast_display, use_container_width=True)
                
    except Exception as e:
        st.error(f"Error generating forecast: {str(e)}")
        st.info("Make sure you have enough historical data (at least 100 days) for accurate forecasting.")
else:
    st.info("Enter a stock symbol to generate a forecast")
    st.markdown("""
    ### About Prophet Forecasting
    
    This page uses Facebook's Prophet algorithm to forecast stock prices. Prophet is designed to handle:
    - **Trend**: Long-term increase or decrease
    - **Seasonality**: Weekly and yearly patterns  
    - **Holidays**: Market holidays and events
    
    **Note**: Forecasts are for educational purposes only and should not be used for investment decisions.
    """)