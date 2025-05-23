import pandas as pd

df = pd.read_csv("final_processed.csv")

df['날짜'] = pd.to_datetime(df['날짜'])
df = df.sort_values(['nickname', '날짜'])

df['공적차'] = df.groupby('nickname')['누적공적'] \
               .diff() \
               .fillna(-1) \
               .astype(int)
df['점수차'] = df.groupby('nickname')['누적점수'] \
               .diff() \
               .fillna(-1) \
               .astype(int)

df['날짜'] = df['날짜'].dt.strftime('%Y-%m-%d')
cols = ['UID', 'nickname', '날짜', '누적공적', '공적차', '누적점수', '점수차', '일일공적']
df = df[cols]

import pandas as pd

df['날짜'] = pd.to_datetime(df['날짜'])
df = df.sort_values(['nickname','날짜'])

df['prev_date']   = df.groupby('nickname')['날짜'].shift(1)
df['prev_score']  = df.groupby('nickname')['누적점수'].shift(1)

df['점수차'] = df.apply(
    lambda x: int(x['누적점수'] - x['prev_score'])
              if (x['prev_date'] is not pd.NaT and 
                  (x['날짜'] - x['prev_date']).days == 1)
              else -1,
    axis=1
)

df.to_csv("final_processed_with_diff.csv", index=False)

