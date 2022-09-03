from PIL import Image, ImageEnhance
import config
from typing import Tuple
import os


def generate_txt_from_image(
    *,
    source_img_path: str,
    destination_img_path: str = None,
    scale: str = config.SCALE,
    max_resolution: Tuple[int, int] = None,
    quiet: bool = True,
):
    """Creates txt file containg letters that correspond to
    pixels in darkness scale

    Params
    ------
    source_img_path: str
        Image path

    destination_image_path: str
        Output txt file path
        Default name is [source name].txt

    scale: str
        Chars chain, that will replace corresponding pixels
        from darkest to lightest

    max_resolution: Tuple[int,int]
        Maximal width and hight of the output txt file
        in numbers of letters in line on line number

    quiet: bool
        Indicates if progress messages shoul be displayed
    """

    max_resolution = config.MAX_RESOLUTION if max_resolution is None else max_resolution
    if destination_img_path is None:
        destination_img_path = _get_destination_file_from_source(source_img_path)

    img = _get_image_in_gray_scale(source_img_path)
    preprocessed_img = _preprocess_image(img=img, max_resolution=max_resolution)
    _redner_image_in_txt(
        img=preprocessed_img, scale=scale, destination_file=destination_img_path
    )


def _get_destination_file_from_source(source_file: str) -> str:
    filename_without_extension, _ = os.path.splitext(source_file)
    return filename_without_extension + ".txt"


def _get_image_in_gray_scale(source_img_path: str) -> Image.Image:
    with Image.open(source_img_path) as img:
        return img.convert("L")


def _preprocess_image(
    *, img: Image.Image, max_resolution: Tuple[int, int], sharpness_factor: int = 36
) -> Image.Image:

    # Resize image if bigger than max_resolution
    width, height = img.size
    if width > max_resolution[0]:
        img = img.resize((max_resolution[0], int((max_resolution[0] / width) * height)))

    width, height = img.size
    if height > max_resolution[1]:
        img = img.resize((int((max_resolution[1] / height) * width), max_resolution[1]))

    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(sharpness_factor)

    return img


def _redner_image_in_txt(img: Image.Image, scale: str, destination_file: str) -> None:
    width, height = img.size
    pixels = img.load()
    with open(destination_file, "w") as file:
        for y in range(height):
            for x in range(width):
                file.write(_px2char(pixels[x, y], scale))
            file.write("\n")


def _px2char(px: int, scale) -> str:
    scale_length = len(scale)
    MAX_PX_VALUE = 255
    scale_index = int(round((px / MAX_PX_VALUE) * (scale_length - 1)))
    return scale[scale_index]
