import pandas as pd

# 1) CSV 불러오기
df = pd.read_csv("final_processed.csv")

# 2) 날짜를 datetime으로 변환하고 정렬
df['날짜'] = pd.to_datetime(df['날짜'])
df = df.sort_values(['nickname', '날짜'])

# 3) 공적차·점수차 계산 (첫날 diff는 NaN → -1)
df['공적차'] = df.groupby('nickname')['누적공적'] \
               .diff() \
               .fillna(-1) \
               .astype(int)
df['점수차'] = df.groupby('nickname')['누적점수'] \
               .diff() \
               .fillna(-1) \
               .astype(int)

# 4) 날짜 포맷 다시 문자열로, 컬럼 순서 재배치
df['날짜'] = df['날짜'].dt.strftime('%Y-%m-%d')
cols = ['UID', 'nickname', '날짜', '누적공적', '공적차', '누적점수', '점수차', '일일공적']
df = df[cols]

import pandas as pd

df['날짜'] = pd.to_datetime(df['날짜'])
df = df.sort_values(['nickname','날짜'])

# 바로 이전 행의 날짜와 누적점수
df['prev_date']   = df.groupby('nickname')['날짜'].shift(1)
df['prev_score']  = df.groupby('nickname')['누적점수'].shift(1)

# 날짜 차이가 정확히 1일인 경우만 diff, 아니면 -1
df['점수차'] = df.apply(
    lambda x: int(x['누적점수'] - x['prev_score'])
              if (x['prev_date'] is not pd.NaT and 
                  (x['날짜'] - x['prev_date']).days == 1)
              else -1,
    axis=1
)

# 5) 새 파일로 저장
df.to_csv("final_processed_with_diff.csv", index=False)

print("✅ 'final_processed_with_diff.csv' 생성 완료!")
