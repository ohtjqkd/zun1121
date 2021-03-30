from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time, requests, random, re, sys, os, urllib3


my_headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'accept-language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':'gzip, deflate',
    'Upgrade-Insecure-Requests': '1',
    'referer':'http://210.222.27.5/',
}

def makeDriver():
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    option.add_argument("--silent")
    option.add_argument("--disable-logging")
    option.add_argument("--log-level=3")
    option.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
    driver = webdriver.Chrome(executable_path=os.path.join(sys._MEIPASS, "chromedriver.exe"), options=option) if getattr(sys, 'frozen', False) else webdriver.Chrome(options=option)
    driver.implicitly_wait(time_to_wait=5)
    return driver

def getUrlJob(page_url, list_class):
    job_url_list = []
    page = 1
    
    print("원하시는 검색건수를 입력해주세요. 입력하지 않으시면 모든 페이지를 검색합니다.")
    cnt = input()
    cnt = int(cnt) if cnt != "" else float('inf')
    print(f"Start Crwaling")
    while True:
        try:
            list_url = f'{page_url}{page}'
            time.sleep(random.randint(5, 10))
            job_res = requests.get(list_url, headers = my_headers)
            soup = BeautifulSoup(job_res.text, "html.parser")
            job_list = soup.select(list_class.get("value"))
            print(f'<---------------{page} page scrapped--------------->', flush=True )
            if len(job_list) == 0:
                print("No more job")
                break
            for job in job_list:
                job_url_list.append(job.get('href'))
            if len(job_url_list) >= cnt:
                break
            page += 1
        except Exception as e:
            print(e, flush=True)
    return job_url_list

def getDataByUrl(root_url, page_url, params, driver):
    data = {}
    page_url = root_url+page_url
    info_page = params.get('info_page')
    if info_page.get('selenium'):
        info_page_url = getDataBySel({}, page_url, info_page, driver)['url']
    else:
        info_page_url = getDataByBs({}, requests.get(page_url), info_page.get('params'))['url']
    if info_page_url[:4] != "http":
        info_page_url = root_url + info_page_url

    info = params.get('info')
    if info.get('selenium'):
        getDataBySel(data, info_page_url, info, driver)
    else:
        getDataByBs(data, requests.get(info_page_url), info.get('params'))
    #get Email address
    getDataBySel(data, page_url, params.get('email'), driver)
    print('data--------------------------------------------------------------------->', flush=True)
    print(data, flush=True)
    return data

def getDataBySel(data, url, params, driver):
    # option = webdriver.ChromeOptions()
    # option.add_argument("--headless")
    # option.add_argument("--silent")
    # option.add_argument("--disable-logging")
    # option.add_argument("--log-level=3")
    # option.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
    # with webdriver.Chrome(executable_path=os.path.join(sys._MEIPASS, "chromedriver.exe"), options=option) if getattr(sys, 'frozen', False) else webdriver.Chrome(options=option) as driver:
        # driver.implicitly_wait(time_to_wait=5)
    driver.get(url)
    isIframe = params.get('iframe')
    if isIframe:
        selector = isIframe.get('selector')
        iframe_content = driver.find_element(selector.get('by'), selector.get('value'))
        driver.switch_to.frame(iframe_content)
        params = params.get('params')
        getElementBySel(data, driver, params)
    else:
        params = params.get('params')
        getElementBySel(data, driver, params)
        # driver.quit()
    return data

def getDataByBs(data, res, params):
    soup = BeautifulSoup(res.text, 'html.parser')
    root = html.fromstring(res.text)
    for param in params:
        try:
            if param.get('selector').get('by') == 'css':
                element = soup.select_one(param.get('selector').get('value'))
                data[param['name']] = element[param.get('attr')]
            elif param.get('selector').get('by') == 'xpath':
                element = root.xpath(param.get('selector').get('value'))[param.get('attr')]
                data[param['name']] = element
        except Exception as e:
            print(f'{param["name"]} doesn\'t not exist', flush=True)
            print(e, flush=True)
            data[param['name']] = None            
    return data

def getElementBySel(data, driver, params):
    for param in params:
        try:
            target = driver.find_element(param.get('selector').get('by'), param.get('selector').get('value'))
            if param.get('selector').get('pattern'):
                element = param.get('selector').get('pattern').findall(target.text)
                data[param['name']] = element if element != [] else None
            else:
                data[param['name']] = target.get_attribute(param.get('attr'))
        except Exception as e:
            print(f'{param["name"]} doesn\'t not exist', flush=True)
            print(e, flush=True)
            data[param['name']] = None
            continue


def scrap(params):
    root_url = params.get("root_url")
    page_url = params.get("page_url")
    result = []
    url_list = getUrlJob(f'{root_url}{page_url}', list_class=params.get("list_class"))
    with makeDriver() as driver:
        for idx, url in enumerate(url_list):
            try:
                result.append(getDataByUrl(root_url, url, params.get("each"), driver))
            except Exception as e:
                print(e, flush=True)
                continue
    return result