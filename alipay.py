from BeautifulSoup import BeautifulSoup as bs
import requests
import time

#Alipay cookie after logged in
cookies = {'ALIPAYJSESSIONID': ''}

#API
api = 'http://'

#API return success
api_success = 1

#API return data existed
api_exist = 2

#Custom Secure Key
key = ''

url = 'https://lab.alipay.com/consume/record/items.htm'

# store transaction id.if id in list, do not pass api
posted = []
while True:
    if len(posted) > 1000:
        posted = []
    req = requests.get(url, cookies=cookies)
    if req.url.startswith('https://auth.alipay.com/'):
        print('authenticate failed')
        import sys

        sys.exit(0)
    html = req.text

    soup = bs(html)

    transactions = soup.findAll("tr")

    for tr in transactions:
        if transactions.index(tr) == 0:
            continue

        tr = bs(str(tr))

        id = tr.find("div", {"class": "consumeBizNo"}).getText().strip()
        if id in posted:
            continue

        name = tr.find("span", {"class": "ft-gray"}).getText()
        if '-' not in name:
            continue

        name = name.split('-')[1]
        tm = tr.find("td", {"class": "time"}).getText()
        amount = tr.find("td", {"class": "amount income"}).getText()

        data = {'id': id, 'time': tm, 'name': name, 'amount': amount, 'key':key}
        response = requests.post(api, data)
        #1 may means received, 2 means data existed
        if response != api_exist and response != api_success:
            posted.append(id)
            print(name + '    ' + tm + '    ' + id + '    ' + amount)


    time.sleep(5)







