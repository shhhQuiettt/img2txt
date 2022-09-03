from unittest import TestCase
import os
from img2txt import generate_txt_from_image
from PIL import Image
from typing import Tuple

TEST_IMG_FILENAME = os.path.join("tests", "test_image.webp")


def setUpModule():
    assert os.path.exists(TEST_IMG_FILENAME)


def get_txt_image_size(img_filename: str) -> Tuple[int, int]:
    with open(img_filename) as file:
        # - 1 in order to subtrackt \n
        txt_width = len(file.readline()) - 1
        # +1 in order to add line, that hs been already read
        txt_height = sum(1 for line in file) + 1
    return txt_width, txt_height


class GenerateTxtFromImageWithoutDestination(TestCase):
    @classmethod
    def setUpClass(cls):
        filename_without_extension, _ = os.path.splitext(TEST_IMG_FILENAME)
        cls.expected_destination_file = filename_without_extension + ".txt"
        cls.source_file = TEST_IMG_FILENAME

    def tearDown(self):
        try:
            os.remove(self.expected_destination_file)
        except FileNotFoundError:
            pass

    def test_when_only_source_given(self):
        generate_txt_from_image(source_img_path=self.source_file)

        self.assertTrue(os.path.exists(self.expected_destination_file))

    def test_when_scale_given(self):
        scales = ["@1.", "#$5gio.", " .123#$@"]

        for scale in scales:
            with self.subTest(scale):
                generate_txt_from_image(
                    source_img_path=self.source_file,
                    scale=scale,
                )

        self.assertTrue(os.path.exists(self.expected_destination_file))

    def test_when_max_resolution_bigger_than_image(self):
        with Image.open(self.source_file) as img:
            img_width, img_height = img.size
            max_resolution = (img_width * 2, img_height * 2)
            generate_txt_from_image(
                source_img_path=self.source_file, max_resolution=max_resolution
            )

        self.assertTrue(os.path.exists(self.expected_destination_file))

        txt_width, txt_height = get_txt_image_size(self.expected_destination_file)
        self.assertEqual(img_width, txt_width)
        self.assertEqual(img_height, txt_height)

    def test_when_max_resolution_width_smaller_than_image(self):
        with Image.open(self.source_file) as img:
            img_width, img_height = img.size
            img_resolution = img_width // img_height
            max_resolution = (img_width // 2, img_height * 2)
            generate_txt_from_image(
                source_img_path=self.source_file, max_resolution=max_resolution
            )

        self.assertTrue(os.path.exists(self.expected_destination_file))

        txt_width, txt_height = get_txt_image_size(self.expected_destination_file)
        txt_resolution = txt_width // txt_height

        self.assertEqual(max_resolution[0], txt_width)
        self.assertAlmostEqual(img_resolution, txt_resolution)

    def test_when_max_resolution_height_smaller_than_image(self):
        with Image.open(self.source_file) as img:
            img_width, img_height = img.size
            img_resolution = img_width // img_height
            max_resolution = (img_width * 2, img_height // 2)
            generate_txt_from_image(
                source_img_path=self.source_file, max_resolution=max_resolution
            )

        self.assertTrue(os.path.exists(self.expected_destination_file))

        txt_width, txt_height = get_txt_image_size(self.expected_destination_file)
        txt_resolution = txt_width // txt_height
        self.assertEqual(max_resolution[1], txt_height)

        self.assertAlmostEqual(img_resolution, txt_resolution)

    def test_when_max_resolution_height_and_width_smaller_than_image(self):
        with Image.open(self.source_file) as img:
            img_width, img_height = img.size
            img_resolution = img_width // img_height

            max_resolution = (img_width // 2, img_height // 2)
            generate_txt_from_image(
                source_img_path=self.source_file, max_resolution=max_resolution
            )

        self.assertTrue(os.path.exists(self.expected_destination_file))

        txt_width, txt_height = get_txt_image_size(self.expected_destination_file)
        txt_resolution = txt_width // txt_height

        self.assertEqual(max_resolution[0], txt_width)
        self.assertEqual(max_resolution[1], txt_height)
        self.assertAlmostEqual(img_resolution, txt_resolution)
