import random
import sys

import cv2 as cv
import numpy as np


def to_percent(channel_val):
    return int(100.0 * float(channel_val) / 255.0)


def get_color_removed_image(image):
    hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    # lower1 = np.array([0, 0, 70])
    # upper1 = np.array([180, 255, 255])
    # lower_mask = cv.inRange(src_image, lower1, upper1)

    alias_mask = get_alias_mask1(hsv_image)
    alias_mask = get_alias_mask2(hsv_image, alias_mask)
    alias_mask = get_alias_mask2(hsv_image, alias_mask)
    alias_mask = get_alias_mask2(hsv_image, alias_mask)
    alias_mask = get_alias_mask2(hsv_image, alias_mask)

    # for x in range(x0, x1 + 1):
    #     for y in range(y0, y1 + 1):
    #         rgb = [result[y, x][2], result[y, x][1], result[y, x][0]]
    #         rgb_percent = [to_percent(rgb[0]), to_percent(rgb[1]), to_percent(rgb[2])]
    #         print(
    #                 f"x:{x}, y: {y}, src_image, percent, hsv, lower_mask, alias_mask:"
    #                 f" {rgb}, {rgb_percent}, {hsv_image[y, x]}, {lower_mask[y, x]}, {alias_mask[y, x]}"
    #         )
    #         lower_mask[y, x] = 128

    return alias_mask


def get_alias_mask1(hsv_img):
    h, w, num_ch = hsv_img.shape

    mask = np.full((h, w), 0, dtype=np.uint8)

    for y in range(0, height):
        for x in range(0, width):
            if hsv_img[y, x][2] > 110:
                # Not dark enough
                continue
            mask[y, x] = 255 if has_black_neighbour(hsv_img, w, h, x, y) else 0

    return mask


def get_alias_mask2(hsv_img, cur_mask):
    h, w, num_ch = hsv_img.shape

    mask = np.full((h, w), 0, dtype=np.uint8)

    for y in range(0, height):
        for x in range(0, width):
            if hsv_img[y, x][2] > 150:
                # Not dark enough
                continue
            mask[y, x] = 255 if has_alias_neighbour(cur_mask, w, h, x, y) else 0

    return mask


def has_black_neighbour(hsv_img, w, h, x, y):
    if x == 0 or x == w - 1:
        return 1
    if y == 0 or y == h - 1:
        return 1

    assert 0 < x < w - 1
    assert 0 < y < h - 1

    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if i == j:
                continue
            if hsv_img[j, i][2] < 50:
                return True

    return False


def has_alias_neighbour(alias_mask, w, h, x, y):
    if x == 0 or x == w - 1:
        return 1
    if y == 0 or y == h - 1:
        return 1

    assert 0 < x < w - 1
    assert 0 < y < h - 1

    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if i == j:
                continue
            if alias_mask[j, i] == 255:
                return True

    return False


NEXT_SIBLING = 0
PREV_SIBLING = 1
CHILD_CONTOUR = 2
PARENT_CONTOUR = 3


def draw_hierarchy(image, contours, hierarchy):
    rows = hierarchy.shape[0]
    for i in range(rows):
        if hierarchy[i][3] == -1:
            print(f"No parent: {i} - {contours[i][:5]}")
            cv.drawContours(image, contours, i, (0, 255, 0), 1)
        else:
            print(f"Parent:    {i} - {contours[i][:5]}")
            cv.drawContours(image, contours, i, (255, 0, 0), 1)
    return

    num_contours = len(contours)

    num_processed = 0
    i = 0
    while True:
        assert hierarchy[i][PARENT_CONTOUR] == -1

        if hierarchy[i][CHILD_CONTOUR] == -1:
            # This contour has no children, draw it red for demonstration purposes
            print(f"Red: {i} - {contours[i][0]}")
            cv.drawContours(image, contours, i, (0, 0, 255), 1)
            num_processed += 1
            i = hierarchy[i][NEXT_SIBLING]
            if i == -1:
                break
            continue

        # This contour has children, draw it blue for demonstration purposes
        print(f"Blue: {i} - {contours[i][0]}")
        cv.drawContours(image, contours, i, (255, 0, 0), 1)
        num_processed += 1

        # Iterate over all direct children
        j = hierarchy[i][CHILD_CONTOUR]
        assert j != -1
        while True:
            cv.drawContours(image, contours, j, (0, 55, 0), 2)
            print(f"Green: {j} - {contours[j][0]}")
            num_processed += 1
            assert hierarchy[j][PARENT_CONTOUR] != -1
            j = hierarchy[j][NEXT_SIBLING]
            if j == -1:
                break

        i = hierarchy[i][NEXT_SIBLING]
        if i == -1:
            break

    print(f"num_processed = {num_processed}")


def draw_contours(image, contours):
    cv.drawContours(image, contours, -1, (0,255,0), 1)

    # for i in range(len(contours)):
    #     # Draw the contour
    #     color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    #     cv.drawContours(image, contours, i, color, 1)


def get_edges(image):
    canny_lower = 50
    canny_upper = 300
    canny_aperture_size = 7
    l2_gradient = False
    return cv.Canny(
            image,
            canny_lower,
            canny_upper,
            apertureSize=canny_aperture_size,
            L2gradient=l2_gradient,
    )


# src_image = cv.imread(
#     "/home/greg/Books/Carl Barks/The Comics/Comics and Stories/055 The Terrible Turkey/images/05.jpg"
# )
src_image = cv.imread("/home/greg/Prj/github/mcomix-barks-tools/simple-test-image.jpg")
#src_image = cv.imread("/home/greg/Prj/github/mcomix-barks-tools/test-image.jpg")
src_image = cv.copyMakeBorder(src_image, 10, 10, 10, 10, cv.BORDER_CONSTANT, None, value = (255,255,255))
height, width, num_channels = src_image.shape
print(f"width: {width}, height: {height}, channels: {num_channels}")

gray_image = cv.cvtColor(src_image, cv.COLOR_BGR2GRAY)
ret, bin_image = cv.threshold(gray_image,
                            0, 255,
                            cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
cv.imwrite("/tmp/junk-bin-image.jpg", bin_image)

# noise removal
# kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
# bin_image = cv.morphologyEx(bin_image,cv.MORPH_OPEN,kernel, iterations=1)
# cv.imwrite("/tmp/junk-bin-image-de-noise.jpg", bin_image)

edges = get_edges(bin_image)

edge_contours, edge_hierarchy = cv.findContours(edges, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

edge_contours = list(edge_contours)
edge_hierarchy = edge_hierarchy[0]
print(type(edge_contours))
print(f"len(edge_contours) = {len(edge_contours)}.")
print(f"edge_contours[0].shape = {edge_contours[0].shape}.")
print(f"edge_hierarchy.shape = {edge_hierarchy.shape}.")

contours_image = np.zeros((height,width,3), np.uint8)
draw_contours(contours_image, edge_contours)

hierarchy_image = np.zeros((height,width,3), np.uint8)
draw_hierarchy(hierarchy_image, edge_contours, edge_hierarchy)

contours_list = []
for i in range(0, len(edge_contours)):
    c = edge_contours[i]
    print(len(c))
    # if len(c) < 10:
    #     print(c)
    #print(c[0][0], c[-1][0])
    # print(type(c), c.shape)
    if c[0][0][0] != c[-1][0][0] or c[0][0][1] != c[-1][0][1]:
        c_list = c.tolist()
        c_list.append(c[0].tolist())
        # print(type(c_list[0]), type(c_list[-1]))
        #print(c_list)
        c = np.array(c_list).reshape((-1, 1, 2))
    contours_list.append(c)
contours_list_image = np.zeros((height,width,3), np.uint8)
draw_contours(contours_list_image, contours_list)

print(len(contours_list))
contours_merged = np.zeros((height,width,3), np.uint8)
for c in contours_list:
    color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    cv.fillPoly(contours_merged, [c], color)
# cv.fillPoly(contours_merged, contours_list, (0.255,0), cv.LINE_8)

contours_circles = contours_image.copy()
for i, contour in enumerate(edge_contours): # loop over one contour area
    color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    for j, contour_point in enumerate(contour): # loop over the points
       # draw a circle on the current contour coordinate
       cv.circle(contours_circles, ((contour_point[0][0], contour_point[0][1])), 2, color, 1, cv.LINE_AA)

cv.imwrite("/tmp/junk-edges.jpg", edges)
cv.imwrite("/tmp/junk-hierarchy.jpg", hierarchy_image)
cv.imwrite("/tmp/junk-contours.jpg", contours_image)
cv.imwrite("/tmp/junk-contours-circles.jpg", contours_circles)
cv.imwrite("/tmp/junk-contours-list.jpg", contours_list_image)
cv.imwrite("/tmp/junk-contours-merged.jpg", contours_merged)
#sys.exit(0)

#alias_mask = get_color_removed_image(src_image)
#cv.imwrite("/tmp/junk-alias.jpg", alias_mask)

# result = cv.bitwise_or(result, result, mask=full_mask)
# cv.imwrite("/tmp/junk.jpg", lower_mask)
# cv.imwrite("/tmp/junk.jpg", result)

cv.imwrite("/tmp/junk-src-image.jpg", src_image)

out_image = np.bitwise_or(src_image, edges[:,:,np.newaxis])
cv.imwrite("/tmp/junk-out-image.jpg", out_image)
