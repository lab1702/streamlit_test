import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Stock Dashboard", layout="wide")

st.title("📊 Stock Dashboard")

stock_symbol = st.session_state.get('stock_symbol', '')
start_date = st.session_state.get('start_date', datetime.now() - timedelta(days=1825))
end_date = st.session_state.get('end_date', datetime.now())

if stock_symbol:
    try:
        with st.spinner(f"Fetching data for {stock_symbol.upper()}..."):
            ticker = yf.Ticker(stock_symbol.upper())
            data = ticker.history(start=start_date, end=end_date)
            
            if data.empty:
                st.error(f"No data found for symbol '{stock_symbol.upper()}'. Please check the ticker symbol.")
            else:
                info = ticker.info
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Current Price", f"${data['Close'][-1]:.2f}")
                with col2:
                    change = data['Close'][-1] - data['Close'][-2]
                    st.metric("Daily Change", f"${change:.2f}", f"{(change/data['Close'][-2]*100):.2f}%")
                with col3:
                    volume_dollars = data['Volume'][-1] * data['Close'][-1]
                    if volume_dollars >= 1e9:
                        volume_str = f"${volume_dollars/1e9:.2f}B"
                    elif volume_dollars >= 1e6:
                        volume_str = f"${volume_dollars/1e6:.2f}M"
                    elif volume_dollars >= 1e3:
                        volume_str = f"${volume_dollars/1e3:.2f}K"
                    else:
                        volume_str = f"${volume_dollars:.2f}"
                    st.metric("Volume", volume_str)
                with col4:
                    market_cap = info.get('marketCap', 0)
                    if market_cap and market_cap != 'N/A':
                        if market_cap >= 1e12:
                            market_cap_str = f"${market_cap/1e12:.2f}T"
                        elif market_cap >= 1e9:
                            market_cap_str = f"${market_cap/1e9:.2f}B"
                        elif market_cap >= 1e6:
                            market_cap_str = f"${market_cap/1e6:.2f}M"
                        else:
                            market_cap_str = f"${market_cap:,.0f}"
                    else:
                        market_cap_str = "N/A"
                    st.metric("Market Cap", market_cap_str)
                
                fig = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.1,
                    subplot_titles=(f"{stock_symbol.upper()} Candlestick Chart", "Volume"),
                    row_heights=[0.7, 0.3]
                )
                
                fig.add_trace(
                    go.Candlestick(
                        x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'],
                        name=stock_symbol.upper()
                    ),
                    row=1, col=1
                )
                
                fig.add_trace(
                    go.Bar(
                        x=data.index,
                        y=data['Volume'],
                        name="Volume",
                        marker_color='rgba(255,165,0,0.8)'
                    ),
                    row=2, col=1
                )
                
                fig.update_layout(
                    height=700,
                    showlegend=False,
                    xaxis_rangeslider_visible=False
                )
                
                fig.update_yaxes(title_text="Price ($)", row=1, col=1)
                fig.update_yaxes(title_text="Volume", row=2, col=1)
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("Recent Data")
                st.dataframe(data.tail(10), use_container_width=True)
                
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
else:
    st.info("Enter a stock symbol to get started")