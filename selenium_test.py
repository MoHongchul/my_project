from selenium import webdriver
driver = webdriver.Chrome('C:/Users/chromedriver.exe')

from bs4 import BeautifulSoup

keyword = '코끼리'
url = 'https://www.google.com/search?q='+keyword+'&hl=ko&sxsrf=ACYBGNSTW5YFeVU0I4abA6H_bXsmwJ-gag:1582014089814&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj7kune1drnAhXaAYgKHQY3CwkQ_AUoAXoECBUQAw&biw=1440&bih=712'

driver.get(url)

req = driver.page_source

soup = BeautifulSoup(req, 'html.parser')

images = soup.select('#islrg > div.islrc > div')

for count, image in enumerate(images):
    img = image.select_one('img')
    print(img['data-iml'])
    if count == 5:
        break

driver.close()