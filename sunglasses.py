import os

import cv2
import numpy as np

from utils import (
    detect_face,
    draw_landmarks,
    get_orientation,
    load_assets,
    rotate_along_axis,
)


class PutOn(object):
    def __init__(self):
        self.face_alignment = detect_face()
        self.sunglasses, self.points = load_assets("sunglasses")

        self.sun_h, self.sun_w, _ = self.sunglasses.shape

    def save_landmarks(self, landmarks):
        img_copy = self.img.copy()
        draw_landmarks(img_copy, landmarks)

        landmarks_filename = f"landmarks_{self.filename}"
        landmarks_filepath = os.path.join(
            os.getcwd(), "results", landmarks_filename)
        cv2.imwrite(landmarks_filepath, img_copy)

    def save_result(self):
        result_filename = f"puton_{self.filename}"
        result_filepath = os.path.join(os.getcwd(), "results", result_filename)
        cv2.imwrite(result_filepath, self.img)

    def run(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        all_landmarks, _, face_rectangles = self.face_alignment.get_landmarks_from_image(
            img_rgb, return_bboxes=True)
        # face_rectangles = self.detector_faces(img_rgb, 0)

        # for i in range(len(face_rectangles)):
        for bbox, landmarks in zip(face_rectangles, all_landmarks):
            # NOTE: Pazi na float vrijednosti od bounding boxova od lica jer ćeš ih trebati zamutiti ako je sjebana detekcija landmarksa.

            left_eye = landmarks[36:42]
            right_eye = landmarks[42:48]

            # Compute center and radius of left eye
            left_eye_center = np.mean(left_eye, axis=0, dtype=int)
            left_eye_radius = int(np.linalg.norm(left_eye[0] - left_eye[3]))

            # Compute center and radius of right eye
            right_eye_center = np.mean(right_eye, axis=0, dtype=int)
            right_eye_radius = int(np.linalg.norm(right_eye[0] - right_eye[3]))

            # Calculate the distance between the centers of the two circles
            distance = np.linalg.norm(left_eye_center - right_eye_center)

            # Check if the circles overlap or cover the whole face
            if distance <= left_eye_radius + right_eye_radius:
                # If the circles overlap, blur the face
                face = img[int(bbox[1]):int(bbox[3]),
                           int(bbox[0]):int(bbox[2])]
                blurred_face = cv2.GaussianBlur(face, (3, 3), 11)
                img[int(bbox[1]):int(bbox[3]), int(
                    bbox[0]):int(bbox[2])] = blurred_face

            else:
                # nose top, left and right face end points
                x = int(landmarks[27][0])
                y = int(landmarks[27][1])
                x_18 = int(landmarks[17][0])
                x_27 = int(landmarks[26][0])

                # calculate new width and height, moving distance for adjusting sunglasses
                width = int(abs(x_18 - x_27))
                scale = width / self.sun_w
                height = int(self.sun_h * scale)

                move_x = int(self.points[1] * scale)
                move_y = int(self.points[2] * scale)

                if width == 0 or height == 0:
                    continue

                _h, _w, _ = img.shape
                _, roll, yaw = get_orientation(_w, _h, landmarks)
                sunglasses = rotate_along_axis(
                    self.sunglasses, width, height, phi=yaw, gamma=roll)

                # get region of interest on the face to change
                roi_color = img[(y - move_y):(y + height - move_y),
                                (x - move_x):(x + width - move_x)]

                # find all non-transparent points
                index = np.argwhere(sunglasses[:, :, 3] > 0)

                try:
                    for j in range(3):
                        roi_color[index[:, 0], index[:, 1],
                                  j] = sunglasses[index[:, 0], index[:, 1], j]
                except Exception as e:
                    # If the circles overlap, blur the face
                    face = img[int(bbox[1]):int(bbox[3]),
                               int(bbox[0]):int(bbox[2])]
                    blurred_face = cv2.GaussianBlur(face, (3, 3), 11)
                    img[int(bbox[1]):int(bbox[3]), int(
                        bbox[0]):int(bbox[2])] = blurred_face

                # set the area of the image of the changed region with sunglasses
                img[(y - move_y):(y + height - move_y),
                    (x - move_x):(x + width - move_x)] = roi_color

        # self.save_result()
        return img


def main():

    puton = PutOn()
    puton.images()


if __name__ == "__main__":
    main()
