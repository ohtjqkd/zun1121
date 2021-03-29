import pandas, datetime

def download(keyword, contents):
  now = datetime.datetime.now().strftime("%Y-%m-%d-%h-%m")
  df = pandas.DataFrame(contents)
  df['company'] = df['company'].apply(lambda x: x.strip())
  df['address'] = df['address'].apply(lambda x: x.replace(" 지도보기", ""))
  df['email'] = df['email'].apply(lambda x: x.replace("mailto:", ""))
  try:
    df.to_csv(path_or_buf=f'{now}_{keyword}.csv', encoding="utf-8-sig")
  except:
    print("다운로드 실패")
    return False

  return True