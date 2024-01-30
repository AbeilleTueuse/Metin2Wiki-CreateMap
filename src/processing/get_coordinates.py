import os

import cv2
import numpy as np


class ImageDigit:
    COORDINATE_MAPPING = [[3, 3], [4, 0], [2, 3], [0, 3], [3, 1], [5, 2], [6, 1]]
    SUM_MAPPING = {71: 0, 96: 1, 68: 2, 84: 3, 15: 4, 88: 5, 82: 6, 8: 7, 86: 8, 85: 9}
    PIXEL_WEIGHT_CONSTANT = 128
    RANK_MULTIPLIER_CONSTANT = 2

    def __init__(self, image):
        self.image = image[:, :, 0]

    def _pixel_weight(self, x, y, rank):
        return (
            self.image[y, x]
            // self.PIXEL_WEIGHT_CONSTANT
            * self.RANK_MULTIPLIER_CONSTANT**rank
        )

    def convert_to_number(self):
        sum_ = sum(
            self._pixel_weight(x, y, rank)
            for rank, [y, x] in enumerate(self.COORDINATE_MAPPING)
        )

        return self.SUM_MAPPING.get(sum_, -1)


class ImageWithCoordinates:
    PINK = np.array([200, 200, 255])
    MARKER = np.loadtxt(
        os.path.join("src", "processing", "mark", "mark_values.txt"), delimiter="\t", dtype=np.uint8
    )

    def __init__(self, path):
        self.image = cv2.imread(path)

    def _color_filter(self):
        mask = cv2.inRange(self.image, self.PINK, self.PINK)
        image_filtered = cv2.bitwise_and(self.image, self.image, mask=mask)

        return image_filtered

    def _find_all_mark(self):
        image_gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

        res = cv2.matchTemplate(self.MARKER, image_gray, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.95)

        return [pt for pt in zip(*loc)]

    def get_coordinates(self):
        def get_one_coordinates(mark):
            image_filtered = self._color_filter()

            coordinates = []
            compt = 0

            for coord_index in range(2):
                number_list = []
                number = 0

                while number != -1:
                    number_image = image_filtered[
                        mark[0] + 1 : mark[0] + 8,
                        mark[1]
                        + 6
                        + 5 * compt
                        + coord_index : mark[1]
                        + 10
                        + 5 * compt
                        + coord_index,
                    ]

                    number = ImageDigit(number_image).convert_to_number()
                    number_list.append(number)

                    compt += 1

                coord = sum(
                    [
                        number * 10**index
                        for index, number in enumerate(number_list[:-1][::-1])
                    ]
                )
                coordinates.append(coord)

            return coordinates

        return [tuple(get_one_coordinates(mark)) for mark in self._find_all_mark()]


class ImageFolder:
    def __init__(self, path):
        self.path = path
        self.images = os.listdir(path)

    def get_coordinates(self):
        def get_coordinates_from_image(image_name):
            image_path = os.path.join(self.path, image_name)
            image_with_coordinates = ImageWithCoordinates(path=image_path)
            coordinates = image_with_coordinates.get_coordinates()

            return coordinates

        return set(
            [
                coord
                for image in self.images
                for coord in get_coordinates_from_image(image)
            ]
        )
