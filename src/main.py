import os

from processing.write_image import ImageMap
from processing.get_coordinates import ImageFolder
from database.database import Database


# ========================================
# VALUES TO CHANGE
MAP_NAME = "citadelledaquilon"
MOB_NAME = "chienerrant"
VNUM = 4100
# END OF VALUES TO CHANGE
# ========================================


IMAGE_FOLDER_PATH = os.path.join("src", "processing", "images")
DATABASE_PATH = os.path.join("src", "database", "database.json")


def main():
    image_folder = ImageFolder(path=IMAGE_FOLDER_PATH)
    image_map = ImageMap(map_name=MAP_NAME, mob_name=MOB_NAME)
    database = Database(path=DATABASE_PATH)

    coordinates = image_folder.get_coordinates()

    image_map.write_points(coordinates)
    image_map.save_mask()

    database.add_coordinates(map_name=MAP_NAME, vnum=VNUM, coordinates=coordinates)
    database.save()


if __name__ == "__main__":
    main()
