import os.path
import sys

import cv2
import numpy as np
from skimage.metrics import structural_similarity

image1_file = sys.argv[1]
image2_file = sys.argv[2]

image1 = cv2.imread(image1_file)
image2 = cv2.imread(image2_file)

# Convert images to grayscale.
image1_grey = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
image2_grey = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# Compute SSIM between two images.
(score, diffs) = structural_similarity(image1_grey, image2_grey, full=True)
print("Image similarity", score)

# The diff image contains the actual image differences between the two images and
# is represented as a floating point data type in the range [0,1]. So we must
# convert the array to 8-bit unsigned integers in the range [0,255] before we
# can use it with OpenCV.
diffs = (diffs * 255).astype("uint8")

# Threshold the difference image, followed by finding contours to obtain the
# regions of the two input images that differ.
thresh = cv2.threshold(diffs, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

mask = np.zeros(image1.shape, dtype="uint8")
image2_filled = image2.copy()

for c in contours:
    area = cv2.contourArea(c)
    if area > 40:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image1, (x, y), (x + w, y + h), (36, 255, 12), 2)
        cv2.rectangle(image2, (x, y), (x + w, y + h), (36, 255, 12), 2)
        cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
        cv2.drawContours(image2_filled, [c], 0, (0, 255, 0), -1)

out_dir = "/tmp"

cv2.imwrite(os.path.join(out_dir, "image1-with-diffs.png"), image1)
cv2.imwrite(os.path.join(out_dir, "image2-with-diffs.png"), image2)
cv2.imwrite(os.path.join(out_dir, "diffs.png"), diffs)
cv2.imwrite(os.path.join(out_dir, "mask.png"), mask)
cv2.imwrite(os.path.join(out_dir, "image2-with-filled-diffs.png"), image2_filled)
