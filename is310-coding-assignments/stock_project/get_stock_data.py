import time
import datetime
import pandas as pd

def get_current_timestamp():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def date_to_timestamp(year, month, day, hour, minute):
    """Convert a date to a timestamp."""
    return int(time.mktime(datetime.datetime(year, month, day, hour, minute).timetuple()))

def get_historical_prices(tickers, interval, period1, period2):
    with pd.ExcelWriter(f'historical_prices_{get_current_timestamp()}.xlsx', engine='openpyxl') as xlwriter:
        for ticker in tickers:
            print(f'Processing ticker {ticker}')
            try:
                query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history'
                df = pd.read_csv(query_string)
                df.to_excel(xlwriter, sheet_name=ticker[:31], index=False)  # Sheet name limited to 31 chars
            except Exception as e:
                print(f'{ticker}: {e}')
                continue

def main():
    # Define parameters
    # List of ticker symbols for the top 30 companies in the NASDAQ 100 Technology Sector
    tickers = [
        "AAPL", "ADI", "ADSK", "AMAT", "AMD", "ANSS", "ASML", "AVGO", "CDW", "CRWD",
        "CTSH", "DASH", "DDOG", "GFS", "GOOG", "GOOGL", "INTU", "KLAC", "LRCX", "MDB",
        "META", "MSFT", "MU", "NVDA", "NXPI", "ON", "PANW", "PDD", "QCOM", "TXN"
    ]
    interval = '1wk'  # Frequency {1d, 1wk, 1mo}
    period1 = date_to_timestamp(2010, 1, 1, 23, 59)
    period2 = date_to_timestamp(2024, 3, 10, 23, 59)
    # Get historical prices data
    get_historical_prices(tickers, interval, period1, period2)

if __name__ == "__main__":
    main()
