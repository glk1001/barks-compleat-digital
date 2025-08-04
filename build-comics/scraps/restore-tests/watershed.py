#!/usr/bin/env python

"""
Watershed segmentation
=========

This program demonstrates the watershed segmentation algorithm
in OpenCV: watershed().

Usage
-----
watershed.py [image filename]

Keys
----
  1-7   - switch marker color
  SPACE - update segmentation
  r     - reset
  a     - toggle autoupdate
  ESC   - exit

"""

import numpy as np
import cv2 as cv


class App:
    def __init__(self, fn):
        self.img = cv.imread(fn)
        if self.img is None:
            raise Exception("Failed to load image file: %s" % fn)

        h, w = self.img.shape[:2]
        self.markers = np.zeros((h, w), np.int32)
        self.markers_vis = self.img.copy()
        self.cur_marker = 1
        self.colors = np.int32(list(np.ndindex(2, 2, 2))) * 255

        self.auto_update = True

    def get_colors(self):
        return list(map(int, self.colors[self.cur_marker])), self.cur_marker

    def watershed(self):
        m = self.markers.copy()
        cv.watershed(self.img, m)
        overlay = self.colors[np.maximum(m, 0)]
        vis = cv.addWeighted(self.img, 0.5, overlay, 0.5, 0.0, dtype=cv.CV_8UC3)
        return vis


if __name__ == "__main__":
    #    image_file = "/home/greg/Prj/github/barks-compleat-digital/restore-tests/simple-test-image.jpg"
    image_file = "/home/greg/Prj/github/restore-barks/experiments/test-image-2.jpg"
    src_image = cv.imread(image_file)
    gray = cv.cvtColor(src_image, cv.COLOR_BGR2GRAY)
    ret, bin_img = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    bin_img = cv.morphologyEx(bin_img, cv.MORPH_OPEN, kernel, iterations=2)
    #    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    #    bin_img = cv.morphologyEx(bin_img,
    #                               cv.MORPH_CROSS,
    #                               kernel,
    #                               iterations=2)
    cv.imwrite("/tmp/junk-bin-image.jpg", bin_img)

    # sure background area
    sure_bg = cv.dilate(bin_img, kernel, iterations=3)
    cv.imwrite("/tmp/junk-sure_bg.jpg", sure_bg)

    # foreground area
    dist = cv.distanceTransform(bin_img, cv.DIST_L2, 5)
    ret, sure_fg = cv.threshold(dist, 0.2 * dist.max(), 255, cv.THRESH_BINARY)
    sure_fg = sure_fg.astype(np.uint8)
    cv.imwrite("/tmp/junk-sure_fg.jpg", sure_fg)

    # unknown area
    unknown = cv.subtract(sure_bg, sure_fg)
    cv.imwrite("/tmp/junk-unknown.jpg", unknown)

    # Marker labelling
    # sure foreground
    ret, markers = cv.connectedComponents(sure_fg)

    # Add one to all labels so that background is not 0, but 1
    markers += 1
    # mark the region of unknown with zero
    markers[unknown == 255] = 0
    cv.imwrite("/tmp/junk-markers.jpg", markers)

    # watershed Algorithm
    markers = cv.watershed(src_image, markers)
    src_image[markers == -1] = [0, 0, 255]
    cv.imwrite("/tmp/junk-watershed-img.jpg", src_image)

    # app = App("/home/greg/Prj/github/barks-compleat-digital/simple-test-image.jpg")
    # vis = app.watershed()
    # cv.imwrite("/tmp/junk-watershed.jpg", vis)

    for label in np.unique(markers):
        # if the label is zero, we are examining the 'background'
        # so simply ignore it
        if label == 1:
            continue
        # otherwise, allocate memory for the label region and draw
        # it on the mask
        mask = np.zeros(gray.shape, dtype="uint8")
        mask[markers == label] = 255
        file = f"/tmp/junk-label-{label}.jpg"
        cv.imwrite(file, mask)
