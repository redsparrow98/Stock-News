# Stock News App

This Stock News App tracks the stock of a chosen company (Tesla Inc in this case) and determines the stock's rise or 
fall percentage over the past two days at the stock closing time. 

If the stock rises or falls by more than 5%, it then 
uses the NewsAPI to access three most recent articles about the company whose stock is being tracked. 
These articles are formatted and sent to the user via Twilio services on WhatsApp using a free 
account (WhatsApp sandbox). 

The reason for sending out the text is to give the user a starting point for research since the news might cover some 
event that caused the company stock to rise/fall drastically, such as an incident or a new release.


## Installation
Clone the repository to your local machine.
```commandline
git clone https://github.com/redsparrow98/Stock-News.git
cd stock-news-app
```
Create and activate a virtual environment.
```commandline
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
Install the required packages.
```commandline
pip install -r requirements.txt
```
Create a .env file in the project root directory and add your API keys and Twilio credentials.
```commandline
STOCK_API_KEY=your_alpha_vantage_api_key        # stock news
NEWS_API_KEY=your_news_api_key
ACCOUNT_SID=your_twilio_account_sid
AUTH_TOKEN=your_twilio_auth_token
SENDER_NUMBER=your_twilio_whatsapp_number
RECEIVER_NUMBER=your_verified_whatsapp_number
```

## How It Works

- **Fetch Stock Data:** The app fetches the daily stock data for Tesla Inc. from the Alpha Vantage API.

- **Calculate Percentage Change:** It calculates the percentage change in the stock price between the closing prices of the 
last two days.

- **Check for Significant Change:** If the percentage change is greater than 5%, it fetches the latest news articles about 
Tesla Inc. from the NewsAPI.

- **Send News via Twilio:** The three most recent news articles are formatted and sent to the user via Twilio's WhatsApp 
service.


## Changing the Tracked Company
To track the stock of a different company, you can change the ***STOCK_NAME*** and ***COMPANY_NAME*** constant 
variables in the program.

**STOCK_NAME:**

- This should be set to the [ticker symbol](https://en.wikipedia.org/wiki/Ticker_symbol) of the company you wish to track. 
- These symbols can be unique to each country, but all countries use some form of the system. 
- You can find the ticker symbols that Alpha Vantage provides by downloading the
[CSV file](https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo) that contains all the tickers the API supports.

**COMPANY_NAME:** 

- This should be set to the full public name of the company.
- It's used for the NewsAPI query to retrieve the most relevant and accurate articles for the company whose stock is being tracked.



## Dependencies
-   Python 3.7+
- requests
- python-dotenv
- twilio


## API References
- [Alpha Vantage API](https://www.alphavantage.co/)
- [NewsAPI](https://newsapi.org/)
- [Twilio](https://www.twilio.com/en-us)

