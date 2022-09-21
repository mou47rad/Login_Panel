import requests
import re
import threading
import time
import urllib3
import io
import random
import string
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = str(input('Enter your username: '))
password = str(input('Enter your password: '))
quantity = str(input('Enter quantity numbers: '))

with io.open('numbers_test.txt', 'w', encoding='utf-8') as f:
	f.write('')

url = 'http://127.1.1.0/ajax_form_handler.php'
s = requests.Session()
s.headers.update({
	'Accept':'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'en-US,en;q=0.9,ar;q=0.8',
	'Connection':'keep-alive',
	'Content-Length':'39',
	'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	'Cookie':'PHPSESSID=7vigoj9h8a95q8u4eqe3jqk214',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
	'X-Requested-With':'XMLHttpRequest',
	})


#login
data = {'action':'save','sub':'login','username':username,'password':password}
resp = s.post(url,data=data, allow_redirects=True)



#get all hash countrry
data = {'sub': 'numberslist', 'menu': 'sms', 'action': 'getmenu'}
resp = s.post(url,data=data, allow_redirects=True)

#scrapng hashs
menu = resp.json()['menu']
soup = BeautifulSoup(menu, 'html.parser')
soup = soup.find_all('select')[0]
soup = soup.find_all('option')[1:]

dic_data = {}
for i in soup:
	dic_data[i.text]  = i['value']

#get numbers
for i_data in dic_data: 
	data = {'sub':'numberslist','subpage':'numberslist','page':'numbers','pageview':'sms','pageviewcnt':quantity,'pagesearch':'','pageorder':'dateAsc','pageno':'1','noclient':'all','noservice':'all','nobillgroup':str(dic_data[i_data]),'test_view_type':'1','search_option':'1','action':'get',}
	resp = s.post(url,data=data, allow_redirects=True)
	save_id = resp.json()['save_id']
	soup = BeautifulSoup(save_id, 'html.parser')
	soup = soup.find_all('input')
	print(i_data)
	for input_ in soup:
		number = input_['value']
		print(number)
	
		with io.open('numbers_test.txt', 'a', encoding='utf-8') as f:
			f.write(number + '\n')

input('____END____')