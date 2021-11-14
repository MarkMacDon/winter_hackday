import csv
import glob
import os.path

import cv2
import numpy as np

def prepare_im(path):
    # loads the image from a path and converts it to greyscale
    img = cv2.imread(path)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grey = grey.astype(np.float64)
    return grey

if __name__ == "__main__":
    # so long as the brightness is this many units greater than the background, we detected a light
    threshold = 50

    # load the background image
    background = prepare_im("../data/background.jpg")

    pixels = []
    # for each of the images we have in data
    for img_path in glob.glob(f"../data/*.jpg"):
        light_im = prepare_im(img_path)

        # remove the background so that we are looking at the change in lighting conditions
        diff = np.clip(light_im - background, 0, None)

        # threshold out any change below our defined threshold
        threshed = np.zeros_like(diff, dtype=np.uint8)
        threshed[diff > threshold] = diff[diff > threshold]

        # get the location of the maximum brightness in the image
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(threshed)

        # if we detected a change then
        if maxVal > 0:
            filename = os.path.basename((img_path))
            pixel_id = int(filename.replace(".jpg", ""))

            pixels.append([pixel_id, maxLoc[0], maxLoc[1]])

        # show the images and the detections
        image = light_im.copy().astype(np.uint8)
        image = np.dstack([image, image, image])
        cv2.circle(image, maxLoc, 10, (255, 0, 0), 2)
        cv2.imshow("im", image)
        cv2.waitKey(1)

    with open("../data/coords2.csv", "w", newline="\n") as f:
        writer = csv.writer(f)
        for row in pixels:
            writer.writerow(row)