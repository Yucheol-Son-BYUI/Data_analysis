import pandas as pd

df = pd.read_csv("preprocessed_data5.csv")
df['essential_merit'] = (df['daily_merit'] - df['daily_score'] * 0.1).astype(int)

df.to_pickle("preprocessed_data6.pkl")