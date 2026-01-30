import cv2
import numpy as np
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

def load_image(path, files) -> cv2.typing.MatLike | None:
    index = select_file()
    if index is None:
        print("Can't read image")
        return None
    try: 
        image = cv2.imread(f"{path}/{files[index]}")
        if image is None:
            return None
        return image
    except Exception as e:
        print(e)
        return None

def show_image(image: cv2.typing.MatLike, title="image") -> None:
    cv2.imshow(f"{title}", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def select_file() -> int | None:
     cmd = input("Select file: ")
     if cmd.lower() == "q":
         return
     return int(cmd)



def menu() -> None:
    files = get_files()
    while True:
        print(f"Select command\n[l] - list images\n[w] - make a screenshot caputre camera and save\n[s] - show image\n[c] - convert image\n[blur] - blur image\n[layer] - layer image\n[edge] - edge image\n[q] - quit")
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
                print_files(files)
                while True:
                    try:
                        image = load_image(PATH, files)
                        if image is not None:
                            show_image(image)
                    except IndexError:
                        print("Image not Found")
            case "c":
                    print_files(files)
                    while True:
                        try:
                            image = load_image(PATH, files)
                            if image is not None:
                                convert_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                                filename = f"converted_image_{time.time()}.jpeg"
                                cv2.imwrite(f"{PATH}/{filename}", convert_image)
                                files.append(filename)
                        except Exception:
                            pass

            ### START LR2 ###
            case "layer":
                print_files(files)
                while True:
                    try: 
                        image = load_image(PATH, files)
                        if image is None:
                            continue
                        mask = np.zeros(image.shape[:2], dtype="uint8")
                        cv2.rectangle(mask, (50,50), (500, 300), 255, -1)
                        masked_image = cv2.bitwise_and(image, image, mask=mask)
                        show_image(masked_image, "masked_image")
                    except Exception as e:
                        print(e)
            case "blur":
                print_files(files)
                while True:
                    try:
                        image = load_image(PATH, files)
                        if image is None:
                            continue
                        blur = cv2.GaussianBlur(image, (5,5), 0)
                        cv2.imshow(f"blur", blur)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                    except Exception as e:
                        print(e)

            case "edge":
                print_files(files)
                while True:
                    try:
                        image = load_image(PATH, files)
                        if image is None:
                            continue
                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        edge = cv2.Canny(gray, 150, 300)
                        show_image(edge)
                    except Exception as e:
                        print(e)


            ### END LR2 ###

            case "quit" | "q":
                break


def main() -> None:
    menu()


if __name__ == "__main__":
    main()
