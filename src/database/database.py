import json


class Database:
    def __init__(self, path: str):
        self.path = path
        self.database = self._open_data()

    def _open_data(self) -> dict:
        with open(self.path, "r") as file:
            database = json.load(file)

        return database

    def is_in_database(self, map_name: str):
        return map_name in self.database

    def add_map(self, map_name: str):
        if not self.is_in_database(map_name):
            self.database[map_name] = {}
            print(f"Map {map_name} added in the database.")

        else:
            print(f"The map {map_name} is already in the database.")

    def all_map_in_database(self):
        return list(self.database.keys())

    def add_coordinates(
        self, map_name: str, vnum: int, coordinates: set[list[int, int]]
    ):
        vnum = str(vnum)
        coordinates = list(coordinates)

        if self.is_in_database(map_name):
            map_data = self.database[map_name]

            if vnum in map_data:
                print(f"Vnum {vnum} is already in the map {map_name}.")
                print(f"This vnum contains {len(map_data[vnum])} coordinates.")
                overwrite = input("Do you want to overwrite them? [Y/N] ")

                if overwrite.lower() == "y":
                    map_data[vnum] = coordinates
                    print(
                        f"Vnum {vnum} remplaced in the map {map_name} by {len(coordinates)} coordinates."
                    )

                else:
                    print("Action canceled.")

            else:
                map_data[vnum] = coordinates
                print(
                    f"Vnum {vnum} added in the map {map_name} with {len(coordinates)} coordinates."
                )

        else:
            print(
                f"The map {map_name} isnt in the database\n"
                f'List of map in the database:\n {", ".join(self.all_map_in_database())}'
            )

            add_map = input(
                f"Do you want to add the map {map_name} in the database? [Y/N] "
            )

            if add_map.lower() == "y":
                self.add_map(map_name)

    def delete_map(self, map_name: str):
        if self.is_in_database(map_name):
            print(f"Map {map_name} contains {len(self.database[map_name])} vnum.")
            delete = input("Do you want to delete them? [Y/N] ")

            if delete.lower() == "y":
                del self.database[map_name]
                print(f"Map {map_name} deleted.")
            else:
                print("Action canceled.")

        else:
            print(f"The map {map_name} isnt in the database.")

    def delete_vnum(self, map_name: str, vnum: int):
        vnum = str(vnum)

        if self.is_in_database(map_name):
            if vnum in self.database[map_name]:
                print(
                    f"Vnum {vnum} contains {len(self.database[map_name][vnum])} coordinates."
                )
                delete = input("Do you want to delete them? [Y/N] ")
                if delete.lower() == "y":
                    del self.database[map_name][vnum]
                    print(f"Vnum {vnum} deleted.")
                else:
                    print("Action canceled.")

            else:
                print(f"The vnum {vnum} isnt in the map {map_name}.")

        else:
            print(f"The map {map_name} isnt in the database.")

    def save(self):
        with open(self.path, "w") as file:
            json.dump(self.database, file)
