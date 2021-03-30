import scrapper.homepageScrapper as homepageScrapper
import downloader
import time


while True:
    try:
        print("검색어를 입력해주세요. 종료하시려면 'exit'를 입력해주세요.")
        keyword = input()
        if keyword == "exit":
            break
        result = homepageScrapper.saraminScrap(keyword)
        # result = homepageScrapper.jobkoreaScrap(keyword)
        print("데이터 수집완료. csv파일 다운로드를 시작합니다.")
        try:
            downloader.download(keyword, result)
        except Exception as e:
            print(e)
            print("다운로드 실패")
        
    except Exception as e:
        print(e)
        print("에러발생. 개발자에게 연락하시고 종료하시려면 'exit'를 입력해주세요.")
        command = input()
        if command == 'exit':
            break
