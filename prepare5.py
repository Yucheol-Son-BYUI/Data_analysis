import pandas as pd


df = pd.read_csv("final_processed_with_features.csv")

df.drop(['prev_date', 'prev_score', '일일공적', '누적공적', '누적점수'], axis=1, inplace=True)
df.rename(columns={
    '공적차': 'daily_merit',
    '점수차': 'daily_score',
    '전투회수': 'battle_count',
    '일일임무': 'daily_mission',
    '출석': 'attendance',
    '날짜': 'date'
}, inplace=True)

df.to_csv("preprocessed_data.csv", index=False)