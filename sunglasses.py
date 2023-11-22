import cv2
import numpy as np

from utils import (
    detect_face,
    load_assets,
    blur_face,
    rotate_sunglasses,
    add_border_to_image,
    rescale_to_facesize
)


class PutOn(object):
    def __init__(self):
        self.face_alignment = detect_face()
        self.sunglasses = load_assets("sunglasses")

        self.sun_h, self.sun_w, _ = self.sunglasses.shape

    def run(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        all_landmarks, _, face_rectangles = self.face_alignment.get_landmarks_from_image(
            img_rgb, return_bboxes=True)

        for bbox, landmarks in zip(face_rectangles, all_landmarks):
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
                img_rgb = blur_face(img_rgb, bbox)

            else:
                sunglasses = self.sunglasses.copy()

                # nose top, left and right face end points
                x = tuple(map(int, landmarks[27]))
                x_18 = tuple(map(int, landmarks[17]))
                x_27 = tuple(map(int, landmarks[26]))

                dx = x_27[0] - x_18[0]
                dy = x_27[1] - x_18[1]

                sunglasses = rescale_to_facesize(sunglasses, dx, dy)
                sunglasses = add_border_to_image(sunglasses)
                sunglasses = rotate_sunglasses(sunglasses, dx, dy)
                height, width, _ = sunglasses.shape

                # Overlay the sunglasses on the original image
                # Get region of interest on the face to change
                try:
                    # Get region of interest on the face to change
                    startY = max(0, x[1]-height//2)
                    endY = min(img_rgb.shape[0]-1, startY + height)
                    startX = max(0, x[0]-width//2)
                    endX = min(img_rgb.shape[1]-1, startX + width)

                    roi_color = img_rgb[startY:endY, startX:endX]

                    # Resize sunglasses to match ROI size
                    sunglasses = cv2.resize(
                        sunglasses, (roi_color.shape[1], roi_color.shape[0]), interpolation=cv2.INTER_AREA)

                    # Removing non-transparent points
                    index = np.argwhere(sunglasses[:, :, 3] > 0)
                    for j in range(3):
                        roi_color[index[:, 0], index[:, 1],
                                  j] = sunglasses[index[:, 0], index[:, 1], j]
                except Exception:
                    img_rgb = blur_face(img_rgb, bbox)

        # self.save_result()
        return cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
