import pandas as pd

df = pd.read_pickle("edited.pkl")

# interactive column deletion
step = 5
cols = df.columns.tolist()
deleted_cols = []

i = 0
while i < len(cols):
    current_chunk = cols[i:i+step]
    print("\n현재 열 그룹:")
    for idx, col in enumerate(current_chunk):
        print(f"  {idx}: {col}")

    to_delete = input("삭제할 열 번호를 쉼표로 입력하세요 (건너뛰려면 엔터): ")
    if to_delete.strip():
        try:
            indices = [int(x.strip()) for x in to_delete.split(',')]
            drop_cols = [current_chunk[j] for j in indices if 0 <= j < len(current_chunk)]
            df = df.drop(columns=drop_cols)
            deleted_cols.extend(drop_cols)
        except ValueError:
            print("잘못된 입력입니다. 숫자를 쉼표로 구분해서 입력하세요.")
    i += step

df.to_pickle("edited.pkl")