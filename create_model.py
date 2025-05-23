import pickle
import tensorflow as tf
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense

# ─── 1) define model ───────────────────────────────────────────
inputs = Input(shape=(2,), name="inputs")
x = Dense(8, activation='relu', name="hidden_1")(inputs)
x = Dense(16, activation='relu', name="hidden_2")(x)
x = Dense(8, activation='relu', name="hidden_3")(x)

out_battle     = Dense(4, activation='softmax', name="battle_count")(x)
out_mission    = Dense(1, activation='sigmoid', name="daily_mission")(x)
out_attendance = Dense(1, activation='sigmoid', name="attendance")(x)

model = Model(inputs=inputs,
    outputs=[out_battle, out_mission, out_attendance])

model.compile(
    optimizer='adam',
    loss={
        "battle_count":    "sparse_categorical_crossentropy",  
        "daily_mission":   "binary_crossentropy",
        "attendance":      "binary_crossentropy",
    },
    metrics={
        "battle_count":    "accuracy",                        
        "daily_mission":   "accuracy",
        "attendance":      "accuracy",
    }
)

with open('model5.pkl', 'wb') as f:
    pickle.dump(model, f)
