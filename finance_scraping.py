import requests
from bs4 import BeautifulSoup
import locale
from selenium import webdriver
import time

def itooza_Scraping(stock_code):
    url = 'http://search.itooza.com/search.htm?seName=' + stock_code + '&jl=&search_ck=&sm=&sd=2020-07-08&ed=2020-08-07&ds_de=&page=&cpv='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    # stockItem > div.item-body > div.ar > div.item-detail > h2 > em > span
    cur_price = soup.select_one('#stockItem > div.item-body > div.ar > div.item-detail > h2 > em > span')
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    price_data = float(locale.atof(cur_price.text))

    per_tag = soup.select_one(
        '#stockItem > div.item-body > div.ar > div.item-data1 > table > tr:nth-child(2) > td:nth-child(1)')
    per_data = per_tag.text

    roe_tag = soup.select_one(
        '#stockItem > div.item-body > div.ar > div.item-data1 > table > tr:nth-child(2) > td:nth-child(3)')
    roe_data = float((roe_tag.text).split('%')[0])

    roe5_tag = soup.select_one(
        '#stockItem > div.item-body > div.ar > div.item-data2 > table > tr:nth-child(2) > td:nth-child(3)')
    roe5_data = float((roe5_tag.text).split('%')[0])

    eps5_tag = soup.select_one(
        '#stockItem > div.item-body > div.ar > div.item-data2 > table > tr:nth-child(2) > td:nth-child(4)')
    eps5_data = float((eps5_tag.text).split('%')[0])

    print(price_data, per_data, roe_data, roe5_data, eps5_data)

def naverfinance_Scraping(stock_code):
    url = 'https://finance.naver.com/item/coinfo.nhn?code='+stock_code+'&target=finsum_more'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    browser = webdriver.Chrome("C:/Users/chromedriver.exe", options=options)
    # browser.maximize_window()

    print("Scraping...wait for seconds...")
    browser.get(url)
    browser.switch_to.frame(browser.find_element_by_id('coinfo_cp'))
    browser.find_elements_by_xpath('//*[@class="schtab"][1]/tbody/tr/td[3]')[0].click()

    time.sleep(2)
    cur_html = browser.page_source
    soup = BeautifulSoup(cur_html, 'html.parser')

    finance_info = soup.find('table',{'class':'gHead01 all-width','summary':'주요재무정보를 제공합니다.'})
    tbody = finance_info.find('tbody')
    trs = tbody.find_all('tr')

    # 콤마 형태의 숫자를 소수점 형태로 변환하기 위함
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    # 영업이익
    operating_income_datas = []
    datas_info = trs[1].find_all('td')
    for data in datas_info:
        if data.text is not None:
            operating_income_datas.append(float(locale.atof(data.text)))
    print(operating_income_datas)
    
    # 당기순이익(지배)
    net_income_datas = []
    datas_info = trs[5].find_all('td')
    for data in datas_info:
        if data.text is not None:
            net_income_datas.append(float(locale.atof(data.text)))
    print(net_income_datas)

    # for tr in trs :
    #     print(tr)

    browser.quit()

stock_code = '000100'
# itooza_Scraping(stock_code)
naverfinance_Scraping(stock_code)

