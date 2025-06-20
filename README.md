# 📈 Stock Analysis Hub

A comprehensive Streamlit dashboard for stock market analysis, featuring real-time data visualization and AI-powered price forecasting.

## Features

### 🏠 Home Page
- Centralized stock symbol and date range controls
- Navigation hub with app overview
- Shared state management across pages

### 📊 Dashboard
- **Real-time Stock Data**: Live price, daily change, volume, and market cap
- **Interactive Candlestick Charts**: Plotly-powered charts with zoom and pan functionality
- **Volume Analysis**: Color-coded volume bars for trading activity
- **Key Metrics**: Formatted financial data with currency abbreviations (K, M, B, T)

### 🔮 Forecast
- **AI-Powered Predictions**: Facebook Prophet algorithm for price forecasting
- **Configurable Timeframes**: 7-90 day forecast periods
- **Trend Analysis**: Decomposition charts showing trend and seasonality components
- **Confidence Intervals**: Upper and lower bounds for predictions
- **Data Export**: Downloadable forecast tables

## Installation

### Quick Setup (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/lab1702/streamlit_test
cd streamlit_test
```

2. Run the installation script:
```bash
./install.sh
```

3. Activate the virtual environment:
```bash
source venv/bin/activate
```

4. Run the application:
```bash
streamlit run "🏠_Home.py"
```

### Manual Setup

1. Clone the repository:
```bash
git clone https://github.com/lab1702/streamlit_test
cd streamlit_test
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run "🏠_Home.py"
```

## Dependencies

- **streamlit**: Web app framework
- **yfinance**: Yahoo Finance data API
- **plotly**: Interactive charting library
- **pandas**: Data manipulation and analysis
- **prophet**: Time series forecasting

## Usage

1. **Start the App**: Launch with `streamlit run "🏠_Home.py"`
2. **Enter Stock Symbol**: Input any valid ticker (e.g., AAPL, GOOGL, TSLA)
3. **Select Date Range**: Choose historical data timeframe (default: 5 years)
4. **Navigate Pages**: Use sidebar to switch between Dashboard and Forecast
5. **Analyze Data**: View charts, metrics, and predictions

## Data Source

Stock data is fetched from Yahoo Finance via the `yfinance` library, providing:
- Historical OHLCV (Open, High, Low, Close, Volume) data
- Real-time price information
- Company fundamentals (market cap, etc.)

## Forecasting

The Prophet model analyzes historical price patterns to predict future movements:
- **Trend Component**: Long-term price direction
- **Seasonality**: Yearly patterns in stock behavior
- **Uncertainty**: Confidence intervals for predictions

## File Structure

```
streamlit_test/
├── 🏠_Home.py              # Main entry point
├── pages/
│   ├── 1_📊_Dashboard.py   # Real-time data visualization
│   └── 2_🔮_Forecast.py    # AI price predictions
├── utils.py                # Shared utilities and constants
├── requirements.txt        # Project dependencies
└── README.md              # This file
```

## Configuration

### Default Settings
- **Historical Data**: 5 years (1825 days)
- **Forecast Period**: 30 days
- **Minimum Data**: 100 days required for forecasting
- **Chart Height**: 700px for dashboard, 600px for forecast

### Customization
- Modify constants in `utils.py` for different defaults
- Adjust chart styling in individual page files
- Add new metrics or indicators as needed

## Limitations

- **Data Accuracy**: Depends on Yahoo Finance data quality
- **Forecast Reliability**: AI predictions are for educational purposes only
- **Market Hours**: Real-time data may have delays
- **Symbol Validation**: No pre-validation of ticker symbols

## Disclaimer

This application is for educational and informational purposes only. Stock price forecasts should not be used as the sole basis for investment decisions. Always consult with financial professionals before making investment choices.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues or questions:
- Create an issue in the repository
- Check existing documentation
- Review error messages in the app interface