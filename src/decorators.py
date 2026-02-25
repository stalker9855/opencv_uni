from os import listdir
from os.path import isfile, join
from pathlib import Path
import time
import cv2
import functools

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

def reading_image(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
            print(func.__name__.capitalize().replace('_', ' '))
            files = get_files()
            print_files(files)
            while True:
                try:
                    result = func(files, *args, **kwargs)
                    name, _, _ = func.__name__.split('_')
                    filename = f"{name}_image_{time.time()}.jpeg"
                    cv2.imwrite(f"{PATH}/{filename}", result)
                    print(f"SAVE IMAGED IN {PATH}/{filename}")
                except IndexError:
                    print("Image not Found")
    return inner
