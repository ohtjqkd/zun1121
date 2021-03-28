import homepageScrapper
import downloader
import requests
import scrapper
keyword = input()
# print(scrapper.scrapJobKr(keyword))
# print(scrapper.testSel('https://www.saramin.co.kr/zf_user/company-info/view?csn=ZFFwTDRyK3dRNklvY2c2dS9TQWVFZz09&popup_yn=y'))
print(homepageScrapper.saraminScrap(keyword))
# print(homepageScrapper.jobkoreaScrap(keyword))
# print(requests.get("https://www.saramin.co.kr/zf_user/jobs/relay/view?isMypage=no&rec_idx=39538120&recommend_ids=eJxNz0EOBCEIRNHTzB4KLGDdB%2FH%2Btxg7Jg3unnxjsKIlwjYFv3hscPu9WJDqeYB%2BZuG8tCD8I1927AUdXMzzfi%2FqpWYxPtIrQpop53Qs5x9vZobmiE0w4jL46n9TltdY0ROTC6ojViJ6BSojO66E8%2BUfBFlENA%3D%3D&view_type=search&searchword=javascript&searchType=search&gz=1&t_ref_content=generic&t_ref=search&paid_fl=n#seq=0").text)
# print(getBySelenium(keyword))