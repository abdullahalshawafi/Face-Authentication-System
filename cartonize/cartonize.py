import cv2


def cartoonize(image):
    if (len(image.shape) == 3) and (image.shape[2] == 4):
        image = image[:, :, 0:3]
    if len(image.shape) != 2:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
    else:
        gray = image

    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2
    )

    color = cv2.bilateralFilter(image, 9, 200, 200)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    cartoon = cv2.medianBlur(cartoon, 9)
    return cartoon
