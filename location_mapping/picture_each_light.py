import os.path
import shutil
import time
from pathlib import Path

import board
import neopixel
import requests

pixel_pin = board.D18
ORDER = neopixel.RGB

num_pixels = 500
# we use an app, ipwebcam, on a phone to get the image of each light
camera_url = "http://192.168.1.86:8080/photo.jpg"


pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER
)

def take_image(filename):
    print(f"download: {filename}")
    r = requests.get(camera_url, stream=True)
    if r.status_code == 200:
        Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        with open(filename, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        raise Exception("could not download image")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Only run a single animation loop')
    parser.add_argument('angle', type=str,
                        help='the angle we are taking the pictures from (front, back, left, right)')
    parser.add_argument('--camera_url', type=str, default=camera_url,
                        help='the ip address of the ipwebcam')

    args = parser.parse_args()
    
    ANGLE = args.angle
    camera_url = args.camera_url

    # take a few background shots, sometimes the ipwebcam changes zoom for the first few pictures, I dont know why, this gives it time to settle on a zoom setting first before taking the rest of the pictures
    for i in range(3):
        pixels.fill((0,0,0))
        pixels.show()
        take_image(f"./data/{ANGLE}/background.jpg")

    # for each pixel, turn it on and take a picture
    for i in range(num_pixels):
        pixels.fill((0,0,0))
        pixels[i] = (255,255,255)
        pixels.show()

        img_path = f"./data/{ANGLE}/{i:03}.jpg"
        take_image(img_path)

    # change the tree to red for 10 seconds to show we are done
    for i in range(10):
        pixels.fill((255,0,0))
        pixels.show()
        time.sleep(1)

    pixels.fill((0,0,0))
    pixels.show()
