import csv

import cv2
import numpy as np

def prepare_im(path):
    img = cv2.imread(path)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grey = grey.astype(np.float64)
    return grey

if __name__ == "__main__":
    background = prepare_im("./data/background.jpg")
    threshold = 50

    pixels = []
    for i in range(150):
        path = img_path = f"./data/{i:03}.jpg"
        light_im = prepare_im(img_path)

        diff = np.clip(light_im - background, 0, None)
        threshed = np.zeros_like(diff, dtype=np.uint8)
        threshed[diff > threshold] = diff[diff > threshold]

        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(threshed)

        if maxVal > 0:
            pixels.append([i, maxLoc[0], maxLoc[1]])

        image = diff.copy().astype(np.uint8)
        cv2.circle(image, maxLoc, 10, (255, 0, 0), 2)
        cv2.imshow("im", image)

        cv2.waitKey(-1)



    # with open("./data/coords.csv", "w", newline="\n") as f:
    #     writer = csv.writer(f)
    #     for row in pixels:
    #         writer.writerow(row)