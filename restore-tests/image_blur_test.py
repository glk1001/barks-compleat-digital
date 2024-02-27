import cv2 as cv
import numpy as np


def median_filter1(gray_img, mask=3):
    """
    :param gray_img: gray image
    :param mask: mask size
    :return: image with median filter
    """
    # set image borders
    bd = int(mask / 2)
    median_img = np.zeros_like(gray_img)
    for i in range(bd, gray_img.shape[0] - bd):
        for j in range(bd, gray_img.shape[1] - bd):
            # get mask according with mask
            kernel = np.ravel(gray_img[i - bd : i + bd + 1, j - bd : j + bd + 1])
            # calculate mask median
            median = np.sort(kernel)[np.int8(np.divide((np.multiply(mask, mask)), 2) + 1)]
            median_img[i, j] = median
    return median_img

def median_filter2(data, filter_size):
    temp = []
    indexer = filter_size // 2
    data_final = []
    data_final = np.zeros((len(data),len(data[0])))
    for i in range(len(data)):

        for j in range(len(data[0])):

            for z in range(filter_size):
                if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                    for c in range(filter_size):
                        temp.append(0)
                else:
                    if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                        temp.append(0)
                    else:
                        for k in range(filter_size):
                            temp.append(data[i + z - indexer][j + k - indexer])

            temp.sort()
            data_final[i][j] = temp[len(temp) // 2]
            temp = []
    return data_final


def median_filter3(original_image, kernel_size: int):
    filtered_image = np.zeros(original_image.shape, dtype=np.int32)
    image_h, image_w = original_image.shape[0], original_image.shape[1]
    w = kernel_size // 2

    wrapped_image = cv.copyMakeBorder(original_image, w, w, w, w, cv.BORDER_CONSTANT, None,
                                  value=(255, 255, 255))

    for i in range(w, image_h - w):  ## traverse image row
        for j in range(w, image_w - w):  ## traverse image col
            neighbours = []
            for x in range(i - w, i + w + 1):
                for y in range(j - w, j + w + 1):
                    pixel = wrapped_image[x, y]
                    if pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0:
                        continue
                    neighbours.append(pixel)
            if len(neighbours) == 0:
                filtered_image[i][j] = (0,0,0)
            else:
                overlap_image = np.array(neighbours)
                filtered_image[i][j] = np.median(overlap_image.reshape(-1, 3), axis=0)  # Filtering

    return filtered_image


# src_image = cv.imread(
#     "/home/greg/Books/Carl Barks/The Comics/Comics and Stories/055 The Terrible Turkey/images/05.jpg"
# )
#src_image = cv.imread("/home/greg/Prj/github/mcomix-barks-tools/simple-test-image.jpg")
src_image = cv.imread("/home/greg/Prj/github/mcomix-barks-tools/test-image.jpg")
#src_image = cv.copyMakeBorder(src_image, 10, 10, 10, 10, cv.BORDER_CONSTANT, None, value = (255,255,255))
height, width, num_channels = src_image.shape
print(f"width: {width}, height: {height}, channels: {num_channels}")

gray_image = cv.cvtColor(src_image, cv.COLOR_BGR2GRAY)
# ret, bin_image = cv.threshold(gray_image,
#                             0, 255,
#                             cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
bin_image = cv.adaptiveThreshold(gray_image, 255,
                               cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV,
                                 21, 10)
cv.imwrite("/tmp/junk-bin-image.jpg", bin_image)

kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
bigger_mask = cv.dilate(bin_image,kernel, iterations=1)
cv.imwrite("/tmp/junk-bigger-mask.jpg", bigger_mask)
src_cut_out = np.full_like(src_image, (255,255,255))
src_cut_out[bigger_mask==0] = src_image[bigger_mask==0]
cv.imwrite("/tmp/junk-src-cut-out.jpg", src_cut_out)

src_inpainted = cv.inpaint(src_cut_out,bigger_mask,5,cv.INPAINT_NS)
cv.imwrite("/tmp/junk-src-inpainted.jpg", src_inpainted)

#src_masked = np.full_like(src_image, (0,0,0))
#src_masked[bin_image==0] = src_image[bin_image==0]

blurred_image = cv.medianBlur(src_inpainted, 5)
#blurred_image = cv.medianBlur(src_masked, 3)
#blurred_image = median_filter1(src_masked, 3)
#blurred_image = median_filter2(src_masked, 3)
#blurred_image = median_filter3(src_masked, 3)

# kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
# smaller_mask = cv.erode(bin_image,kernel, iterations=1)
# cv.imwrite("/tmp/junk-smaller-mask.jpg", smaller_mask)

out_image = src_image.copy()
#out_image = blurred_image
out_image[bin_image==0] = blurred_image[bin_image==0]
out_image[bigger_mask!=0] = src_image[bigger_mask!=0]

cv.imwrite("/tmp/junk-out-image.jpg", out_image)
