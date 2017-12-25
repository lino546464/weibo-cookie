
from selenium import webdriver
import time
import requests
from lxml import etree
import json
import re


headers = {
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

def get_cookie(url):
    # driver = webdriver.PhantomJS()
    # data = driver.page_source
    driver = webdriver.Firefox()
    driver.get(url)
    # driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[2]/span').click()
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="loginName"]').send_keys('*******@qq.com')
    driver.find_element_by_xpath('//*[@id="loginPassword"]').send_keys('*********')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="loginAction"]').click()
    time.sleep(1)
    # driver.add_cookie(driver.get_cookies())
    print(driver.get_cookies())
    cookies = {}
    for cookie in driver.get_cookies():
        name = cookie['name']
        value = cookie['value']
        cookies[name] = value

    print(cookies)
    return cookies

def get_name(url,cookies=None):
    data = requests.get(url, headers=headers,cookies=cookies)
    # time.sleep(3)
    # data = driver.page_source
    # print(data.title())
    html = etree.HTML(data.text)
    name = html.xpath('//*[@id="boxId_1514167735653_1"]/div[1]/div[1]/div/p/text()')
    print(name)
    topics = html.xpath('//div[@class="weibo-og"]')
    for t in topics:
        title = t.xpath('div[@class="weibo-text"]/text()')
        # context = t.xpath('section/p/text()')
        print(title)

def ajax_requsets(ajax_url,cookies=None):
    data = requests.get(ajax_url,cookies=cookies,headers=headers)
    print(data.content)
    content = json.loads(data.content)
    print(content)
    # if data in content.keys():
    title = content.get('data').get('cards')
    print(title)
    for it in title:
        text = it.get('mblog').get('text')
        texts = re.sub('<.*?>','',text)
        print(texts)


if __name__ == '__main__':
    login_url = 'https://passport.weibo.cn/signin/login'
    cookies = get_cookie(login_url)
    name_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=1713926427&containerid=1076031713926427&page=2'
    # get_name(name_url,cookies)
    ajax_requsets(name_url,cookies)
