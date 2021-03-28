from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.webdriver import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import with_tag_name
import time
import requests
from bs4 import BeautifulSoup
import random
import os
import re
comp = re.compile(r"[a-zA-Z0-9._]+\@+[[a-zA-Z0-9._]+.[a-z]")


def getBySelenium(keyword):
    jobKr_url = "http://www.jobkorea.co.kr/"
    search_q = f"Search/?stext={keyword}"
    # Start the driver
    with webdriver.Chrome() as driver:
        # Open URL
        page = 1
        # while 
        f'http://www.jobkorea.co.kr/Search/?stext={keyword}&Page_No={page}'
        driver.get(jobKr_url + search_q)

        # Setup wait for later
        wait = WebDriverWait(driver, 5)
        time.sleep(10)

        # Store the ID of the original window
        original_window = driver.current_window_handle
        print("when")
        # Check we don't have other windows open already
        # assert len(driver.window_handles) == 1

        # Click the link which opens in a new window
        print("start get job_list")
        company_li = driver.find_element_by_css_selector(".title.dev_view")
        print("finish get job_list")
        for com in company_li:
            print(com.text)

        # Wait for the new window or tab
        # wait.until(EC.number_of_windows_to_be(2))

        # Loop through until we find a new window handle
        # for window_handle in driver.window_handles:
        #     if window_handle != original_window:
        #         driver.switch_to.window(window_handle)
        #         break

        # Wait for the new tab to finish loading content
        # wait.until(EC.title_is("Selenium documentation"))

my_headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'accept-language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':'gzip, deflate',
    'Upgrade-Insecure-Requests': '1',
    'referer':'http://210.222.27.5/',
}

def getUrlJob(page_url, list_class):
    job_url_list = []
    print(f"Get Url")
    page = 1
    while page<2:
        list_url = f'{page_url}{page}'
        time.sleep(random.randint(5, 10))
        print(list_url)
        job_res = requests.get(list_url, headers = my_headers)
        soup = BeautifulSoup(job_res.text, "html.parser")
        job_list = soup.select(list_class.get("value"))
        print("IS EXIST?")
        if len(job_list) == 0:
            print("No")
            break
        print("YES")
        for job in job_list:
            job_url_list.append(job.get('href'))
        page += 1
    return job_url_list

def getDataByUrl(root_url, page_url, params):
    data = {}
    page_url = root_url+page_url
    info_page = params.get('info_page')
    if info_page.get('selenium'):
        info_page_url = getDataBySel({}, page_url, info_page)['url']
    else:
        # info_page_res = requests.get(page_url)
        # soup = BeautifulSoup(info_page_res.text, "html.parser")
        # print(soup.select_one(".coBtn .girBtn.girBtn_3")['href'])
        info_page_url = getDataByBs({}, requests.get(page_url), info_page.get('params'))['url']
    if info_page_url[:4] != "http":
        info_page_url = root_url + info_page_url
    print(info_page_url)
    # info_page_res = requests.get(info_page_url)
    # info_page_soup = BeautifulSoup(info_page_res.text, "html.parser")
    
    #get Email address
    getDataBySel(data, page_url, params.get('email'))
    
    info = params.get('info')
    if info.get('selenium'):
        infos = getDataBySel(data, info_page_url, info)
        # company_name, address, homepage = infos['company'], infos['address'], infos['homepage']
    else:
        infos = getDataByBs(data, requests.get(info_page_url), info.get('params'))
        # company_param = params.get('company')
        # if company_param.get('selector') == 'css':
        #     company_name = info_page_soup.select_one(company_param.get('value')).text
        # elif company_param.get('selector') == 'find':
        #     company_name = info_page_soup.find(company_param.get('value')).text

        # homepage_param = params.get('homepage')
        # if homepage_param.get('selector') == 'css':
        #     homepage = info_page_soup.select_one(homepage_param.get('value'))['href']
        # elif homepage_param.get('selector') == 'find':
        #     homepage = info_page_soup.find(homepage_param.get('value'))
        #     if homepage_param.get('value').get('locate') == 'after':
        #         homepage = homepage.next_sibling['href']

        # address_param = params.get('address')
        # if address_param.get('selector') == 'css':
        #     address = info_page_soup.select_one(address_param.get('value')).text
        # elif address_param.get('selector') == 'find':
        #     address = info_page_soup.find(address_param.get('value'))
        #     if address_param.get('value').get('locate') == 'after':
        #         address = address.next_sibling.text
        # getDataBySel({
        #     "iframe":
        # })        
    # print(company_name, homepage, address, email)
    
    # email_tag = page_soup.select_one('a.devChargeEmail')
    # email = email_tag['href'] if email_tag else getEmailBySel(url)
    # if email:
        # print(companyName, homepage, email)
    # data = [company_name, homepage, email, address]
    print('data--------------------------------------------------------------------->')
    print(data)
    return data

def getDataBySel(data, url, params):
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    option.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
    with webdriver.Chrome(options=option) as driver:
        driver.implicitly_wait(time_to_wait=30)
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
        driver.quit()
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
            print(param['name'])
            print(e)
            data[param['name']] = None            
    return data

def getElementBySel(data, driver, params):
    for param in params:
        try:
            target = driver.find_element(param.get('selector').get('by'), param.get('selector').get('value'))
            if param.get('selector').get('pattern'):
                print('by compiler')
                data[param['name']] = param.get('selector').get('pattern').findall(target.text) if __ != [] else None
            else:
                data[param['name']] = target.get_attribute(param.get('attr'))
        except Exception as e:
            print(param['name'])
            print(e)
            data[param['name']] = None
            continue


def scrap(params):
    root_url = params.get("root_url")
    page_url = params.get("page_url")
    result = []
    url_list = getUrlJob(f'{root_url}{page_url}', list_class=params.get("list_class"))
    for idx, url in enumerate(url_list):
        result.append(getDataByUrl(root_url, url, params.get("each")))
    return result

def testSel(url):
    option = webdriver.ChromeOptions()
    option.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")
    with webdriver.Chrome(chrome_options=option) as driver:
        driver.get(url)
        driver.implicitly_wait(10)
        iframe = driver.find_element(by=By.CSS_SELECTOR, value='iframe.iframe_content')
        driver.switch_to.frame(iframe)
        html = driver.find_element(By.TAG_NAME,'html')
        # email = driver.find_element(By.XPATH, "//*[text()[contains(.,match(@text,'[a-zA-Z0-9_]+\@[a-zA-Z0-9_]+\.+[a-zA-Z0-9-.]+'))]]")
        html = html.text
        comp = re.compile(r"[a-zA-Z0-9._]+\@+[a-zA-Z0-9._]+.[a-z]")
        comp.search(html)
        result = comp.search(html)
        result = comp.findall(html)
        # result = re.match(comp, html)
        print(html)
        # print(type(html))
        print(result)
        # print(email.text)
        # print(html.text)
        # dt = driver.find_element(By.XPATH, "//dt[text()='기업주소']/following-sibling::dd")
        # print(dt.get_attribute('innerHTML'))
        # print(dt.get_attribute('outerHTML'))
        # print(dt.get_attribute('innerText'))

# mobizen = "https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx=39860876&recommend_ids=eJxdkMkVAzEIQ6vJHQxI%2BJxC3H8X8cTrm%2BM3khC2mikF1uj88GsXNh8PhBlb1ImgsnTEC5dcIKxHHhCVHjfkpKuiQcpAJLU21BxiDTcc78aVnRnyVIk%2FRhUr1t2zivTAvhn6wummhaSd9OKK65CNS97baew40I2xDznYzqHIPT8456Cx2OVfuP2eV%2F7B7XeI3%2FsnrrowpTyf8QOLiWey&view_type=list&gz=1&t_ref_content=ing_recruit&t_ref=company_info_view#seq=0"
# url = "https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx=39826805&recommend_ids=eJxdkMkVwyAMRKvJXftI5xRC%2F13EfiYIfPxIswitzAzk8PIPvlqpCPcBixcOex7K3HKA9IVzjmCQX3ZTb1TY7O51OdWyqROpnls6XxuNWSrSVRd2t4rDfeJ%2FniCu1js5o93dDJ2NYoasQ6CkjoXOwlp9ZjllreRgJrNlFSYssX9CZRw1Hxz2AyjUWFw%3D&view_type=list&gz=1&t_ref_content=general&t_ref=headhunting#seq=0"
# testSel(mobizen)