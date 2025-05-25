import pandas as pd
import numpy as np
import tensorflow as tf
import pickle
from tabulate import tabulate
import time

model_name = 'model9_onehot_hidden_trained'
with open(model_name + '.pkl', 'rb') as f:
    model = pickle.load(f)

df = pd.read_pickle("preprocessed_data6.pkl")
df['essential_merit'] = df['essential_merit'].round(-1).astype('int32')

categories = [0,50,80,90,110,120,140,150,180]
idx_map    = {v:i for i,v in enumerate(categories)}
indices    = df['essential_merit'].map(idx_map).values
X_all      = tf.one_hot(indices, depth=9).numpy().astype('float32')

y_battle   = df['battle_count'].values.astype('int32')
y_mission  = df['daily_mission'].values.astype('int32')
y_att      = df['attendance'].values.astype('int32')

N = 800
X_sub  = X_all[:N]
yb_sub = y_battle[:N]
ym_sub = y_mission[:N]
ya_sub = y_att[:N]

batch_size = 32
ds = tf.data.Dataset.from_tensor_slices(X_sub).batch(batch_size)

# log
t0 = time.perf_counter()

preds = model.predict(ds, verbose=0)
# preds[0].shape == (800,4), preds[1].shape == (800,1), preds[2].shape == (800,1)

pred_battle     = np.argmax(preds[0], axis=1)
pred_mission    = (preds[1].flatten() > 0.5).astype(int)
pred_attendance = (preds[2].flatten() > 0.5).astype(int)

t1 = time.perf_counter()

correct = (
    (pred_battle     == yb_sub) &
    (pred_mission    == ym_sub) &
    (pred_attendance == ya_sub)
)
result_emoji = ['✔️' if c else '❌' for c in correct]

# ─── 5) 출력용 DataFrame 준비 & tabulate 출력 ─────────────────
out_df = df.iloc[:N][['nickname','date','daily_merit','daily_score']].copy()
out_df['pred_battle'] = pred_battle
out_df['result'] = result_emoji

print(tabulate(out_df, headers='keys', tablefmt='psql', showindex=False))
print("time elapsed: ", t1-t0)
print("rows processed: ", N)
print("accuracy: ", correct.mean())