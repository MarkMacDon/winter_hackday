import itertools

from demo_cycle import get_inheritors
from tree_animator import TreeAnimator

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Only run a single animation loop')
    parser.add_argument('animation_name', type=str,
                        help='name of the animation class you wish to run')
    parser.add_argument('--coords', type=str,
                        help='the location of a coordinates file')

    args = parser.parse_args()

    # remove .py from the end of the string, we only care about the name of the animation class, not the file type
    desired_animation_name = args.animation_name.lower()
    if desired_animation_name.endswith(".py"):
        desired_animation_name = desired_animation_name[:-3]

    # find the animation class that matches the desired_animation_name
    animation_classes = get_inheritors(TreeAnimator, "animations")
    class_found = None
    # for each available TreeAnimator, check its file name and class name to see if it matches the desired animation name
    for klass in animation_classes:
        # compare the class and module name in lowercase
        class_module_name = klass.__module__.split(".")[-1].lower()
        class_name = klass.__name__.lower()

        # if we have found it, break out of the for loop
        if class_module_name == desired_animation_name or class_name == desired_animation_name:
            class_found = klass
            break

    # if we didnt find anything, give a handy error message
    if class_found is None:
        candidates = "\n".join(["\t'" + c.__module__.split(".")[-1] + "' or '" + c.__name__ + "'" for c in animation_classes])
        print(f"Sorry, no animation named {args.animation_name} could be found. Possible candidates are:")
        print(candidates)
        exit()

    print(f"Changing animation to {class_found.__name__}")
    current_animation = class_found(coords_path=args.coords)
    current_animation.animation_loop()