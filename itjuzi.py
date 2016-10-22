#coding:utf-8
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import datetime,time,random
import codecs

def download_page(download_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    html = requests.get(download_url,headers=headers).content.decode('utf-8')
    return html


date_list, link_list, company_list, field_list,place_list,round_list, amount_list, investor_list = [], [], [], [], [], [],[],[]


def parse_html(html):
    date, link, company, field, place, round, amount, investor = [], [], [], [], [], [], [], []
    body = BeautifulSoup(html,'lxml')
    eventset = body.find_all('ul',attrs={'class':'list-main-eventset'})[1]
    for event in eventset.find_all('li'):
        t = event.find('i',attrs={'class':'cell round'}).find('span').get_text().strip()
        date.append(t)
        amount.append(event.find('i',attrs = {'class':'cell fina'}).get_text().strip())
        a = event.find_all('a')
        link.append(a[0]['href'].strip())
        company.append(a[1].get_text().strip())
        field.append(a[2].get_text().strip())
        place.append(a[3].get_text().strip())
        round.append(a[4].get_text().strip())

        #investor 可能有多个，对应多个链接，也可能是‘投资方未透露’，需要处理这两种情况
        if len(a) >= 6:
            inv = ','.join([i.get_text().strip() for i in a[5:]])
        else:
            span = event.find('span',attrs = {'class':'investorset'}).find_all('span')
            inv = ','.join([i.get_text().strip() for i in span])
        investor.append(inv)

    page_url = body.find('div',attrs={'class':'ui-pagechange for-sec-bottom'}).find_all('a')
    if page_url[-1]['href']:
        download_url = page_url[-2]['href']
    else:
        download_url = False

    return date,link,company,field,place,round,amount,investor,download_url


download_url = 'https://www.itjuzi.com/investevents?page=1430'
def loop():
    global download_url
    while download_url:
        html = download_page(download_url)
        date, link, company, field, place, round, amount, investor, download_url = parse_html(html)

        date_list.extend(date)
        link_list.extend(link)
        company_list.extend(company)
        field_list.extend(field)
        place_list.extend(place)
        round_list.extend(round)
        amount_list.extend(amount)
        investor_list.extend(investor)
        time.sleep(random.random() * 0.5)

#由于截止目前共有1534页，数量太多，所以提取前10页
def main():
    start = datetime.datetime.now()
    try:
        loop()
    except Exception as e:
        print ('Next url is: {}, second chance.'.format(download_url))
        try:
            loop()
        except Exception as e:
            print ('Next url is: {}, last chance.'.format(download_url))
            try:
                loop()
            except Exception as e:
                print ('Next url is: {}, stop here.'.format(download_url))
                raise
            raise
        raise
    finally:
        d = dict(date=date_list, link=link_list, company=company_list, field=field_list, place=place_list,
                 round=round_list, amount=amount_list, investor=investor_list)
        df = DataFrame(d, columns=['date', 'link', 'company', 'field', 'place', 'round', 'amount', 'investor'])
        df.to_csv(r'C:\Users\zluck\Documents\Python\web crawler\full_invest_4.csv', encoding='gb18030')
        end = datetime.datetime.now()
        timespan = end - start
        print ('Done! The process costs {}.'.format(timespan))

if __name__ == '__main__':
    main()






