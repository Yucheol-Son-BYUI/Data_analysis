import pandas as pd
import random

df = pd.read_csv("preprocessed_data4.csv")
print(len(df))

merit_list = [180, 140, 150, 110, 120, 80, 90, 50, 0]


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

# ─── 4) generate 1000 data per merit-map ──────────────────────────
records = []
for merit in merit_list:
  bc, dm, att = mapping[merit]
    
  for _ in range(1000):
    daily_merit, daily_score = generate_score_merit(merit, bc)
    records.append({
      'UID':             '00000',
      'nickname':        'test_data',
      'date':            '2222-02-22',
      'daily_merit':     daily_merit,
      'daily_score':     daily_score,
      'battle_count':    bc,
      'daily_mission':   dm,
      'attendance':      att,
    })

# ─── 5) add to target df ───────────────────
df_synthetic = pd.DataFrame(records)
df = pd.concat([df, df_synthetic], ignore_index=True)

# ─── 6) check result ─────────────────────────────────────
print(f"추가된 행 개수: {len(df_synthetic)}")
print(f"최종 df 행 개수: {len(df)}")
print(df.tail(10))

df.to_csv("preprocessed_data5.csv", index=False)