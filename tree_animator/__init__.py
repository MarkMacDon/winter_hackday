import io

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception:
        pass
    return False

if is_raspberrypi():
    from tree_animator.neopixel_animator import NeopixelAnimator
    TreeAnimator = NeopixelAnimator
else:
    from tree_animator.test_animator import TestAnimator
    TreeAnimator = TestAnimator