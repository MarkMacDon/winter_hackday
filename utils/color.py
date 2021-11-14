import numpy as np
import colorsys

def hsv_to_rgb(h, s, v):
    # converts Hue (0-360) and saturation and value into RGB colors (0-255)
    h = (h%360)/360
    rgb = colorsys.hsv_to_rgb(h,s,v)
    return (np.array(rgb) * 255).astype(np.uint8)
