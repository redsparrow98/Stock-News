import os
import requests
from dotenv import find_dotenv, load_dotenv

# -----------------------------------------------------------------------------------------------------------------
# ================= #
#   dotenv set-up   #
# ================= #

# Find the .env file automatically by walking up directories until its found
dotenv_path = find_dotenv()

# Load up the entries in the .env file as environment variables
load_dotenv(dotenv_path)

# -----------------------------------------------------------------------------------------------------------------
# ================= #
#     CONSTANTS     #
# ================= #

# Tesla data
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"


# Stock API constants
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = os.getenv("STOCK_API_KEY")


# news API constants
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# -----------------------------------------------------------------------------------------------------------------
# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increases/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# ============== #
#    Stock API   #
# ============== #

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

# Creates a response from the stock api retrieving the stock data for Tesla.
# Selects only the 'Time Series (Daily)' key from the data
response = requests.get(url="https://www.alphavantage.co/query", params=stock_params)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]


# Get yesterday's closing and day before yesterday's closing stock price.
"""
In order for this app to be correct it would need to get the data for the past 2 days any time its run. Therefore it
cant use the hard coded keys in the stock_daya which would be specific dates (e.g. 2024-06-14)

    - To work around this the program creates a new list from the stock_data using list comprehension selecting only the 
    values which will hold all nested dictionary with keys for each significant point of the day. 
    (open, high, low, close, volume) and the price at that point of the day as the value
    
    - To select yesterday's closing stock price it just need to access the first item in the list '0' and the '4. close' 
    key which will retrieve the value of the stock at market close point.
    
    - To select day before yesterday's closing stock price it just need to access the second item in the list '1' and 
    the '4. close' key which will retrieve the value of the stock at market close point.
"""
stock_data_list = [value for (key, value) in stock_data.items()]
yesterdays_closing_price = stock_data_list[0]["4. close"]
day_bf_yest_closing_price = stock_data_list[1]["4. close"]


# Find the positive difference between yesterday's and day before yesterday's stock value.
"""
    - To find the positive difference (days_difference) between the two days the program subtracts the second day out of
    the first day which are converted from string in to float data types.
    
    - Then it uses the absolute function on the equation to get the positive difference even if it a negative one.
    (The absolute value of a real number x is the non-negative value of x without regard to its sign)
"""
difference = abs(float(yesterdays_closing_price) - float(day_bf_yest_closing_price))

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday
"""
1. Calculate the change (X) from the yesterdays (A) and day before yesterdays (B): A − B = X
2. Divide the change (X) by the original value (A): X ÷ A = D
3. Finally multiply this amount by 100: D × 100 = The Percentage Change (C)
"""
diff_percentage = (difference / float(yesterdays_closing_price)) * 100


    # TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if diff_percentage > 5:
    print("Get News")


# -----------------------------------------------------------------------------------------------------------------
# ================= #
#     News API      #
# ================= #
## STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

    # TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

    # TODO 7. - Use Python slice operator to create a list that contains the first 3 articles.
    # Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation

# STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

    # TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

    # TODO 9. - Send each article as a separate message via Twilio.


# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the 
coronavirus market crash.

or

"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file
by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the
coronavirus market crash.
"""

