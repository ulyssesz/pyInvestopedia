pyInvestopedia
==============

Interact with Investopedia Stock Simulator with Python.  
Can be used to test strategies.

Everything is done without interacting with an actual browser, so can be put on a cloud platform like Google App Engine.


## What can it do?
It can:  
Buy/Sell/Short/Cover stocks.  
Trade on multiple portfolios/games.  
Get portfolio info.  


# Usage

## Login
First, to do anything, create a `Browser` object to login and store the authentication.

```python
user = "username@domain.com"
pass = "helloworld"
b = Browser(user, pass)
```

## Get Game Info
In case you are playing in multiple games, you can retrieve all your games and respective ids using `Browser.getGames()`

```python
b = Browser(user, p)
print b.getAccountInfo()
```

Sample Output:
A list of id,name pairs.
```python
[(u'211140', u'Active Game - Investopedia Game 2013 No End'), (u'100', u'Beginners')]
```

## To change portfolio
Investopedia, by default chooses a portfolio when logging in. To make sure you are managing the correct portfolio, use `Browser.setGame(id)` to change the active portfolio.

```python
b = Browser(user, p)
game_id = "211140"
b.setGame(game_id)
```

## Get portfolio info
`Browser.getPortfolioInfo()` retrieves the `AccountValue`, `BuyingPower`, `AnnualReturn` and `Cash` for the active portfolio.

```python
b = Browser(user, p)
print b.getPortfolioInfo()
```

Sample Output:
```python
{'AccountValue': u'100000.00', 'BuyingPower': u'100000.00', 'AnnualReturn': u'0.00 ', 'Cash': u'100000.00'}
```

## Get Securities
`Browser.getSecurities()` retrieves the securities from the active portfolio. It returns a list of `Security` objects. (Note: if there are multiple orders for the same stock(issued at different times), there will be an object sent for each.)

```python
b = Browser(user, p)
securities = b.getSecurities()
for s in securities:
  print s
```

Sample Output:  
```python
[<__main__.Security object at 0x886b70>, <__main__.Security object at 0x886c30>, <__main__.Security object at 0x8866b0>, <__main__.Security object at 0x6c7df0>, <__main__.Security object at 0x88b2b0>]
Security:
	Symbol: BBRY
	Quantity: 1000
	Security Type: SHORT
	Time: 12/2/2013 02:15 PM
Security:
	Symbol: MSFT
	Quantity: 500
	Security Type: SHORT
	Time: 12/2/2013 02:15 PM
Security:
	Symbol: MSFT
	Quantity: 100
	Security Type: SHORT
	Time: 12/2/2013 02:48 PM
Security:
	Symbol: AAPL
	Quantity: 500
	Security Type: LONG
	Time: 12/2/2013 02:15 PM
Security:
	Symbol: IBM
	Quantity: 500
	Security Type: LONG
	Time: 12/2/2013 02:15 PM
```

## `Security` class
It has the following properties (Note: They are all strings): 
`symbol`          : The symbol of security  
`qty`             : The quantity of the one order  
`securityType`    : Security type `LONG` or `SHORT`  
`purchasePrice`   : Purchase price of this order (per stock)  
`adjPurchasePrice`: Adjusted price (per stock)  
`currentPrice`    : Current market price  
`time`            : Time of purchase  

