# Zerodha WebSocket Ticker Saver

<h2 align="center">
    <a href="https://httpie.io" target="blank_">
        <img height="100" alt="Ticker Saver" src="https://github.com/simonmh2u/TickerSaver/blob/main/docs/logo.png?raw=true" />
    </a>
    <br>
 Free web-socket wrapper client for Zerodha Trading platform 
</h2>


# What

TickerSaver is a  web-socket wrapper client for Zerodha trading platform which can listen to the Zerodha web-socket stream for any stock or index instruments on the Trading platform and saves the current price of the instrument  in sqlite database.
Any backend Live Trading Algo program can now use this live tick current price data by reading from the sql-lite database which is continuously getting updated by the TickerSaver application. 
**It does this all free without the 2000 INR monthly cost that Zerodha charges for WebSocket live tick data.**

# Install


# How

- User needs to have a valid  account on Zerodha Trading platform - Kite
- User will need log into the Kite Web on any browser and copy the user token and username from the browser and provide it to the TickerSaver application
- TickerSaver will now connect to your account and connect to Zerodha WebSocket server to get live tick data for any subscribed instruments
- It will save the current price of all subscribed instruments in a sql-lite database which can then be used by any of your applications like Live Trading bots to get the current live price from this sql-lite db which is constantly getting updated


# Features
- Costs 0 rupees to get live tick data
- Saves the current price of all subscribed instruments in sql-lite database which can be used by live trading bots
- At startup can subscribe  to get and save the current price of all instruments showing up in the current positions in Zerodha account based on config ```subscribe_current_positions```. 
- Can dynamically subscribe to new instruments when the application is already  running. Just add the  Zerodha instrument_id , tradingsymbol in the ```conf/ticker_instruments.csv``` file  For example: ```12628226,BANKNIFTY22N0339500PE```
- When new positions are taken in Zerodha account and if they need to be subscribed to dynamically then just create a file ```touch instrument_touch.txt``` which will load all current positions from Zerodha account and subscribe to them and start saving the current price .

# Usage
- User needs to manually login into Kite on any browser , and copy the below token 
 <img height="100" alt="Ticker Saver" src="https://github.com/simonmh2u/TickerSaver/docs/logo.png" />
- Needs to set the username and token as environment variables "ZUSERNAME"  and "ZWSSTOKEN" respectively
- Needs to add in conf/config.json the "zusername" and "zwsstoken" (this overrides the above env variables)
	```
	{
		"username":"YL1111",
		"wsstoken":"XXXXXXX"
	}
	```
# Disclaimer
TickerSaver is an application built for self learning and as a  Jugaad *(definition: a resourceful approach to problem-solving)* to understand the working of web-sockets and to see if the live tick data from zerodha can be extracted and saved locally tick by tick for free without paying for monthly charges for API access. Please use at your own discretion.

