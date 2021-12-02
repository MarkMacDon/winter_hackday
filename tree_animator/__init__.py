import io

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception:
        pass
    return False

# assigns the TreeAnimator class to either a testbed for local development
# or if the code detects it is running on a pi, it uses the neopixel animator class to control the real lights
if is_raspberrypi():
    from tree_animator.neopixel_animator import NeopixelAnimator
    TreeAnimator = NeopixelAnimator
else:
    from tree_animator.test_animator import TestAnimator
    TreeAnimator = TestAnimator