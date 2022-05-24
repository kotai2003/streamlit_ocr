import easyocr
import cv2
import numpy as np
import math


class my_ocr():
    def __init__(self, lang_list=['en', 'ja']):
        self.lang_list = lang_list
        self.reader = easyocr.Reader(self.lang_list)
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def ocr_read(self, img):
        self.result = self.reader.readtext(img)
        return self.result

    def _detect_rot_angle(self, img,p0,p1,p2,p3 ):
        points = np.array([p0, p1, p2, p3], dtype=np.int32)

        # マスク画像生成
        img_h, img_w, _ = img.shape
        img_black = np.zeros((img_h, img_w))
        img_mask = cv2.fillPoly(img_black, [points], (255, 255, 255), cv2.LINE_AA)

        # moment 計算
        m = cv2.moments(img_mask)
        area = m['m00']
        x_g = m['m10'] / m['m00']
        y_g = m['m01'] / m['m00']
        ang = 0.5 * math.atan2(2.0 * m['mu11'], m['mu20'] - m['mu02'])

        #center points and rotation angle
        center = (int(x_g), int(y_g))
        rot_ang = 1 * math.degrees(ang)

        return center, rot_ang

    def draw_boxes(self, img, result):
        img_copy = img.copy()

        center_list = []
        text_list = []

        for detection in result:

            p0 = tuple((detection[0][0]))
            p1 = tuple((detection[0][1]))
            p2 = tuple((detection[0][2]))
            p3 = tuple((detection[0][3]))
            points = np.array([p0, p1, p2, p3], dtype=np.int32)
            text = detection[1]
            text_list.append(text)

            #detect center, rotation_angle
            center, rot_ang = self._detect_rot_angle(img_copy, p0, p1, p2, p3)
            center_list.append(center)
            conficence = round(detection[2],2)

            #Draw
            img = cv2.drawMarker(img, position=center, color=(0,0,255), markerType=cv2.MARKER_CROSS, markerSize=20,
                                 thickness=2)
            img = cv2.polylines(img, [points], True, (255, 0, 0), thickness=2)
            img = cv2.putText(img, text, (int(p0[0]), int(p0[1])), self.font, 1, (255, 255, 0), 2, cv2.LINE_AA)

        if center_list is None:

            return img

        else:

            return img, center_list, text_list



