import pandas as pd
import time
import datetime
from pytrends.request import TrendReq

# Utility functions remain unchanged
def get_current_timestamp():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def date_to_timestamp(year, month, day, hour, minute):
    return int(time.mktime(datetime.datetime(year, month, day, hour, minute).timetuple()))

def fetch_trends(keywords, timeframe='2010-01-01 2024-03-10', geo='US', category=0):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list=keywords, timeframe=timeframe, geo=geo, cat=category)
    df = pytrends.interest_over_time()
    if not df.empty:
        df = df.drop(columns=['isPartial'])  # Remove incomplete data indicator
        df.reset_index(inplace=True)
        df['date'] = pd.to_datetime(df['date']).dt.date  # Ensure date format matches stock data
    return df


def main():
    tickers = [
        "AAPL", "ADI", "ADSK", "AMAT", "AMD", "ANSS", "ASML", "AVGO", "CDW", "CRWD",
        "CTSH", "DASH", "DDOG", "GFS", "GOOG", "GOOGL", "INTU", "KLAC", "LRCX", "MDB",
        "META", "MSFT", "MU", "NVDA", "NXPI", "ON", "PANW", "PDD", "QCOM", "TXN"
    ]
    
    keywords_mapping = {
    "AAPL": ["Apple Inc", "AAPL", "Apple stock"],
    "ADI": ["Analog Devices", "ADI", "Analog Devices stock"],
    "ADSK": ["Autodesk", "ADSK", "Autodesk stock"],
    "AMAT": ["Applied Materials", "AMAT", "Applied Materials stock"],
    "AMD": ["Advanced Micro Devices", "AMD", "AMD stock"],
    "ANSS": ["ANSYS", "ANSS", "ANSYS stock"],
    "ASML": ["ASML Holding", "ASML", "ASML stock"],
    "AVGO": ["Broadcom", "AVGO", "Broadcom stock"],
    "CDW": ["CDW Corp", "CDW", "CDW Corporation stock"],
    "CRWD": ["CrowdStrike", "CRWD", "CrowdStrike stock"],
    "CTSH": ["Cognizant", "CTSH", "Cognizant stock"],
    "DASH": ["DoorDash", "DASH", "DoorDash stock"],
    "DDOG": ["Datadog", "DDOG", "Datadog stock"],
    "GFS": ["GlobalFoundries", "GFS", "GlobalFoundries stock"],
    "GOOG": ["Google", "GOOG", "Google stock"],
    "GOOGL": ["Alphabet", "GOOGL", "Alphabet stock"],
    "INTU": ["Intuit", "INTU", "Intuit stock"],
    "KLAC": ["KLA Corporation", "KLAC", "KLA Corp stock"],
    "LRCX": ["Lam Research", "LRCX", "Lam Research stock"],
    "MDB": ["MongoDB", "MDB", "MongoDB stock"],
    "META": ["Meta Platforms", "META", "Meta stock"],
    "MSFT": ["Microsoft", "MSFT", "Microsoft stock"],
    "MU": ["Micron Technology", "MU", "Micron stock"],
    "NVDA": ["NVIDIA", "NVDA", "NVIDIA stock"],
    "NXPI": ["NXP Semiconductors", "NXPI", "NXP stock"],
    "ON": ["ON Semiconductor", "ON", "ON Semiconductor stock"],
    "PANW": ["Palo Alto Networks", "PANW", "Palo Alto Networks stock"],
    "PDD": ["Pinduoduo", "PDD", "Pinduoduo stock"],
    "QCOM": ["Qualcomm", "QCOM", "Qualcomm stock"],
    "TXN": ["Texas Instruments", "TXN", "Texas Instruments stock"]
    }

    interval = '1mo'
    period1 = date_to_timestamp(2010, 1, 1, 23, 59)
    period2 = date_to_timestamp(2024, 3, 10, 23, 59)
    timeframe = f'{datetime.date.fromtimestamp(period1)} {datetime.date.fromtimestamp(period2)}'

    with pd.ExcelWriter(f'historical_data_{get_current_timestamp()}.xlsx', engine='openpyxl') as xlwriter:
        for ticker in tickers:
            print(f'Processing {ticker}')
            try:
                # Fetching stock prices
                query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history'
                stock_df = pd.read_csv(query_string)
                stock_df['Date'] = pd.to_datetime(stock_df['Date']).dt.date  # Standardize date format

                # Fetching Google Trends data
                trend_df = fetch_trends(keywords_mapping[ticker], timeframe)

                # Merge the stock and trend data on the date
                if not trend_df.empty:
                    combined_df = pd.merge(stock_df, trend_df, how='left', left_on='Date', right_on='date')
                    combined_df.to_excel(xlwriter, sheet_name=f'{ticker}_combined', index=False)
            except Exception as e:
                print(f'Error processing {ticker}: {e}')

if __name__ == "__main__":
    main()
