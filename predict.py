import pandas as pd
import tensorflow as tf
import numpy as np

CATEGORIES = [0,50,80,90,110,120,140,150,180]
model = pd.read_pickle('model9_onehot_hidden_trained.pkl')

while True:
  daily_score = input("Enter a daily score (or 'exit' to quit): ")
  daily_score = daily_score.lower()
  if daily_score == 'exit':
    break
  daily_score = int(daily_score)
  daily_merit = input("Enter a daily merit (or 'exit' to quit): ")
  daily_merit = daily_merit.lower()
  if daily_merit == 'exit':
    break
  daily_merit = int(daily_merit)
  merit = round(daily_merit - int(daily_score * 0.1),-1)
  idx = CATEGORIES.index(merit)
  X = tf.one_hot(idx, depth=9).numpy().astype('float32')
  x_input = tf.expand_dims(X, axis=0)  # model expects a batch dimension

  pred_battle_probs, pred_mission_prob, pred_attendance_prob = model.predict(x_input, verbose=0)
  
  battle_count  = int(np.argmax(pred_battle_probs[0]))
  daily_mission = int(pred_mission_prob[0][0] > 0.5)
  attendance    = int(pred_attendance_prob[0][0] > 0.5)
  
  print("\n=== Prediction ===")
  print(f"Input Daily Score: {daily_score}")
  print(f"Input Daily Merit: {daily_merit}")
  print(f"Input Merit Category: {merit} (index {idx})")
  print(f"Predicted Battle Count : {battle_count}")
  print(f"Daily Mission: {daily_mission}")
  print(f"Attendance: {attendance}\n")