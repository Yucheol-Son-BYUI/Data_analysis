import pandas as pd
from tabulate import tabulate

# df = pd.read_csv("edited.csv")
# print(df.head(10))

# CSV 파일 불러오기
df = pd.read_csv("preprocessed_data3.csv")
print(df)

chunk_size = 5
total_rows = len(df)

for start in range(0, total_rows, chunk_size):
  end = min(start + chunk_size, total_rows)
  chunk = df.iloc[start:end]
  
  # 헤더와 데이터가 열 너비에 맞춰 정렬된 테이블 출력
  print(f"\n📄 행 {start}–{end-1} (총 {total_rows}행 중):")
  print(tabulate(chunk, headers='keys', tablefmt='github', showindex=False))
  print("-" * 50)
  
  input("계속하려면 엔터 키를 누르세요…")
