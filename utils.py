import os

import cv2
import face_alignment
import numpy as np


def detect_face():
    detector = face_alignment.FaceAlignment(
        face_alignment.LandmarksType.TWO_D, device='cpu', flip_input=False, verbose=False)
    return detector


def load_assets(filename):
    image_filename = filename + ".png"
    image_path = os.path.join(os.getcwd(), "assets",
                              "sunglasses", image_filename)
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    return image


def draw_landmarks(img, landmarks):
    for i, points in enumerate(landmarks.parts()):
        px = int(points[0])
        py = int(points[1])
        cv2.circle(img, (px, py), 1, (255, 0, 255),
                   thickness=2, lineType=cv2.LINE_AA)
        cv2.putText(img, str(i+1), (px, py),
                    cv2.FONT_HERSHEY_SIMPLEX, .3, (0, 255, 0), 1)


def blur_face(img, bbox):
    # If the circles overlap, blur the face
    face = img[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
    blurred_face = cv2.GaussianBlur(face, (3, 3), 11)
    img[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])] = blurred_face

    return img


def rotate_sunglasses(img, dx, dy):
    # Rotate the sunglasses image
    angle = np.arctan2(dy, dx) * 180 / np.pi
    rows, cols, _ = img.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), -angle, 1)
    img = cv2.warpAffine(
        img, M, (cols, rows),  flags=cv2.INTER_AREA)

    return img


def add_border_to_image(img):
    # Calculate the diagonal length of the resized image
    # NOTE: Could cause issues if the face crop is too large???
    diagonal = int(
        np.sqrt(img.shape[0]**2 + img.shape[1]**2))

    # Calculate the amount of border needed on each side
    border_vertical = (diagonal - img.shape[0]) // 2
    border_horizontal = (diagonal - img.shape[1]) // 2

    # Add the border to the image
    img = cv2.copyMakeBorder(img, border_vertical, border_vertical,
                             border_horizontal, border_horizontal, cv2.BORDER_CONSTANT, value=[0, 0, 0, 0])

    return img


def rescale_to_facesize(img, dx, dy):
    # Calculate the aspect ratio of the sunglasses image
    aspect_ratio = img.shape[1] / img.shape[0]

    # Calculate the width and height of the sunglasses
    width = max(1, int(np.sqrt(dx**2 + dy**2)))
    height = max(1, int(width / aspect_ratio))
    img = cv2.resize(
        img, (width, height), interpolation=cv2.INTER_AREA)

    return img
