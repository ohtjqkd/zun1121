import scrapper.homepageScrapper as homepageScrapper
import datetime
import downloader
import time

import pandas

while True:
    try:
        print("검색어를 입력해주세요. 종료하시려면 'exit'를 입력해주세요.")
        keyword = input()
        if keyword == "exit":
            break
        result = homepageScrapper.saraminScrap(keyword)
        # result = homepageScrapper.jobkoreaScrap(keyword)
        print("데이터 수집완료. csv파일 다운로드를 시작합니다.")
        downloader.download(keyword, result)
        print("다운로드 완료")
        # df.to_csv(path_or_buf="test.csv", encoding="utf-8-sig")
    except Exception as e:
        print(e)
        time.sleep(10)
        break
