from enum import StrEnum, Enum

class TextColor(StrEnum):
    pink = "pink"
    green = "green"
    blue = "blue"
    red = "red"
    orange = "orange"
    yellow = "yellow"

class TextColorCodes(Enum):
    pink = (236, 113, 115)
    green = (0, 128, 0)
    blue = (29, 32, 236)
    red = (225, 13, 17)
    orange = (241, 152, 0)
    yellow = (255, 255, 0)
