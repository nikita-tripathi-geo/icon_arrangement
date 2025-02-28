import math

class Icon:
    def __init__(self, icon_id, width, height, priority = 1):
        self.id = icon_id
        self.width = math.ceil(width)
        self.height = math.ceil(height)
        self.priority = priority

class Wall:
    def __init__(self, wall_id, width, height):
        self.id = wall_id
        self.width = math.ceil(width)
        self.height = math.ceil(height)
        self.hung_icons = []
        self.available_height = self.height

    def can_hang_icon(self, icon):
        return icon.width <= self.width and icon.height <= self.available_height

    def hang_icon(self, icon, x_pos):
        self.hung_icons.append((icon, x_pos))
        self.available_height -= icon.height


def arrange_icons(icons, walls):
    # Sort icons based on priority
    icons.sort(key=lambda icon: icon.priority, reverse=True)

    # Sort walls based on their height (descending)
    walls.sort(key=lambda wall: wall.height, reverse=True)

    unhung_icons = []

    for icon in icons:
        best_wall = None
        best_x_pos = 0

        for wall in walls:
            if wall.can_hang_icon(icon):
                for x_pos in range(0, wall.width - icon.width + 1, 1):
                    if all(
                            (
                                    hung_icon[1] + hung_icon[0].width <= x_pos or
                                    hung_icon[1] >= x_pos + icon.width
                            )
                            for hung_icon in wall.hung_icons
                    ):
                        best_wall = wall
                        best_x_pos = x_pos
                        break
                if best_wall:
                    break

        if best_wall:
            best_wall.hang_icon(icon, best_x_pos)
        else:
            unhung_icons.append(icon)

    return walls, unhung_icons


def main():
    from convert_list import parse_csv

    icon_list = parse_csv("sortly-list.csv")

    icons = []

    for [i, name, width, height] in icon_list:
        icons.append(Icon(i, width, height))

    # Example icons and walls data (replace this with your actual data)
    # icons = [
    #     Icon(1, 180, 242),
    #     Icon(2, 112, 137),
    #     Icon(3, 120, 200, 9),
    #     Icon(4, 50, 70, 6),
    #     # Add more icons here...
    # ]

    walls = [
        Wall(1, 300, 400),
        Wall(2, 250, 350),
        Wall(3, 400, 300),
        # Add more walls here...
    ]

    arranged_walls, unhung_icons = arrange_icons(icons, walls)

    # Output results
    print("Arranged Icons:")
    for wall in arranged_walls:
        print(f"Wall {wall.id}:")
        for icon, x_pos in wall.hung_icons:
            print(f"Icon {icon.id} - Position: ({x_pos}, 0), Size: ({icon.width}, {icon.height})")
        print("-" * 30)

    print("\nUnhung Icons:")
    for icon in unhung_icons:
        print(f"Icon {icon.id} - Size: ({icon.width}, {icon.height})")


if __name__ == "__main__":
    main()
