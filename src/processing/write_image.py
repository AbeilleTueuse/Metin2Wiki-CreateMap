import os

import cv2
import numpy as np


class ImageMap:
    MOB_COLOR = [0, 0, 255, 127]
    MAP_INFO_PATH = os.path.join("src", "data", "map_size.txt")
    RESULT_PATH = os.path.join("src", "result")

    def __init__(self, map_name: str, mob_name: str, max_height=640, square_size=4):
        self.map_name = map_name
        self.mob_name = mob_name

        self.width = None
        self.height = None

        self._get_map_size()

        self.max_height = max_height

        if self.height <= self.max_height:
            self.resize_height = self.height
            self.resize_width = self.width

            self.prop = 1

        else:
            self.resize_height = self.max_height
            self.resize_width = int(self.width * self.max_height / self.height)

            self.prop = self.max_height / self.height

        self.square_size = square_size

    def _get_map_size(self):
        with open(self.MAP_INFO_PATH, "r") as file:
            lines = file.readlines()

        for line in lines:
            name, width, height = line.strip().split("\t")

            map_name = self.map_name

            if name == map_name:
                self.width = int(width)
                self.height = int(height)

                break

        if self.width is None or self.height is None:
            raise ValueError(
                f"Le nom {map_name} n'a pas pu être trouvé dans le fichier {self.MAP_INFO_PATH}."
            )

    def _resize_coord(self, coordinates):
        return [round(coordinates[0] * self.prop), round(coordinates[1] * self.prop)]

    def write_points(self, coordinates):
        mask = np.full(
            (self.resize_height, self.resize_width, 4),
            (255, 255, 255, 0),
            dtype=np.uint8,
        )

        for coord in coordinates:
            coord = self._resize_coord(coord)

            square_size = self.square_size

            square: np.ndarray = mask[
                coord[1] - square_size // 2 : coord[1] + square_size // 2,
                coord[0] - square_size // 2 : coord[0] + square_size // 2,
            ]

            if square.shape[:-1] != (square_size, square_size):
                print(f"the coord {coord} cannot be written")

            else:
                alpha1 = square[:, :, 3] / 255
                alpha2 = self.MOB_COLOR[3] / 255

                square[:, :, :-1] = self.MOB_COLOR[:-1]
                square[:, :, 3] = (alpha1 + alpha2 * (1 - alpha1)) * 255

        self.mask = mask

        return mask

    def save_mask(self):
        save_path = os.path.join(
            self.RESULT_PATH, f"Zonedapparition{self.mob_name}.png"
        )

        if os.path.exists(save_path):
            print(f"Image Zonedapparition{self.mob_name}.png already exists.")
            overwrite = input("Do you want to overwrite it? [Y/N] ")
            if overwrite:
                cv2.imwrite(save_path, self.mask)
                print(f"Image saved in {self.RESULT_PATH}.")

            else:
                print("Action canceled.")

        else:
            cv2.imwrite(save_path, self.mask)
            print(f"Image saved in {self.RESULT_PATH}.")
