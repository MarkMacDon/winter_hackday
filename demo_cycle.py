import importlib
import inspect
import itertools
from pathlib import Path

from tree_animator import TreeAnimator


def get_inheritors(klass, search_dir):
    subclasses = set()

    for x in Path(search_dir).rglob("*.py"):
        try:
            module_name = ".".join(x.parts).replace(".py", "")
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, klass) and obj != klass:
                    subclasses.add(obj)
        except Exception as e:
            pass
            # print(e)

    return subclasses

if __name__ == "__main__":
    animation_classes = get_inheritors(TreeAnimator, "animations")

    coords_path = "./data/test_coords.csv"
    animation_duration = 15

    for anim_class in itertools.cycle(animation_classes):
        print(f"Changing animation to {anim_class.__name__}")
        current_animation = anim_class(coords_path)
        current_animation.animation_loop(n_time=animation_duration)