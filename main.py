import shutil
import time
import board
import neopixel
import requests

pixel_pin = board.D18
ORDER = neopixel.RGB

num_pixels = 150
camera_url = "http://192.168.1.71:8080/photo.jpg"

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=ORDER
)

def take_image(filename):
    print(f"download: {filename}")
    r = requests.get(camera_url, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        raise Exception("could not download image")


if __name__ == "__main__":
    pixels.fill((0,0,0))
    pixels.show()
    take_image("./data/background.jpg")

    for i in range(num_pixels):
        pixels.fill((0,0,0))
        pixels[i] = (255,255,255)
        pixels.show()

        img_path = f"./data/{i:03}.jpg"
        take_image(img_path)

    for i in range(10):
        pixels.fill((255,0,0))
        pixels.show()
        time.sleep(0.5)

    pixels.fill((0,0,0))
    pixels.show()
