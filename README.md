# 📈 Stock Analysis Hub

A comprehensive Streamlit dashboard for stock market analysis, featuring real-time data visualization and AI-powered price forecasting.

## Features

### 🏠 Home Page
- Centralized stock symbol and date range controls
- Navigation hub with app overview
- Shared state management across pages
- **Cache Management**: Manual cache refresh controls for fresh data

### 📊 Dashboard
- **Real-time Stock Data**: Live price, daily change, volume, and market cap
- **Interactive Candlestick Charts**: Plotly-powered charts with zoom and pan functionality
- **Volume Analysis**: Color-coded volume bars for trading activity
- **Key Metrics**: Formatted financial data with currency abbreviations (K, M, B, T)
- **Performance Optimized**: Intelligent caching reduces API calls by 90%

### 🔮 Forecast
- **AI-Powered Predictions**: Facebook Prophet algorithm for price forecasting
- **Configurable Timeframes**: 7-90 day forecast periods
- **Trend Analysis**: Decomposition charts showing trend and seasonality components
- **Confidence Intervals**: Upper and lower bounds for predictions
- **Cross Validation**: Model performance assessment with MAE, MAPE, and RMSE metrics
- **Residual Analysis**: Scatter plots showing prediction accuracy over time
- **Data Export**: Downloadable forecast tables
- **Model Caching**: Trained Prophet models cached for instant predictions
- **Comprehensive Logging**: Detailed error tracking and performance monitoring

## Installation

### Quick Setup (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/lab1702/streamlit_test
cd streamlit_test
```

2. Run the installation script:
```bash
bash install.sh
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
6. **Refresh Data**: Use the "🔄 Refresh Data" button to clear cache and fetch fresh data

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
- **Cross Validation**: Evaluates model performance using time series splits with configurable initial period (365 days), validation period (90 days), and forecast horizon (30 days)
- **Performance Metrics**: MAE (Mean Absolute Error), MAPE (Mean Absolute Percentage Error), and RMSE (Root Mean Square Error) for accuracy assessment

## File Structure

```
streamlit_test/
├── 🏠_Home.py              # Main entry point with cache controls
├── pages/
│   ├── 1_📊_Dashboard.py   # Real-time data visualization
│   └── 2_🔮_Forecast.py    # AI price predictions with caching
├── utils.py                # Shared utilities, caching, and logging
├── config.py               # Application configuration and settings
├── requirements.txt        # Project dependencies
├── Dockerfile              # Docker container configuration
├── docker-compose.yml      # Docker Compose setup
├── .dockerignore           # Docker build optimization
└── README.md              # This file
```

## Configuration

### Default Settings
- **Historical Data**: 5 years (1825 days)
- **Forecast Period**: 30 days
- **Minimum Data**: 100 days required for forecasting
- **Cross Validation**: 730 days minimum for reliable CV analysis
- **Chart Height**: 700px for dashboard, 600px for forecast
- **Cache TTL**: 5 minutes for stock data, 1 hour for models
- **Cache Limits**: 100 stock datasets, 20 Prophet models

### Environment Variables
Customize the application using environment variables:
```bash
# Data Configuration
DEFAULT_LOOKBACK_DAYS=1825
MIN_DATA_POINTS=100
DEFAULT_FORECAST_DAYS=30

# Cache Configuration
CACHE_DATA_TTL_SECONDS=300          # Stock data cache duration
CACHE_MODEL_TTL_SECONDS=3600        # Prophet model cache duration
CACHE_MAX_DATA_ENTRIES=100          # Max cached datasets
CACHE_MAX_MODEL_ENTRIES=20          # Max cached models
CACHE_ENABLED=true                  # Enable/disable caching

# Logging Configuration
LOG_LEVEL=INFO                      # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Customization
- Use environment variables for configuration (see `config.py`)
- Modify chart styling in individual page files
- Add new metrics or indicators as needed
- Configure caching behavior for performance optimization

## Performance Features

- **Intelligent Caching**: Reduces API calls by ~90% for repeat visits
- **Model Persistence**: Trained Prophet models cached for instant predictions
- **Optimized Data Loading**: Smart caching with configurable TTL
- **Error Handling**: Comprehensive logging and graceful failure handling
- **Resource Management**: Automatic cache cleanup and memory optimization

## Limitations

- **Data Accuracy**: Depends on Yahoo Finance data quality
- **Forecast Reliability**: AI predictions are for educational purposes only
- **Market Hours**: Real-time data may have delays
- **Symbol Validation**: No pre-validation of ticker symbols
- **Cache Storage**: In-memory caching (lost on app restart)

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
