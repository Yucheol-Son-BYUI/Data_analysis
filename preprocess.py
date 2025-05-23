import pandas as pd

df = pd.read_pickle("raw_data.pkl")

num_people = 32
rows_per_person = 4
date_columns = df.loc[0, 1:]  # 1열은 UID/nickname 자리로 비우고, 2열부터 날짜

data_rows = []

for i in range(num_people):
    base_row = 1 + i * rows_per_person  # 한 사람의 첫 줄
    uid = df.loc[base_row, 0]           # A열: UID
    nickname = df.loc[base_row, 1]      # B열: 닉네임

    for col in range(2, df.shape[1]):  # 날짜 데이터 시작열부터 반복
        date = df.loc[0, col]  # 날짜는 0행에 있음

        evaluation = df.loc[base_row, col]       # 평가 (선택적으로 무시 가능)
        daily = df.loc[base_row + 1, col]
        cumulative = df.loc[base_row + 2, col]
        score = df.loc[base_row + 3, col]

        data_rows.append({
            "UID": uid,
            "nickname": nickname,
            "날짜": date,
            "누적점수": score,
            "누적공적": cumulative,
            "일일공적": daily
        })

# 데이터프레임으로 변환
result_df = pd.DataFrame(data_rows)

# 저장
result_df.to_csv("정리된_데이터.csv", index=False)

