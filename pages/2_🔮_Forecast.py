import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
import matplotlib.pyplot as plt
import warnings
from typing import Optional, Tuple

warnings.filterwarnings('ignore')

# Constants
MIN_DATA_POINTS = 100
MIN_CV_DATA_POINTS = 730
DEFAULT_LOOKBACK_DAYS = 1825
DEFAULT_FORECAST_DAYS = 30

st.set_page_config(page_title="Stock Forecast", layout="wide")

st.title("🔮 Stock Price Forecast")

def get_stock_data(symbol: str, start_date: datetime, end_date: datetime) -> Optional[pd.DataFrame]:
    """Fetch stock data from Yahoo Finance."""
    try:
        ticker = yf.Ticker(symbol.upper())
        data = ticker.history(start=start_date, end=end_date)
        return data if not data.empty else None
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None

def prepare_prophet_data(data: pd.DataFrame) -> pd.DataFrame:
    """Prepare data for Prophet model."""
    df = data.reset_index()
    return pd.DataFrame({
        'ds': df['Date'].dt.tz_localize(None),
        'y': df['Close']
    })

def perform_cross_validation(model: Prophet, df: pd.DataFrame) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    """Perform cross validation on Prophet model."""
    if len(df) < MIN_CV_DATA_POINTS:
        return None
    
    try:
        initial_days = min(365, len(df) // 2)
        cv_results = cross_validation(
            model,
            initial=f'{initial_days} days',
            period='90 days',
            horizon='30 days'
        )
        performance = performance_metrics(cv_results)
        return cv_results, performance
    except Exception as e:
        st.warning(f"Cross validation failed: {str(e)}")
        return None

# Initialize session state
stock_symbol = st.session_state.get('stock_symbol', '')
start_date = st.session_state.get('start_date', datetime.now() - timedelta(days=DEFAULT_LOOKBACK_DAYS))
end_date = st.session_state.get('end_date', datetime.now())

with st.sidebar:
    st.header("Forecast Settings")
    forecast_days = st.slider("Forecast Days", min_value=7, max_value=90, value=DEFAULT_FORECAST_DAYS)

if stock_symbol:
    with st.spinner(f"Fetching data and generating forecast for {stock_symbol.upper()}..."):
        data = get_stock_data(stock_symbol, start_date, end_date)
        
        if data is None:
            st.error(f"No data found for symbol '{stock_symbol.upper()}'. Please check the ticker symbol.")
        elif len(data) < MIN_DATA_POINTS:
            st.error(f"Insufficient data for forecasting. Please select a longer date range (at least {MIN_DATA_POINTS} days).")
        else:
            try:
                df_prophet = prepare_prophet_data(data)
                
                model = Prophet(
                    weekly_seasonality=False,
                    daily_seasonality=False,
                    yearly_seasonality=True
                )
                model.fit(df_prophet)
                
                future = model.make_future_dataframe(periods=forecast_days)
                forecast = model.predict(future)
                
                # Display metrics
                col1, col2 = st.columns(2)
                with col1:
                    current_price = data['Close'].iloc[-1]
                    st.metric("Current Price", f"${current_price:.2f}")
                with col2:
                    predicted_price = forecast['yhat'].iloc[-1]
                    price_change = predicted_price - current_price
                    change_pct = (price_change / current_price) * 100
                    st.metric(
                        f"Predicted Price ({forecast_days}d)", 
                        f"${predicted_price:.2f}",
                        f"{price_change:+.2f} ({change_pct:+.1f}%)"
                    )
                
                # Main forecast plot
                fig = model.plot(forecast)
                fig.suptitle(f'{stock_symbol.upper()} Stock Price Forecast', fontsize=16)
                st.pyplot(fig)
                
                st.subheader("Forecast Components")
                fig_components = model.plot_components(forecast)
                st.pyplot(fig_components)
                
                # Cross validation analysis
                st.subheader("Cross Validation Analysis")
                cv_data = perform_cross_validation(model, df_prophet)
                
                if cv_data is not None:
                    cv_results, performance = cv_data
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Cross Validation Performance**")
                        metrics_display = performance[['horizon', 'mae', 'mape', 'rmse']].round(4)
                        metrics_display.columns = ['Horizon', 'MAE', 'MAPE', 'RMSE']
                        st.dataframe(metrics_display, use_container_width=True)
                    
                    with col2:
                        fig_cv, ax = plt.subplots(figsize=(10, 6))
                        cv_results_plot = cv_results.copy()
                        cv_results_plot['residual'] = cv_results_plot['y'] - cv_results_plot['yhat']
                        
                        ax.scatter(cv_results_plot['ds'], cv_results_plot['residual'], 
                                 alpha=0.6, s=30, color='blue')
                        ax.axhline(y=0, color='red', linestyle='--', alpha=0.7)
                        ax.set_xlabel('Date')
                        ax.set_ylabel('Residual (Actual - Predicted)')
                        ax.set_title('Cross Validation Residuals')
                        ax.grid(True, alpha=0.3)
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        st.pyplot(fig_cv)
                        plt.close()
                else:
                    st.info(f"Cross validation requires at least {MIN_CV_DATA_POINTS} days of data for reliable results.")
                
                # Forecast data table
                st.subheader("Forecast Data")
                forecast_display = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_days).copy()
                forecast_display.columns = ['Date', 'Forecast', 'Lower Bound', 'Upper Bound']
                forecast_display['Date'] = forecast_display['Date'].dt.date
                for col in ['Forecast', 'Lower Bound', 'Upper Bound']:
                    forecast_display[col] = forecast_display[col].round(2)
                st.dataframe(forecast_display, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error generating forecast: {str(e)}")
                st.info(f"Make sure you have enough historical data (at least {MIN_DATA_POINTS} days) for accurate forecasting.")
else:
    st.info("Enter a stock symbol to generate a forecast")
    
    with st.expander("ℹ️ About Prophet Forecasting", expanded=True):
        st.markdown("""
        ### Prophet Algorithm Features
        
        This page uses Facebook's Prophet algorithm to forecast stock prices. Prophet is designed to handle:
        - **Trend**: Long-term increase or decrease patterns
        - **Seasonality**: Yearly patterns in stock behavior
        - **Uncertainty**: Confidence intervals for predictions
        - **Cross Validation**: Model performance assessment
        
        ### Model Configuration
        - Daily seasonality: Disabled (too noisy for stock data)
        - Weekly seasonality: Disabled (markets closed on weekends)
        - Yearly seasonality: Enabled (captures annual patterns)
        
        **⚠️ Important**: Forecasts are for educational purposes only and should not be used for investment decisions.
        """)