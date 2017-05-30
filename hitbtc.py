import requests, json
import datetime
import hashlib
import hmac
import random
import string
import time
import sys

site = "http://api.hitbtc.com"
apikey = "aaee7e2c72ebebbbd0d910c17b584a11"
secret = "dfb5f9b05550ad06613b467b67065854"
Coin = ['ETHBTC', 'XMRBTC', 'DASHBTC', 'BTCUSD', 'ZECBTC', 'LTCBTC', 'BTUBTC']

def sha512(s, m):
	a = bytearray()
	a.extend(map(ord, s))
	b = bytearray()
	b.extend(map(ord, m))
	return hmac.new(a, b, hashlib.sha512).hexdigest() 

def mknonce():
	return str(int(time.mktime(datetime.datetime.now().timetuple()) * 1000 + datetime.datetime.now().microsecond / 1000))

def balance():
	nonce = mknonce()
	path = "/api/1/trading/balance?apikey="+apikey+"&nonce="+nonce
	signature = sha512(secret, path)
	data = requests.get(site+path, headers={"Api-Signature": signature}).json()
	P = requests.get(site+'/api/1/public/ticker').json()
	tot = 0
	for i in data['balance']:
		if i['cash'] != 0:
			coin = i['currency_code']
			if coin != 'USD' and coin != 'BTC':
				c = P[coin+'BTC']
				p = float(c['last'])
				change = (p - float(c['open'])) / float(c['open'])
				print(coin + ":")
				print('  equal: ' + str(round(i['cash']*p , 6)) + ' B')
				tot = tot + i['cash'] * p;
				print('  balance: ' + str(i['cash'])+' '+coin, end=' ')
				print("  last: " + c['last'] +' B', end=' ')
				print('  change: ' + str(round(change*100, 2)) +'%')
			elif coin == 'BTC':
				print(coin + ":")
				tot = tot + i['cash']
				print('  balance: ' + str(round(i['cash'], 6))+' B')
				print('')

	usd = float(P['BTCUSD']['last'])
	print('')
	print('account: ')
	print('toBTC: '+str(round(tot, 6)) + ' B')
	print('toUSD: '+str(round(tot*usd, 4)) + ' $')


def main():
	print('common:')
	print('  now: price on Hitbtc now')
	print('  balance: your balance on Hitbtc')
	print('  exit: exit this tool')
	while True:
		cmd = input('hitbtc >> ')
		print('')
		if cmd == 'balance':
			P = requests.get(site+'/api/1/public/ticker').json()
			balance()
		elif cmd == 'now':
			P = requests.get(site+'/api/1/public/ticker').json()
			print('time: ' + str(P['ETHBTC']['timestamp']))
			for i in Coin:
				print(i + ': ' + P[i]['last'])
		elif cmd == 'exit':
			break;
		print('')
if len(sys.argv) > 1 and sys.argv[1] == '-r':
	while True:
			P = requests.get(site+'/api/1/public/ticker').json()
			print(P['ETHBTC']['timestamp'])
			for i in Coin:
				print(i + ': ' + P[i]['last'])
			time.sleep(30)

main()
