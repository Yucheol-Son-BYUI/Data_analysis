#remove outlier
import pandas as pd

df = pd.read_csv("preprocessed_data2.csv")

df_clean = df[df['daily_score'] >= 0].reset_index(drop=True)

print(f"삭제 전 행 개수: {len(df)}")
print(f"삭제 후 행 개수: {len(df_clean)}")

df_clean.to_csv("preprocessed_data2.csv", index=False)
