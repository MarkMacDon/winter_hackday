import csv
import neopixel
import board

pixel_pin = board.D18
ORDER = neopixel.RGB

num_pixels = 150

if __name__ == "__main__":
    with open("./data/coords.csv", "r") as f:
        reader = csv.reader(f)
        pixel_coords = []
        for row in reader:
            id, x, y = row
            id = int(id)
            x = int(x)
            y = int(y)
            pixel_coords.append((id, x, y))

    y_sorted = sorted(pixel_coords, key=lambda e:e[2])


    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=ORDER
    )

    curr_y_thresh = 0
    add_dir = 1
    while True:
        pixels.fill((0,255,0))
        for p in y_sorted:
            if p[2] > curr_y_thresh:
                pixels[p[0]] = (255,0,0)

        print(curr_y_thresh)
        if curr_y_thresh < 0 or curr_y_thresh >= 800:
            add_dir = add_dir * -1

        curr_y_thresh = curr_y_thresh + add_dir


        pixels.show()
