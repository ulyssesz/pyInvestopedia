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
Investopedia, by default chooses a portfolio when logging in. To make sure you are managing the correct portfolio, use `Browser.setGame(id)`

```python
b = Browser(user, p)
game_id = "211140"
b.setGame(game_id)
```

## Get portfolio info
`Browser.getPortfolioInfo()` retrieves the `AccountValue`, `BuyingPower`, `AnnualReturn` and `Cash` for the portfolio chosen (by `b.setGame()`).

```python
b = Browser(user, p)
print b.getPortfolioInfo()
```

Sample Output:
```python
{'AccountValue': u'100000.00', 'BuyingPower': u'100000.00', 'AnnualReturn': u'0.00 ', 'Cash': u'100000.00'}
```





