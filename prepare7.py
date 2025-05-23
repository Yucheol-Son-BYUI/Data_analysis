# remove outliers manually
import pandas as pd
from tabulate import tabulate

df = pd.read_csv("preprocessed_data2.csv")

deleted_indices = []
chunk_size = 5
n_rows = len(df)

for start in range(0, n_rows, chunk_size):
    end = min(start + chunk_size, n_rows)
    chunk = df.iloc[start:end]

    print(f"\nRows {start}–{end-1} (총 {n_rows}행 중):")
    print(tabulate(chunk, headers='keys', tablefmt='psql', showindex=True))

    to_delete = input("삭제할 행 번호를 쉼표로 입력 (건너뛰려면 엔터): ")
    if to_delete.strip():
        try:
            nums = [int(x.strip()) for x in to_delete.split(',')]
            for j in nums:
                if 0 <= j < len(chunk):
                    deleted_indices.append(chunk.index[j])
                else:
                    print(f"잘못된 번호 건너뜀: {j}")
        except ValueError:
            print("숫자를 쉼표로 구분해서 입력하세요. 해당 묶음 건너뜁니다.")

# 3) 실제 삭제 및 인덱스 리셋
if deleted_indices:
    df_clean = df.drop(index=deleted_indices).reset_index(drop=True)
    print(f"\n 삭제된 전역 인덱스: {deleted_indices}")
else:
    df_clean = df.copy()
    print("\n 삭제된 행이 없습니다.")

# 4) 결과 확인
print(f"\n최종 데이터 (총 {len(df_clean)}행):")
print(tabulate(df_clean, headers='keys', tablefmt='psql', showindex=False))

df_clean.to_csv("preprocessed_data3.csv", index=False)
