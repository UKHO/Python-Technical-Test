from typing import List, TypedDict, cast

import requests


class BattleShip(TypedDict):
    name: str
    numberOfGuns: float
    lengthInMeters: int
    helipad: bool


class CruiseShip(TypedDict):
    name: str
    numberOfEmergencyRIBs: int
    lengthInMeters: int
    features: List[str]


class CollectionOfShips(TypedDict):
    battleships: List[BattleShip]
    cruiseShips: List[CruiseShip]


class ShipManager:
    __ships: CollectionOfShips

    def __init__(self, ships: CollectionOfShips) -> None:
        self.__ships = ships

    def calculate_total_length_of_ships(self) -> int:
        cumulative_length: int = 0

        for ship in self.__ships["battleships"]:
            cumulative_length += ship["lengthInMeters"]

        for ship in self.__ships["cruiseShips"]:
            cumulative_length += ship["lengthInMeters"]

        return cumulative_length

    # Finds the longest battleship
    def long_ship(self) -> str:
        max_length: int = 0
        found_thing: str = ""

        for ship in self.__ships["battleships"]:
            if ship["lengthInMeters"] > max_length:
                max_length = ship["lengthInMeters"]
                found_thing = ship["name"]

        return found_thing


class ShipManagerBuilder:
    __url: str

    def __init__(self, url: str) -> None:
        self.__url = url

    def create_ship_manager(self) -> ShipManager:
        response = requests.get(self.__url)

        ships: CollectionOfShips = cast(CollectionOfShips, response.json())

        return ShipManager(ships)


def run():
    smb = ShipManagerBuilder("https://lemon-pond-0c20b7303.1.azurestaticapps.net/ships.json")
    shipManager: ShipManager = smb.create_ship_manager()

    print(f"The longest battleship is {shipManager.long_ship()}")
    print(f"The total length of all the ships is {shipManager.calculate_total_length_of_ships()}")


run()
