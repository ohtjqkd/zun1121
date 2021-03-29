from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import RelativeBy
import re
import scrapper.scrapper as scrapper
comp = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
comp = '[a-zA-Z0-9_]+\@[a-zA-Z0-9_]+\.+[a-zA-Z0-9-.]+'
result_obj_model = {
    "company_name":"String",
    "location":"String",
    "homepage":"String",
    "email":"String"
}

def jobkoreaScrap(keyword):
    params = {
        "root_url":"https://www.jobkorea.co.kr",
        "page_url":f"/Search/?stext={keyword}&tabType=recruit&Page_No=",
        "list_class":{
            "selector":"css_all",
            "value": ".recruit-info .lists .lists-cnt .list-default .clear .list-post .post a.name"
        },
        "each": {
            "selector":"css",
            "info_page": {
                "selenium":False,
                "javascript":False,
                "params": [
                    {
                        "name":"url",
                        "selector":{
                            "by":"css",
                            "value":"div.coBtn a.girBtn.girBtn_3"
                        },
                        "attr":"href"
                    }
                ]
            },
            "info": {
                "selenium":False,
                "javascript":False,
                "params": [
                    {
                        "name":"company",
                        "selector":{
                            "by":"xpath",
                            "value":"//div[@class='company-header-branding-body']/div[@class='name']/text()"
                        },
                        "attr":0
                    },
                    {
                        "name":"homepage",
                        "selector":{
                            "by":"xpath",
                            "value":"//th[text()='홈페이지']/following-sibling::td/div/div/a/@href"
                        },
                        "attr":0
                    },
                    {
                        "name":"address",
                        "selector": {
                            "by":"xpath",
                            "value":"//th[text()='주소 ']/following-sibling::td/div/div[@class='value']/text()"
                        },
                        "attr":0
                    }
                ]
            },
            "email":{
                "iframe":{
                    "selector":{
                        "by":By.ID,
                        "value":"gib_frame"
                    }
                },
                "params": [
                    {
                        "name":"email",
                        "selector":{
                            "by":By.CSS_SELECTOR,
                            "value":".devChargeEmail"
                        },
                        "attr":"href"
                    }
                ]
            }
        }
    }
    return scrapper.scrap(params)

def saraminScrap(keyword):
    ##after searching by keyword, each page should be opened by selenium
    params = {
        "root_url":"https://www.saramin.co.kr",
        "page_url":f"/zf_user/search/recruit?search_area=main&search_done=y&search_optional_item=n&searchType=search&searchword={keyword}&recruitSort=relation&recruitPageCount=40&inner_com_type=&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10&quick_apply=&except_read=&recruitPage=",
        "list_class":{
            "selector":"css",
            "value": "#recruit_info_list .content .item_recruit .corp_name>a"
        },
        "each": {
            "selector":"css",
            "info_page": {
                "selenium":True,
                "javascript":True,
                "params": [
                    {
                        "name":"url",
                        "selector":{
                            "by":By.CSS_SELECTOR,
                            "value":"a.company"
                        },
                        "attr":"href"
                    }
                ]
            },
            "info": {
                "selenium":True,
                "javascript":True,
                "params": [
                    {
                        "name":"company",
                        "selector":{
                            "by":By.CSS_SELECTOR,
                            "value":".company_name.recruiting .name"
                        },
                        "attr":"innerHTML"
                    },
                    {
                        "name":"homepage",
                        "selector":{
                            "by":By.XPATH,
                            "value":"//dt[text()='홈페이지']/following-sibling::dd/a"
                        },
                        # "tag":"dd",
                        # "locate":"below",
                        "attr":"href"
                    },
                    {
                        "name":"address",
                        "selector": {
                            "by":By.XPATH,
                            "value":"//dt[text()='기업주소']/following-sibling::dd"
                        },
                        # "tag":"dd",
                        # "locate":"below",
                        "attr":"innerText"
                    }
                ]
            },
            "email":{
                "iframe":{
                    "selector":{
                        "by":By.CSS_SELECTOR,
                        "value":"iframe.iframe_content"
                    }
                },
                "params": [
                    {
                        "name":"email",
                        "selector":{
                            "by":By.TAG_NAME,
                            "value":"html",
                            "pattern":re.compile(r'[a-zA-Z0-9._]+\@+[a-zA-Z0-9._]+\.[a-z.]*')
                        },
                        "attr":"innerText"
                    }
                ]
            }
        }
    }
    return scrapper.scrap(params)
    

