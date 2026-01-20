import cv2
import time
from os import listdir
from os.path import isfile, join
from enum import Enum
from pathlib import Path

PATH = "./assets/"
Path(PATH).mkdir(parents=True, exist_ok=True)



def get_files() -> list[str]:
    return [f for f in listdir(PATH) if isfile(join(PATH,f))]

def print_files(files: list[str]) -> None:
    if len(files) == 0:
        print("No files")
        return
    for index, file in enumerate(files):
        print(f"[{index}] - {file}")

def show_image(file: str) -> None:
    image = cv2.imread(f"{PATH}/{file}") 
    if image is None:
        print("Image not Found")
        return
    cv2.imshow(f"{file}", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def menu() -> None:
    files = get_files()
    while True:
        print(f"Select command\n[l] - list images\n[w] - make a screenshot caputre camera and save\n[s] - show image\n[0..{len(files) - 1}] - show image\n[q] - quit")
        command = input("> ").strip().lower()
        match command:
            case "l" | "ls":
                print_files(files)

            case "w":
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                cap.release()
                if ret is None:
                    print("Can\'t recieve frame.")
                else:
                    filename = f"capture_{time.time()}.jpeg"
                    cv2.imwrite(f"{PATH}/{filename}", frame)
                    files.append(filename)
                    print(f"{filename} saved")
            case "s":
                print("[q] - back to menu")
                print_files(files)
                while True:
                    cmd_select = input("Select file: ")
                    if cmd_select.lower() == "q":
                        break
                    try:
                        index = int(cmd_select)
                        show_image(files[index])
                    except IndexError:
                        print("Image not Found")
            case "c":
                    print("[q] - back to menu")
                    print_files(files)
                    cmd_select = input("Select file: ")
                    if cmd_select.lower() == "q":
                        break
                    index = int(cmd_select)
                    try:
                        image = cv2.imread(f"{PATH}/{files[index]}") 
                        if image is not None:
                            convert_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                            filename = f"converted_image_{time.time()}.jpeg"
                            cv2.imwrite(f"{PATH}/{filename}", convert_image)
                            files.append(filename)
                    except Exception:
                        pass

            case "quit" | "q":
                break

            case command if 0 <= int(command) <= len(files):
                try:
                    index = int(command)
                    show_image(files[index])
                except IndexError:
                    print("Image not found")


def main() -> None:
    menu()


if __name__ == "__main__":
    main()
