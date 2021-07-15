# -*- coding: utf-8 -*-
"""Pose_estimation_and_scoring.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J-ZvJ247lAEB-oKljwyTI84A0UqbuHc2
"""

!pip install mediapipe
!pip install dtaidistance

import cv2
import numpy as np
import mediapipe as mp
from google.colab.patches import cv2_imshow

#teacher_video_preprocess_loc = '/content/drive/MyDrive/weskill/Lambergini Video.mp4'
#teacher_video_processed_loc = '/content/drive/MyDrive/weskill/Lambergini_Video_processed.mp4'
teacher_video_preprocess_loc = '/content/drive/MyDrive/weskill/videoplayback2.mp4'
teacher_video_processed_loc = '/content/drive/MyDrive/weskill/videoplayback2_processed.mp4'
student_video_loc = '/content/drive/MyDrive/weskill/videoplayback1.mp4' # 0 for webcam

all_Landmarks = ['NOSE','LEFT_EYE_INNER','LEFT_EYE','LEFT_EYE_OUTER','RIGHT_EYE_INNER','RIGHT_EYE','RIGHT_EYE_OUTER','LEFT_EAR','RIGHT_EAR','MOUTH_LEFT','MOUTH_RIGHT','LEFT_SHOULDER','RIGHT_SHOULDER','LEFT_ELBOW','RIGHT_ELBOW','LEFT_WRIST','RIGHT_WRIST','LEFT_PINKY','RIGHT_PINKY','LEFT_INDEX','RIGHT_INDEX','LEFT_THUMB','RIGHT_THUMB','LEFT_HIP','RIGHT_HIP','LEFT_KNEE','RIGHT_KNEE','LEFT_ANKLE','RIGHT_ANKLE','LEFT_HEEL','RIGHT_HEEL','LEFT_FOOT_INDEX','RIGHT_FOOT_INDEX']
Landmarks = all_Landmarks.copy()
Landmarks = ['NOSE','LEFT_SHOULDER','RIGHT_SHOULDER','LEFT_ELBOW','RIGHT_ELBOW','LEFT_WRIST','RIGHT_WRIST','LEFT_HIP','RIGHT_HIP','LEFT_KNEE','RIGHT_KNEE','LEFT_ANKLE','RIGHT_ANKLE']

# teacher video processing. Running once is enough. not necessarily realtime
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_holistic =  mp.solutions.holistic
fps_input = 30
fps_output = 20

cap = cv2.VideoCapture(teacher_video_preprocess_loc)
count = 0
frame_width = int(cap.get(3)) # interchange 3 & 4 if inputs are normal
frame_height = int(cap.get(4))
size = (frame_width, frame_height)

result = cv2.VideoWriter(teacher_video_processed_loc, cv2.VideoWriter_fourcc(*'MJPG'),fps_output, size)

teacher_X_data = []
teacher_Y_data = []
teacher_Z_data = []
teacher_visibility_data = []

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5, model_complexity=1) as pose:
  while cap.isOpened():
    success, image = cap.read()
    #image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    count += 1
    if count<100:
      continue
    if count%3 == 2: # need to change is fps_output is not 20
      continue
    if not success:
      print("Done")
      break
    
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    result.write(image)
    try:
      teacher_X_data.append([eval('results.pose_landmarks.landmark[mp_holistic.PoseLandmark.'+Landmark+'].x') for Landmark in Landmarks])
      teacher_Y_data.append([eval('results.pose_landmarks.landmark[mp_holistic.PoseLandmark.'+Landmark+'].y') for Landmark in Landmarks])
      teacher_Z_data.append([eval('results.pose_landmarks.landmark[mp_holistic.PoseLandmark.'+Landmark+'].z') for Landmark in Landmarks])
      teacher_visibility_data.append([eval('results.pose_landmarks.landmark[mp_holistic.PoseLandmark.'+Landmark+'].visibility') for Landmark in Landmarks])
    except:
      continue
teacher_X_data = np.array(teacher_X_data)
teacher_Y_data = np.array(teacher_Y_data)
teacher_Z_data = np.array(teacher_Z_data)
teacher_visibility_data = np.array(teacher_visibility_data)

cap.release()
result.release()

# student video processing. realtime
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_holistic =  mp.solutions.holistic
fps_input = 30
fps_output = 20

cap = cv2.VideoCapture(student_video_loc)
count = 0
frame_width = int(cap.get(3)) # interchange 3 & 4 if inputs are normal
frame_height = int(cap.get(4))
size = (frame_width, frame_height)

#result = cv2.VideoWriter(student_video_processed_loc, cv2.VideoWriter_fourcc(*'MJPG'),fps_output, size)

student_X_data = []
student_Y_data = []
student_Z_data = []
student_visibility_data = []

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5, model_complexity=1) as pose:
  while cap.isOpened():
    success, image = cap.read()
    #image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    count += 1
    if count%3 == 2: # need to change is fps_output is not 20
      continue
    if not success:
      print("Done")
      # If loading a video, use 'break' instead of 'continue'.
      break
    
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    #result.write(image)
    try:
      student_X_data.append([eval('results.pose_landmarks.landmark[mp_holistic.PoseLandmark.'+Landmark+'].x') for Landmark in Landmarks])
      student_Y_data.append([eval('results.pose_landmarks.landmark[mp_holistic.PoseLandmark.'+Landmark+'].y') for Landmark in Landmarks])
      student_Z_data.append([eval('results.pose_landmarks.landmark[mp_holistic.PoseLandmark.'+Landmark+'].z') for Landmark in Landmarks])
      student_visibility_data.append([eval('results.pose_landmarks.landmark[mp_holistic.PoseLandmark.'+Landmark+'].visibility') for Landmark in Landmarks])
    except:
      continue
student_X_data = np.array(student_X_data)
student_Y_data = np.array(student_Y_data)
student_Z_data = np.array(student_Z_data)
student_visibility_data = np.array(student_visibility_data)

cap.release()
result.release()

from dtaidistance import dtw
total_distance = 0
for i in range(33):
  d1 = dtw.distance(student_X_data[:,i],teacher_X_data[:,i])
  d2 = dtw.distance(student_Y_data[:,i],teacher_Y_data[:,i])
  #d3 = dtw.distance(student_Z_data[:,i],teacher_Z_data[:,i])
  total_distance += (d1+d2)/(2*33)
  print(Landmarks[i],total_distance)

def euclidian_distance(a,b,k):
  return np.linalg.norm(a[0:k]-b[0:k])

student_X_data2 = student_X_data.copy()
student_Y_data2 = student_Y_data.copy()
student_Z_data2 = student_Z_data.copy()
teacher_X_data2 = student_X_data.copy()
teacher_Y_data2 = student_Y_data.copy()
teacher_Z_data2 = student_Z_data.copy()

k = min(len(student_X_data[:,0]),len(teacher_X_data[:,0]))
for i in range(k):
  student_X_data2[i] = np.multiply(np.multiply(student_visibility_data[i],teacher_visibility_data[i]),student_X_data[i]-0.5*(student_X_data[0,7]+student_X_data[0,8]))
  student_Y_data2[i] = np.multiply(np.multiply(student_visibility_data[i],teacher_visibility_data[i]),student_Y_data[i]-0.5*(student_Y_data[0,7]+student_Y_data[0,8]))
  student_Z_data2[i] = np.multiply(np.multiply(student_visibility_data[i],teacher_visibility_data[i]),student_Z_data[i])
  teacher_X_data2[i] = np.multiply(np.multiply(student_visibility_data[i],teacher_visibility_data[i]),teacher_X_data[i]-0.5*(teacher_X_data[0,7]+teacher_X_data[0,8]))
  teacher_Y_data2[i] = np.multiply(np.multiply(student_visibility_data[i],teacher_visibility_data[i]),teacher_Y_data[i]-0.5*(teacher_Y_data[0,7]+teacher_Y_data[0,8]))
  teacher_Z_data2[i] = np.multiply(np.multiply(student_visibility_data[i],teacher_visibility_data[i]),teacher_Z_data[i])

total_distance = 0
for i in range(len(Landmarks)):
  d1 = euclidian_distance(student_X_data2[:,i],teacher_X_data2[:,i],k)
  d2 = euclidian_distance(student_Y_data2[:,i],teacher_Y_data2[:,i],k)
  d3 = euclidian_distance(student_Z_data2[:,i],teacher_Z_data2[:,i],k)
  total_distance += (d1+d2+d3)

total_distance

score = 100 - total_distance*10000/(3*len(Landmarks)*k)
print('score = ',score)

def cosine_similarity(a,b):
  return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

student_X_data2 = student_X_data.copy()
student_Y_data2 = student_Y_data.copy()
student_Z_data2 = student_Z_data.copy()
teacher_X_data2 = student_X_data.copy()
teacher_Y_data2 = student_Y_data.copy()
teacher_Z_data2 = student_Z_data.copy()

k = min(len(student_X_data[:,0]),len(teacher_X_data[:,0]))
for i in range(k):
  #student_X_data2[i] = student_X_data[i]-0.5*(student_X_data[0,7]+student_X_data[0,8])
  #student_Y_data2[i] = student_Y_data[i]-0.5*(student_Y_data[0,7]+student_Y_data[0,1])
  student_Z_data2[i] = student_Z_data[i]
  student_X_data2[i] = student_X_data[i]
  student_Y_data2[i] = student_Y_data[i]
  #teacher_X_data2[i] = teacher_X_data[i]-0.5*(teacher_X_data[0,7]+teacher_X_data[0,8])
  #teacher_Y_data2[i] = teacher_Y_data[i]-0.5*(teacher_Y_data[0,7]+teacher_Y_data[0,1])
  teacher_Z_data2[i] = teacher_Z_data[i]

total_similarity = 0
for i in range(len(Landmarks)):
  for j in range(k):
    #total_similarity += cosine_similarity(np.array([student_X_data2[j,i],student_Y_data2[j,i],student_Z_data2[j,i]]),np.array([teacher_X_data2[j,i],teacher_Y_data2[j,i],teacher_Z_data2[j,i]]))
    total_similarity += cosine_similarity(np.array([student_X_data2[j,i],student_Y_data2[j,i]]),np.array([teacher_X_data2[j,i],teacher_Y_data2[j,i]]))
  #print(Landmarks[i],total_distance)

total_similarity

score = total_similarity*100/(len(Landmarks)*k)
print(score)

score = 100 - total_distance*100*10000/(2*33*k)
print('score = ',score)

len(student_X_data[:,13])

print(distance)