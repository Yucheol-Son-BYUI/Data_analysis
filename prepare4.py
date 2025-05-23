import pandas as pd

# 1) CSV 불러오기
df = pd.read_csv("final_processed_with_diff.csv")

# 2) 매핑 정의
mapping = {
    180: (3, 1, 1),
    140: (3, 0, 1),
    150: (2, 1, 1),
    110: (2, 0, 1),
    120: (1, 1, 1),
    80:  (1, 0, 1),
    90:  (0, 1, 1),
    50:  (0, 0, 1),
    0:   (0, 0, 0),
}

# 3) 일일공적으로부터 (전투회수, 일일임무, 출석) 뽑아내기
#    mapping에 없는 값은 (0,0,0)으로 처리
df[['전투회수','일일임무','출석']] = (
    df['일일공적']
      .apply(lambda x: mapping.get(int(x), (0,0,0)))
      .apply(pd.Series)
)

# 4) 결과 저장
df.to_csv("final_processed_with_features.csv", index=False)
