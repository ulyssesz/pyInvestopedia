pyInvestopedia
==============

Interact with Investopedia Stock Simulator with Python
Can be used to test strategies.

Everything is done without interacting with an actual browser, so can be put on a cloud platform like Google App Engine.


## What can it do?
It can:
Buy/Sell/Short/Cover stocks
Trade on multiple portfolios/games
Get portfolio info


# Usage

## Login
First, to do anything, create a `Browser` object to login and store the authentication.

```python
user = "username@domain.com"
pass = "helloworld"
b = Browser(user, pass)
``


