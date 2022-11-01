
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
- At startup it  can subscribe  to get and save the current price of all instruments showing up in the current positions in Zerodha account based on config ```subscribe_current_positions```.   
- Can dynamically subscribe to new instruments when the application is already  running by adding the  Zerodha instrument_id , tradingsymbol in the ```conf/ticker_instruments.csv``` file  For example: ```12628226,BANKNIFTY22N0339500PE```  
- When new positions are taken in Zerodha account after application startup and if they need to be subscribed to dynamically then just create a file ```touch instrument_touch.txt``` which will load all current positions from Zerodha account and subscribe to them and start saving the current price .  
  
# Usage  
### Installation  
- Install the package 
	 ``` pip install zerodha_tickersaver```  

OR

- Download the source
```git clone https://github.com/simonmh2u/TickerSaver.git```

  
### Config file  
-  Takes as an input a json config file
- dbpath :  absolute path of the sqlite file where it needs to be created
- tickerfile_path: absolute path of the csv file which stores the instrument file that are subscribed by the application
- subscribe_current_positions : If true reads the current positions in the users zerodha account and subscribes to those instruments to get the current price
- default_instruments: list of zerodha instruments that will get subscribed to by default even if not present in the tickerfile csv
- zusername: userid copied from browser
- zwsstoken: token copied from the browser
```  
{    
  "dbpath": "/Users/johnwick/ticker_instruments.csv/live_price.db",    
  "tickerfile_path": "/Users/johnwick/ticker_instruments.csv",    
  "subscribe_current_positions": true,    
  "default_instruments": [    
   256265,    
   264969,    
   260105    
   ],
  "zusername":"",
  "zwsstoken":""
 }  
```  
  
### Startup Steps  
- User needs to manually login into Kite on any browser , and copy the below token and user from the Cookie section of the developer console.  

    <a href="https://httpie.io" target="blank_">  
        <img height="100" alt="Ticker Saver" src="https://github.com/simonmh2u/TickerSaver/blob/main/docs/cookie.png?raw=true" />  
    </a>  
    <br>  
  
- Needs to set the username and token as environment variables "ZUSERNAME"  and "ZWSSTOKEN" respectively    
- Needs to add  "zusername" and "zwsstoken" configs in the user supplied config file path(this overrides the above env variables)  
   ``` { "zusername":"YL1111", "zwsstoken":"XXXXXXX" } ```
- Fire up the application

    - ```tickersaver -c config.json``` (when package installed)

    - ``` python tickersaver/fetcher/kite/ws_tick_fetcher.py  -c config.json``` (when source downloaded)


# Disclaimer  
TickerSaver is an application built for self learning and as a  Jugaad *(definition: a resourceful approach to problem-solving)* to understand the working of web-sockets and to see if the live tick data from zerodha can be extracted and saved locally tick by tick for free without paying for monthly charges for API access. Please use at your own discretion.