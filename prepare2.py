import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv("edited.csv")

group_size = 10
cols = list(df.columns)
num_groups = (len(cols) + group_size - 1) // group_size

records = []

for g in range(num_groups):
    start = g * group_size
    end   = start + group_size
    group_cols = cols[start:end]
    
    name_col = group_cols[0]   # nickname
    uid_col  = group_cols[1]   # UID
    base_date_col = group_cols[3]  # date column
    # actual_data 
    date_cols = [c for c in group_cols[3:] 
                 if isinstance(c, str) and c[:4].isdigit()]
    date_cols.sort(key=lambda x: datetime.strptime(x.split()[0], "%Y-%m-%d"))
    
    # 1 person take 4 rows
    for i in range(0, len(df), 4):
        name = df.at[i, name_col]
        uid  = df.at[i, uid_col]
        if pd.isna(name) or pd.isna(uid):
            continue
        
        # —— original score to be compared to real score
        try:
            raw_prev = base_date_col.split()[0]
            prev_date = (datetime.strptime(raw_prev, "%Y-%m-%d") - timedelta(days=1)) \
                        .strftime("%Y-%m-%d")
            records.append({
                "UID":      uid,
                "nickname": name,
                "날짜":     prev_date,
                "누적공적": df.at[i+2, group_cols[2]],  
                "누적점수": df.at[i+3, group_cols[2]], 
                "일일공적": pd.NA                     
            })
        except Exception:
            pass
        
        # actual data
        for d in date_cols:
            records.append({
                "UID":      uid,
                "nickname": name,
                "날짜":     d.split()[0],
                "누적공적": df.at[i+2, d],
                "누적점수": df.at[i+3, d],
                "일일공적": df.at[i+1, d],
            })

final_df = pd.DataFrame(records).fillna(0)

final_df.to_csv("final_processed.csv", index=False)
