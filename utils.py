import cv2
import mediapipe as mp
from cv2 import cvtColor
import numpy as np

upper_lip = [61, 185, 40, 39, 37, 0, 267, 269, 270, 408,
             415, 272, 271, 268, 12, 38, 41, 42, 191, 78, 76]
lower_lip = [61, 146, 91, 181, 84, 17, 314, 405, 320,
             307, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]


def detect_landmarks(src):
    global rgb
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh()
    rgb = cvtColor(src, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    if results.multi_face_landmarks:
        return results.multi_face_landmarks[0].landmark
    return None


def landmarks(landmarks, height, width, mask):
    lip_landmarks = np.array(
        [(int(landmark.x * width), int(landmark.y * height)) for landmark in landmarks])
    if mask:
        lip_landmarks = lip_landmarks[mask]
    return lip_landmarks


def lip_mask(src, points, color):
    mask = np.zeros_like(src)
    mask = cv2.fillPoly(mask, [points], color)
    mask = cv2.GaussianBlur(mask, (7, 7), 5)
    return mask


def apply_lipstick(src, color="NO", transparency=0.1):
    global mask
    ret_landmarks = detect_landmarks(src)
    height, width, _ = src.shape
    feature_landmarks = None
    feature_landmarks = landmarks(
        ret_landmarks, height, width, upper_lip+lower_lip)

    if color == 'NO':
        mask = lip_mask(src, feature_landmarks, [0, 0, 0])
    elif color == 'orange':
        mask = lip_mask(src, feature_landmarks, [50, 50, 200])
    elif color == 'purple':
        mask = lip_mask(src, feature_landmarks, [255, 0, 0])
    elif color == 'red':
        mask = lip_mask(src, feature_landmarks, [30, 10, 250])
    elif color == 'pink':
        mask = lip_mask(src, feature_landmarks, [153, 0, 157])

    src1 = cvtColor(src, cv2.COLOR_BGR2RGB)
    mask1 = cvtColor(mask, cv2.COLOR_BGR2RGB)
    output = cv2.addWeighted(src1, 1, mask1, transparency, 0.0)
    return output
