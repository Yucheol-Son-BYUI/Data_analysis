import pandas as pd
import random
# ─── 1) 기존 DataFrame 불러오기 ───────────────────────────────
df = pd.read_csv("preprocessed_data3.csv")
print(len(df))
# 예시: 빈 DataFrame 생성
# df = pd.DataFrame(columns=[
#   'UID','nickname','date',
#   'daily_merit','daily_score',
#   'battle_count','daily_mission','attendance'
# ])

# ─── 2) 사용자 입력 변수 선언 ────────────────────────────────
# daily_merit 값은 mapping key이므로 고정,
# daily_score 값은 실제로 사용자가 입력해야 하므로 None 으로 둡니다.
merit_list = [180, 140, 150, 110, 120, 80, 90, 50, 0]


# ─── 3) 일일공적으로부터 출력(battle_count, daily_mission, attendance) 매핑 정의 ───
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

def generate_score_merit(merit, battle_count):
  # 1) 3000~4600 random
  base_score = random.uniform(3000, 4600)
  total_score = base_score * battle_count

  noise = random.uniform(-0.2, 0.2)
  daily_score = int(total_score * (1 + noise))

  if(daily_score == 0):
    daily_merit = merit
  else:
    daily_merit = merit + int(daily_score*0.1) + random.randint(-2, 2) 
    
  return (daily_merit, daily_score)

# ─── 4) synthetic 데이터 200개씩 생성 ──────────────────────────
records = []
for merit in merit_list:
  bc, dm, att = mapping[merit]
    
  for _ in range(200):
    daily_merit, daily_score = generate_score_merit(merit, bc)
    records.append({
      'UID':             '00000',
      'nickname':        'test_data',
      'date':            '2222-02-22',
      'daily_merit':     daily_merit,
      'daily_score':     daily_score,    # 사용자가 위에서 설정할 값
      'battle_count':    bc,
      'daily_mission':   dm,
      'attendance':      att,
    })

# ─── 5) DataFrame으로 변환 후 기존 df에 추가 ───────────────────
df_synthetic = pd.DataFrame(records)
df = pd.concat([df, df_synthetic], ignore_index=True)

# ─── 6) 결과 확인 및 저장 ─────────────────────────────────────
print(f"추가된 synthetic 행 개수: {len(df_synthetic)}")
print(f"최종 df 행 개수: {len(df)}")
print(df.tail(10))

# 필요 시 CSV로 저장
df.to_csv("preprocessed_data4.csv", index=False)