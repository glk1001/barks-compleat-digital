import cv2 as cv
import numpy as np

from remove_alias_artifacts import get_median_filter


def get_removed_color(grey_img: cv.typing.MatLike, input_image: cv.typing.MatLike) -> cv.typing.MatLike:
    filtered_image = np.zeros(input_image.shape, dtype=np.int32)
    image_h, image_w = input_image.shape[0], input_image.shape[1]

    threshold = 60

    for i in range(0, image_h):  ## traverse image row
        for j in range(0, image_w):  ## traverse image col
            pixel = input_image[i][j]
            red = int(pixel[2])
            green = int(pixel[1])
            blue = int(pixel[0])
            grey = int(grey_img[i][j])
            if abs(red - 183) < 5 and abs(green - 218) < 5 and abs(blue - 222) < 5:
                filtered_image[i][j] = (255, 255, 255)
            elif abs(red - 248) < 5 and abs(green - 242) < 5 and abs(blue - 226) < 5:
                    filtered_image[i][j] = (255, 255, 255)
            elif abs(red - grey) < threshold and abs(green - grey) < threshold and abs(blue - grey) < threshold:
                filtered_image[i][j] = pixel
                print(f"({i},{j}): {red},{green},{blue},{grey}")
            else:
                filtered_image[i][j] = (255,255,255)

    return filtered_image

test_image = "/home/greg/Prj/github/mcomix-barks-tools/restore-tests/test-image-2.jpg"

src_image = cv.imread(test_image)
#src_image = cv.copyMakeBorder(src_image, 10, 10, 10, 10, cv.BORDER_CONSTANT, None, value = (255,255,255))
height, width, num_channels = src_image.shape
print(f"width: {width}, height: {height}, channels: {num_channels}")

blurred_image = get_median_filter(src_image)
gray_image = cv.cvtColor(blurred_image, cv.COLOR_BGR2GRAY)

out_image = get_removed_color(gray_image, blurred_image)

cv.imwrite("/tmp/junk-out-image.jpg", out_image)
