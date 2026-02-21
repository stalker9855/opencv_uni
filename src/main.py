from core import *
from decorators import get_files, print_files




def menu() -> None:
    commands = {
        "l": ("list images", lambda: print_files(get_files())),
        "ls": ("alias for list", lambda: print_files(get_files())),
        "w": ("capture camera and save", write_image_command),
        "s": ("show image", show_image_command),
        "c": ("convert image", convert_image_command),
        "blur": ("blur image", blur_image_command),
        "layer": ("layer image", layer_image_command),
        "edge": ("edge image", edge_image_command),
        "geometry": ("add geometries", geometry_image_command),
        "text": ("add text to image", text_image_command),
        "shift": ("shift image", shift_image_command),
        "reflect": ("reflect image", reflect_image_command),
        "q": ("quit", None),
        "quit": ("quit", None)
    }
    while True:
        print("\n--- Select command ---")
        for key, (desc, _) in commands.items():
            print(f"[{key}] - {desc}")
        action = input("> ").strip().lower()
        if action in commands:
            _, func = commands[action]
            if func:
                func()
        else:
            print(f"Uknown command: {action}")


def main() -> None:
    menu()


if __name__ == "__main__":
    main()
