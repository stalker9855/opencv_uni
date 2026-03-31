import time
from datetime import datetime

import cv2
import numpy as np
import pandas as pd

from decorators import PATH, reading_image


def load_image(path, files, flags: int | None = None) -> cv2.typing.MatLike | None:
    index = select_file()
    if index is None:
        print("Can't read image")
        return None
    try:
        image = cv2.imread(f"{path}/{files[index]}", flags)
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


def write_image_command():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if ret is None:
        print("Can't recieve frame.")
    else:
        filename = f"capture_{time.time()}.jpeg"
        cv2.imwrite(f"{PATH}/{filename}", frame)
        print(f"{filename} saved")


@reading_image
def show_image_command(files: None | list = None):
    image = load_image(PATH, files)
    if image is not None:
        show_image(image)


@reading_image
def convert_image_command(files: None | list = None):
    image = load_image(PATH, files)
    if image is not None:
        converted_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return converted_image


@reading_image
def layer_image_command(files: None | list = None):
    image = load_image(PATH, files)
    if image is not None:
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.rectangle(mask, (50, 50), (500, 300), 255, -1)
        masked_image = cv2.bitwise_and(image, image, mask=mask)
        return masked_image


@reading_image
def blur_image_command(files: None | list = None):
    image = load_image(PATH, files)
    if image is not None:
        blur_image = cv2.GaussianBlur(image, (5, 5), 0)
        return blur_image


@reading_image
def edge_image_command(files: None | list = None):
    image = load_image(PATH, files)
    if image is not None:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edge_image = cv2.Canny(gray, 150, 300)
        show_image(edge_image)
        return edge_image


@reading_image
def geometry_image_command(files: None | list = None):
    image = load_image(PATH, files)
    if image is not None:
        start_point = (0, 0)
        end_point = (241, 351)
        color = (123, 255, 22)
        geometry_image = cv2.rectangle(image, start_point, end_point, color, cv2.FILLED)
        result = cv2.circle(image, (250, 250), 40, (22, 122, 240), 2)
        cv2.putText(
            image,
            "Moonshine",
            (50, 70),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            (0, 0, 0),
            2,
            cv2.LINE_AA,
        )
        show_image(result)
        return geometry_image


@reading_image
def text_image_command(files: None | list = None):
    image = load_image(PATH, files)
    if image is not None:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(
            image,
            f"Andrii {time.strftime('%a, %d, %b, %Y %H:%M', time.gmtime())}",
            (10, 450),
            font,
            1,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )
        height, width, _ = image.shape
        res_image = cv2.resize(image, (width // 2, height // 2))
        height, width, _ = res_image.shape
        center = (width // 2, height // 2)
        r_matrix = cv2.getRotationMatrix2D(center, 137, 0.6)
        rotated_image = cv2.warpAffine(res_image, r_matrix, (width, height))
        filename = f"text_image_{time.time()}.jpeg"
        cv2.imwrite(f"{PATH}/{filename}", rotated_image)
        show_image(rotated_image)
        return rotated_image


@reading_image
def shift_image_command(files=None):
    image = load_image(PATH, files)
    if image is not None:
        rows, cols = image.shape[:2]
        tx = 200
        ty = 150

        pts1 = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])

        pts2 = np.float32(
            [[0 + tx, 0 + ty], [cols - 1 + tx, 0 + ty], [0 + tx, rows - 1 + ty]]
        )

        M = cv2.getAffineTransform(pts1, pts2)
        shifted_image = cv2.warpAffine(image, M, (cols, rows))

        show_image(shifted_image)
        return shifted_image


@reading_image
def reflect_image_command(files=None):
    image = load_image(PATH, files)
    if image is not None:
        rows, cols = image.shape[:2]

        pts1 = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])
        pts2 = np.float32([[cols - 1, 0], [0, 0], [cols - 1, rows - 1]])
        M = cv2.getAffineTransform(pts1, pts2)

        reflect_image = cv2.warpAffine(image, M, (cols, rows))

        show_image(reflect_image)
        return reflect_image


@reading_image
def jap_image_command(files=None):
    image = load_image(PATH, files)
    if image is not None:
        # [top-left, top-right, bottom-left, bottom-right]
        width, height = 800, 600
        p1 = np.float32([[412, 185], [994, 245], [246, 549], [1012, 654]])
        p2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(p1, p2)

        result = cv2.warpPerspective(image, matrix, (width, height))
        show_image(result)
        return result


@reading_image
def python_image_command(files=None):
    image = load_image(PATH, files)
    if image is not None:
        # [top-left, top-right, bottom-left, bottom-right]
        width, height = 800, 600
        p1 = np.float32([[450, 60], [1012, 216], [190, 358], [836, 640]])
        p2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(p1, p2)

        result = cv2.warpPerspective(image, matrix, (width, height))
        show_image(result)
        return result


def stream_video():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    out = cv2.VideoWriter(f"{PATH}/output.avi", fourcc, 30.0, (800, 600))
    frame_width, frame_height = 800, 600

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Camera not found")
            break

        frame = cv2.resize(frame, (frame_width, frame_height))
        rect_width, rect_height = 350, 50
        top_left = (frame_width - rect_width - 10, 10)
        bottom_right = (frame_width - 10, 10 + rect_height)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), -1)

        date_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text_position = (top_left[0], top_left[1] + 30)
        cv2.putText(
            frame, date_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2
        )

        out.write(frame)
        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


### START LR9 ###


@reading_image
def match_template_image(files=None):
    image = load_image(PATH, files, cv2.IMREAD_GRAYSCALE)
    template = load_image(PATH, files, cv2.IMREAD_GRAYSCALE)
    if image is not None and template is not None:
        h, w = template.shape

        methods = [
            cv2.TM_CCOEFF,
            cv2.TM_CCOEFF_NORMED,
            cv2.TM_CCORR,
            cv2.TM_CCORR_NORMED,
            cv2.TM_SQDIFF,
            cv2.TM_SQDIFF_NORMED,
        ]

        for method in methods:
            img = image.copy()
            result = cv2.matchTemplate(img, template, method)
            _, _, min_loc, max_loc = cv2.minMaxLoc(result)
            location = (
                min_loc if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED] else max_loc
            )

            bottom_right = (location[0] + w, location[1] + h)
            cv2.rectangle(img, location, bottom_right, 255, 5)

            show_image(img, title=f"{method} image")
            threshold = 0.8
            locations = np.where(result >= threshold)
            df_matches = pd.DataFrame(list(zip(*locations[::-1])), columns=["x", "y"])
            print(f"Знайдені координати фрагментів {method}\n", df_matches)


### END LR9 ####
