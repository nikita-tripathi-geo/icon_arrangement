"""TODO
"""
import math
import json

MARGIN = 10

class Icon:
    """
    Represents an icon with a unique ID, dimensions, and priority.

    Attributes:
        id (int): Unique identifier for the icon. Used to track the images.
        width (int): The width of the icon, rounded up to the nearest integer.
        height (int): The height of the icon, rounded up to the nearest integer.
        priority (int): The priority of the icon for hanging (higher is more important).
    """

    def __init__(self, icon_id: int, width: float, height: float, priority: int = 1):
        self.id = icon_id
        self.width = math.ceil(width)
        self.height = math.ceil(height)
        self.priority = priority

class Wall:
    """
    Represents a wall where icons can be hung.

    Attributes:
        id (int): Unique identifier for the wall.
        width (int): The width of the wall.
        height (int): The height of the wall.
        hung_icons (list): List of icons hung on the wall with their coordinates.
    """

    def __init__(self, wall_id: int, width: float, height: float, priority: int = 0):
        self.id = wall_id
        self.width = math.ceil(width)
        self.height = math.ceil(height)
        self.hung_icons: list(Icon) = []
        self.priority = priority

    def can_hang_icon(self, icon: Icon, x_pos: int, y_pos: int) -> bool:
        """
        Checks if an icon can be hung on the wall at the specified position.

        Args:
            icon (Icon): The icon to check.
            x_pos (int): The x-coordinate of the top-left corner of the icon.
            y_pos (int): The y-coordinate of the top-left corner of the icon.

        Returns:
            bool: True if the icon can be hung, False otherwise.
        """
        if x_pos + icon.width > self.width or y_pos + icon.height > self.height:
            return False

        for hung_icon, (hx, hy) in self.hung_icons:
            if not (hx + hung_icon.width + MARGIN <= x_pos or hx >= x_pos + icon.width + MARGIN or
                    hy + hung_icon.height + MARGIN <= y_pos or hy >= y_pos + icon.height + MARGIN):
                return False

        return True

    def hang_icon(self, icon: Icon, x_pos: int, y_pos: int):
        """
        Hangs an icon on the wall at the specified position.

        Args:
            icon (Icon): The icon to hang.
            x_pos (int): The x-coordinate for the icon's position.
            y_pos (int): The y-coordinate for the icon's position.
        """
        self.hung_icons.append((icon, (x_pos, y_pos)))

def arrange_icons(icons: list, walls: list, accuracy: int) -> tuple:
    """
    Arranges icons on walls based on priority and available space.

    Args:
        icons (list): A list of icons to arrange.
        walls (list): A list of walls where icons can be hung.
        accuracy (int): An integer that describes how carefully we search the walls 
            for available space

    Returns:
        tuple: A tuple containing the updated list of walls with hung icons 
               and a list of icons that couldn't be hung.
    """
    # # Sort icons based on priority (descending)
    # icons.sort(key=lambda icon: icon.priority, reverse=True)
    icons.sort(key=lambda icon: (icon.priority, icon.height*icon.width), reverse=True)

    # # Sort walls based on their priority (descending)
    # walls.sort(key=lambda wall: wall.width, reverse=True)
    walls.sort(key=lambda wall: wall.priority, reverse=True)

    # unhung_icons = []
    unhung_icons = []

    wall_height = 850

    for icon in icons:
        placed = False

        for y_pos in range(wall_height - icon.height, -1, -accuracy):  # Start from the bottom
            for wall in walls:
                for x_pos in range(0, wall.width - icon.width + 1, accuracy):
                    if wall.can_hang_icon(icon, x_pos, y_pos):
                        wall.hang_icon(icon, x_pos, y_pos)
                        placed = True
                        break
                if placed:
                    break
            if placed:
                break
        if not placed:
            unhung_icons.append(icon)

    return walls, unhung_icons



def main():
    """
    Demonstrates the arrangement of icons on walls using sample data.

    Reads a CSV file for icon data, arranges icons on walls, and prints the results.
    """
    icons = []

    # 3 cm (~1 in) margins
    margin = 10

    with open("icons.json", "r", encoding="utf-8") as icon_file:
        # load json and convert to Icons
        icons = [
            Icon(icon["id"], icon["width"], icon["height"], icon["priority"])
            for icon in json.load(icon_file)
        ]



    walls = [
        Wall(1, 2505, 850, 10),
        Wall(2, 2530, 850, 2),
        Wall(3, 1440, 850, 3),
        Wall(4, 3100, 850, 7),
        Wall(5, 1155, 850, 5),
        Wall(6, 1750, 850, 5),
        Wall(7, 1155, 850, 5),
        Wall(8, 3100, 850, 7),
        Wall(9, 1410, 850, 3),
        Wall(10, 2530, 850, 2),
        Wall(11, 2230, 850, 10),
    ]

    arranged_walls, unhung_icons = arrange_icons(icons, walls, 5)

    print("Arranged Icons:")
    for wall in arranged_walls:
        print(f"Wall {wall.id}:")
        for icon, (x, y) in wall.hung_icons:
            print(f"Icon {icon.id} - Position: ({x}, {y}), Size: ({icon.width}, {icon.height})")
        print("-" * 30)

    print("\nUnhung Icons:")
    for icon in unhung_icons:
        print(f"Icon {icon.id} - Size: ({icon.width}, {icon.height})")

    return arranged_walls, unhung_icons

if __name__ == "__main__":
    main()
