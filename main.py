import os
import requests
from dotenv import find_dotenv, load_dotenv
from twilio.rest import Client


# ----------------------------------------------------------------------------------------------------------------------
# ================= #
#   dotenv set-up   #
# ================= #

# Find the .env file automatically by walking up directories until its found
dotenv_path = find_dotenv()

# Load up the entries in the .env file as environment variables
load_dotenv(dotenv_path)


# ----------------------------------------------------------------------------------------------------------------------
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
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Twilio credentials
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
SENDER_NUMBER = os.getenv("SENDER_NUMBER")
RECEIVER_NUMBER = os.getenv("RECEIVER_NUMBER")


# ----------------------------------------------------------------------------------------------------------------------
# STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increases/decreases by 5% between yesterday and the day before yesterday then access the 3 most
# recent news articles about the company and send it to user.

# ============== #
#    Stock API   #
# ============== #

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

# Creates a response from the stock api retrieving the stock data for Tesla.
response = requests.get(url="https://www.alphavantage.co/query", params=stock_params)
response.raise_for_status()
# Selects only the 'Time Series (Daily)' key from the data which contains all the data for each day
stock_data = response.json()["Time Series (Daily)"]


# Get yesterday's closing and day before yesterday's closing stock price.
"""
In order for this app to be correct it would need to get the data for the past 2 days any time its run. Therefore it
cant use the hard coded keys in the stock_data which would be specific dates (e.g. 2024-06-14)

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


# Find the difference between yesterday's and day before yesterday's stock value.
difference = float(yesterdays_closing_price) - float(day_bf_yest_closing_price)


# If the difference was bigger than 0, assigns the up emoji to be shown in the message article report sent by twilio
# at the end. And if it was below 0, assign the arrow down emoji.
# This is for better user experience
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


# Work out the % difference in price between closing price yesterday and closing price of the day before yesterday.
# Round up the result to the closest round number for ease of reading since this information will be sent in the message
# as well.
"""
1. Calculate the change (X) from the yesterdays (A) and day before yesterdays (B): A − B = X
2. Divide the change (X) by the original value (A): X ÷ A = D
3. Finally, multiply this amount by 100: D × 100 = The Percentage Change (C)
"""
diff_percentage = round((difference / float(yesterdays_closing_price)) * 100)


# ----------------------------------------------------------------------------------------------------------------------
# ================= #
#     News API      #
# ================= #
# STEP 2: https://newsapi.org/

# If the stock difference between the two days is bigger than 5%, then it retrieves the 3 recent news articles about
# the company.It sends a message to the user's phone notifying them of the big change and possibly a reason as to why
# the change is so big.

if abs(diff_percentage) > 5:
    """
    -   To find the positive difference percentage (diff_percentage) between the two days it must use the absolute 
        function on the percentage result to get the positive difference even if it a negative one.
        (The absolute value of a real number x is the non-negative value of x without regard to its sign)    
    """
    # Use the News API to get articles related to the Tesla Inc, sets up the API parameters and retrieves the articles
    # from the response
    news_params = {
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
        "searchIn": "title",
        "language": "en",
    }

    # request the GET form the API
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data_articles = news_response.json()["articles"]

    # Use Python slice operator to create a list that contains the 3 newest articles.
    three_articles = news_data_articles[:3]

# ----------------------------------------------------------------------------------------------------------------------
    # STEP 3: Use twilio.com/docs/sms/quickstart/python to send each article to user's phone.

    """
    Create a new list of the first 3 article using list comprehension which contain the following:
    
    - The stock name the emoji for up or down to help visually explain and the amount of % that the stock changed
    - Article headlines for each message
    - And Article description for the contents of the article.
    """
    formatted_articles = [f"{STOCK_NAME} {up_down}{diff_percentage}% \
                            \nHeadline: {article['title']}. \
                            \nBrief: {article['description']}" for article in three_articles]

    # Send each article as a separate message via a Twilio client.
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            from_=SENDER_NUMBER,
            body=article,
            to=RECEIVER_NUMBER
        )
