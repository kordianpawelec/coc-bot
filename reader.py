import easyocr
import cv2

img = cv2.imread('view.png')
reader = easyocr.Reader(['en'], gpu=False)

print(reader.readtext(img))