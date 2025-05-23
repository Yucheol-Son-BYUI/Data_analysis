import pickle
import tensorflow as tf
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense

# ─── 1) one-hot model  ──────────────────────────
inputs = Input(shape=(9,), name="daily_merit_onehot")
x = Dense(2, activation='relu', name="hidden_1")(inputs)
x = Dense(4, activation='relu', name="hidden_2")(x)

out_battle     = Dense(4, activation='softmax', name="battle_count")(x)
out_mission    = Dense(1, activation='sigmoid', name="daily_mission")(x)
out_attendance = Dense(1, activation='sigmoid', name="attendance")(x)

model = Model(
    inputs=inputs,
    outputs=[out_battle, out_mission, out_attendance]
)

model.compile(
    optimizer='adam',
    loss={
        "battle_count":  "sparse_categorical_crossentropy",
        "daily_mission": "binary_crossentropy",
        "attendance":    "binary_crossentropy",
    },
    metrics={
        "battle_count":  "accuracy",
        "daily_mission": "accuracy",
        "attendance":    "accuracy",
    }
)

with open('model9_onehot_hidden.pkl', 'wb') as f:
    pickle.dump(model, f)

model.summary()
