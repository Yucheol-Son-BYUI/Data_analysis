import pandas as pd
import numpy as np
import tensorflow as tf
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

model_name = 'model9_onehot_hidden'
# ─── 0) loading model ─────────────────────────────────
with open(model_name + '.pkl', 'rb') as f:
    model = pickle.load(f)

# ─── 1) preprocess ───────────────────────────────
df = pd.read_pickle("preprocessed_data6.pkl")
df['essential_merit'] = df['essential_merit'].round(-1).astype('int32')

categories = [0,50,80,90,110,120,140,150,180]
indices = df['essential_merit'].map({v:i for i,v in enumerate(categories)}).values
X = tf.one_hot(indices, depth=9).numpy().astype('float32')

# X = df['essential_merit'].values.astype('int32')
y_battle  = df['battle_count'].values.astype('int32')
y_mission = df['daily_mission'].values.astype('int32')
y_att     = df['attendance'].values.astype('int32')

# ─── 2) divide dataset into train/test ─────────────────────────────────────
X_train, X_test, \
yb_train, yb_test, \
ym_train, ym_test, \
ya_train, ya_test = train_test_split(
    X, y_battle, y_mission, y_att,
    test_size=0.25, shuffle=True
)

# ─── 3) make batch ─────────────────────────────────
batch_size = 32
train_ds = (
    tf.data.Dataset.from_tensor_slices((
        X_train,
        {"battle_count": yb_train,
         "daily_mission": ym_train,
         "attendance":    ya_train}
    ))
    .shuffle(len(X_train))
    .batch(batch_size)
    .repeat()
)
test_ds = (
    tf.data.Dataset.from_tensor_slices((
        X_test,
        {"battle_count": yb_test,
         "daily_mission": ym_test,
         "attendance":    ya_test}
    ))
    .batch(batch_size)
)

steps_per_epoch = len(X_train)//batch_size
validation_steps = len(X_test)//batch_size


# ─── 4) train ───────────────────────────────────────────
model.fit(
    train_ds,
    epochs=30,
    steps_per_epoch=steps_per_epoch,
    validation_data=test_ds,
    validation_steps=validation_steps
)

# ─── 7) (evaluate) ─────────────────────────────────
print("\n=== Model.evaluate on test set ===")
eval_results = model.evaluate(test_ds, steps=validation_steps)
for name, val in zip(model.metrics_names, eval_results):
    print(f"{name}: {val:.4f}")

# ─── 8) 수동 평가 (predict + classification_report) ────────────
# 8-1) 예측
preds = model.predict(X_test, batch_size=batch_size)
# battle_count: 실수 → 반올림 → 정수
pred_battle = np.argmax(preds[0], axis=1) 
# 나머지는 0.5 기준 이진 분류
pred_mission   = (preds[1].flatten()>0.5).astype(int)
pred_attendance= (preds[2].flatten()>0.5).astype(int)

# 8-2) 리포트 출력
print("\n=== Battle Count Classification Report ===")
print(classification_report(yb_test, pred_battle, labels=[0,1,2,3]))

print("=== Daily Mission Report ===")
print(classification_report(ym_test, pred_mission, labels=[0,1]))

print("=== Attendance Report ===")
print(classification_report(ya_test, pred_attendance, labels=[0,1]))

# ─── 9) 모델 저장 (.pkl) ────────────────────────────────────
save = input("Save model? (y/n): ").strip().lower()
if save == 'y':
    with open(model_name + '_trained.pkl', 'wb') as f:
        pickle.dump(model, f)