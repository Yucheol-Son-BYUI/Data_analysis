import pandas as pd
from datetime import datetime, timedelta

# 1) 원본 CSV 불러오기
df = pd.read_csv("edited.csv")

# 2) 그룹 크기 및 컬럼 리스트 준비
group_size = 10
cols = list(df.columns)
num_groups = (len(cols) + group_size - 1) // group_size

records = []

# 3) 묶음별 순회
for g in range(num_groups):
    start = g * group_size
    end   = start + group_size
    group_cols = cols[start:end]
    
    name_col = group_cols[0]   # 닉네임
    uid_col  = group_cols[1]   # UID
    base_date_col = group_cols[3]  # 첫 번째 날짜 열
    # 이후 실제 날짜들
    date_cols = [c for c in group_cols[3:] 
                 if isinstance(c, str) and c[:4].isdigit()]
    date_cols.sort(key=lambda x: datetime.strptime(x.split()[0], "%Y-%m-%d"))
    
    # 4행 단위로 한 사람씩
    for i in range(0, len(df), 4):
        name = df.at[i, name_col]
        uid  = df.at[i, uid_col]
        if pd.isna(name) or pd.isna(uid):
            continue
        
        # —— 3열(원점수) 처리: 첫 번째 날짜 열의 하루 전 날짜
        try:
            raw_prev = base_date_col.split()[0]
            prev_date = (datetime.strptime(raw_prev, "%Y-%m-%d") - timedelta(days=1)) \
                        .strftime("%Y-%m-%d")
            records.append({
                "UID":      uid,
                "nickname": name,
                "날짜":     prev_date,
                "누적공적": df.at[i+2, group_cols[2]],  # 3열의 누적공적
                "누적점수": df.at[i+3, group_cols[2]],  # 3열의 누적점수
                "일일공적": pd.NA                     # 평가·일일공적은 없음
            })
        except Exception:
            pass
        
        # —— 나머지 날짜들 처리
        for d in date_cols:
            records.append({
                "UID":      uid,
                "nickname": name,
                "날짜":     d.split()[0],
                "누적공적": df.at[i+2, d],
                "누적점수": df.at[i+3, d],
                "일일공적": df.at[i+1, d],
            })

# 4) DataFrame 변환 및 NaN→0
final_df = pd.DataFrame(records).fillna(0)

# 5) CSV로 저장
final_df.to_csv("final_processed.csv", index=False)
