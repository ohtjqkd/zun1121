import pandas, datetime

def download(keyword, contents):
  now = datetime.datetime.now().strftime("%Y-%m-%d-%h-%M")
  df = pandas.DataFrame(contents)
  df['company'] = df['company'].apply(lambda x: x.strip() if x else x)
  df['homepage'] = df['homepage'].apply(lambda x: x.strip() if x else x)
  df['address'] = df['address'].apply(lambda x: x.replace(" 지도보기", "") if x else x)
  df['email'] = df['email'].apply(lambda x: [mail.replace("mailto:","") for mail in x] if x else x)
  try:
    df.to_csv(path_or_buf=f'{now}_{keyword}.csv', encoding="utf-8-sig")
    print("다운로드 완료")
  except:
    print("다운로드 실패")
    return False

  return True