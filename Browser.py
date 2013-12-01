import mechanize
import cookielib
import time
from bs4 import BeautifulSoup as BSoup
import string
from urllib import urlencode
import re

class Browser():
	def __init__(self, userName, userPassword):
		self.br = mechanize.Browser()
		cj = cookielib.LWPCookieJar()
		self.br.set_cookiejar(cj)
		self.br.set_handle_equiv(True)
		#self.br.set_handle_gzip(True)
		self.br.set_handle_redirect(True)
		self.br.set_handle_referer(True)
		self.br.set_handle_robots(False)
		self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

		self.accountInfo = (userName, userPassword)
	
		self.login()
	
	def login(self):
		url = 'http://www.investopedia.com/accounts/login.aspx?returnUrl=http://www.investopedia.com/simulator/default.aspx'
		time.sleep(1)
		r = self.br.open(url)
		self.br.select_form(nr = 1)
		
		#self.br.form['ctl00$ctl00$ctl00$BBCPH$MCPH$MCPH$LoginControl$txtEmail'] = self.accountInfo[0]
		#self.br.form['ctl00$ctl00$ctl00$BBCPH$MCPH$MCPH$LoginControl$txtPassword'] = self.accountInfo[1]
		
		self.br.form['email'] = self.accountInfo[0]
		self.br.form['password'] = self.accountInfo[1]
		self.br.submit()

	def getGames(self):
		url = 'http://www.investopedia.com/simulator/home.aspx'
		time.sleep(1)
		response = self.br.open(url)
		soup = BSoup(response.read())
		self.exportFile(str(soup))
		selectTag = soup.find('select', {'name':'ddlGamesJoined'})
		
		if not selectTag:
			raise Exception("No games found")
		
		games = []
		for optionTag in selectTag.find_all('option'):
			games.append((optionTag['value'], optionTag.text))
		
		return games
			
	def setGame(self, gameID):
		data = {'ddlGamesJoined':gameID}
		url = 'http://www.investopedia.com/simulator/portfolio/default.aspx'
		time.sleep(1)
		response = self.br.open(url, urlencode(data)).read()

	def getBoughtStocks(self):
		url = 'http://www.investopedia.com/simulator/portfolio'
		template = 'http://www.investopedia.com/simulator/Ajax/Portfolio/AssetHistory.aspx?Symbol=%s&PortfolioId=%s&&ST=%s&cId=%s'
		time.sleep(1)
		response = self.br.open(url)
		soup = BSoup(response.read())
		symbols = []
		for x in soup.find_all('tr', {'id':re.compile('S*PS_LONG_\d*')}):
			all_td = x.find_all('td')
			if all_td != None and len(all_td) > 3:
				s = all_td[2].text.strip()
				quant = int(all_td[4].text.strip())
				cost = float(all_td[5].text.strip().strip('$'))
				symbols.append((s, x['id'], quant, cost))

		# Get money
		money_tag = soup.find('span', id = 'ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblBuyingPower')		   
		if money_tag != None and money_tag.text != None:
			moneyString = money_tag.text
			moneyString = string.replace(moneyString, '$', '')
			moneyString = string.replace(moneyString, ',', '')
			moneyString = float(moneyString)
			money = moneyString
			self.accountInfo.money = money
			logging.info('%s money %d' % (self.accountInfo.myId, money))


		self.boughtStocks = []
		for s, t, quant, cost in symbols:
			if 'SPS' in t: 
				q = 'short'
				transType = 2
			else: 
				q = 'long'
				transType = 0

			new_url = template % (s, self.accountInfo.profileId, q, t)
			time.sleep(1)
			#print new_url
			response2 = self.br.open(new_url)
			soup2 = BSoup(response2.read())
			time_tag = soup2.find_all('tr')[1].find_all('td')[0].text.strip()
			date = datetime.datetime.strptime(time_tag, '%m/%d/%Y %I:%M %p')
			self.boughtStocks.append(BoughtStock(s, quant, cost, date, transType = transType))

		return self.boughtStocks
		
	def placeOrder(self, stockOrder):
		data = {'submitOrder':'Submit Order >>'}
		# http://www.investopedia.com/simulator/trade/tradestockpreview.aspx?too=1&type=TYPE&Sym=SYMBOL&Qty=QTY&lmt=LIMIT&do=2&em=False
		if float(stockOrder.price) == 0.0:
			type_s = '1'
			stockOrder.price = '0'
		else:
			type_s = '2'
			stockOrder.price = str(stockOrder.price)
			
		if int(stockOrder.quantity) > self.getMaxShare(stockOrder):
			raise Exception("Invalid order: Ordering more than allowed")

		url = 'http://www.investopedia.com/simulator/trade/tradestockpreview.aspx?too=%d&type=%s&Sym=%s&Qty=%s&lmt=%s&do=1&em=False'
		url = url % (stockOrder.transaction, type_s, stockOrder.symbol, str(stockOrder.quantity), str(stockOrder.price))
		time.sleep(1)
		
		response = self.br.open(url, urlencode(data))
		self.exportFile(response.read())
		#with open('res.html', 'w') as outfile: outfile.write(response.read())

	def getMaxShare(self, stockOrder):
		data = {'isShowMax':stockOrder.transaction,
				'symbolTextbox':stockOrder.symbol,
				'action':'showMax'}
		url = 'http://www.investopedia.com/simulator/trade/tradestock.aspx'
		time.sleep(1)
		response = self.br.open(url, urlencode(data)).read()

		
		ans = re.search('(A|a) maximum of (\d*)', response)
		if ans != None: maxshare = int(ans.group(2))
		else: maxshare = None
		
		return maxshare

	def getProfileID(self):
		url = 'http://www.investopedia.com/simulator/portfolio/#axzz2MXlTZE15'
		time.sleep(1)
		response = self.br.open(url).read()
		soup = BSoup(response)
		a_buy_tag = soup.find('td', id = 'ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_StockPortfolio1_StockListRepeater_ctl01_tBox')
		if a_buy_tag:
			logging.info('found tag')
			prof_id = re.search('(\d+),', a_buy_tag['onclick'])
			if prof_id:
				logging.info('found id %s', prof_id.group(1))
				self.accountInfo.profileId = prof_id.group(1)
	
	def getAccountInfo(self):
		url = 'http://www.investopedia.com/simulator/portfolio/'
		response = self.br.open(url).read()
		soup = BSoup(response)
		accountInfoIDs = {	'ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblAccountValue'	:	'AccountValue',
							'ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblBuyingPower'		:	'BuyingPower',
							'ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblCash'			:	'Cash',
							'ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblAnnualReturn'	:	'AnnualReturn'	}
		info = {}
		for k,v in accountInfoIDs.items():
			tag = soup.find('span', id=k)
			if not tag:
				info[v]=None
			else:
				info[v]=self.stripNumbers(tag.text)
		return info
	
	def exportFile(self, r):
		with open('exp.html', 'w') as outfile:
			outfile.write(r)
	
	def stripNumbers(self, s):
		s = s.strip('$%')
		s = string.replace(s, ',', '')
		return s
		
class StockOrder(object):
	transactionTypes = {	'Buy'	:	1,
							'Sell'	:	2,
							'Short'	:	3,
							'Cover'	:	4,
							1		:	'Buy',
							2		:	'Sell',
							3		:	'Short',
							4		:	'Cover', }
	
	def __init__(self, symbol, transaction, quantity = 0, price = 0, limit = '', stop = '', duration = 'Good Till Cancelled'):
		self.symbol = symbol
		self.transaction = self.__class__.transactionTypes[transaction]
		self.quantity = quantity
		self.price = price
		self.limit = limit
		self.stop = stop
		self.duraction = duration
	
	def __str__(self):
		return 'StockOrder:\n\tSymbol: %s\n\tTransaction: %s' % (self.symbol, self.__class__.transactionTypes[self.transaction])
	
	
	
def main():
	with open('accountInfo.in') as infile:
		info = infile.read().split('\n')
	user = info[0].strip()
	p = info[1].strip()
	b = Browser(user, p)
	#print b.getGames()
	#print b.stripNumbers('$100,000,000.000%')
	print b.getAccountInfo()
	1/0
	for i,j in b.getGames():
		print i,j
		b.setGame(i)
		s = StockOrder('GOOG', 'Buy', 1, price = 10)
		#print b.getMaxShare(s)
		b.placeOrder(s)
	print s
	

if __name__ == '__main__':
	main()
	
	
	