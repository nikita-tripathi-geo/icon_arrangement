#
import csv      # Used to read from the sortly list and create a new one
import re       # Regular expressions to search for dimensions in the list 
# import math

def frac_str_to_int(frac: str) -> int:
    """
    TODO
    """
    result = 0

    # print(frac)
    frac = frac.strip().split(" ")

    result += int(frac[0])

    if len(frac) > 1:
        frac = frac[1].split("/")
        result += int(frac[0]) / int(frac[1])

    return result



def parse_csv(filename: str):
    """
    TODO
    """

    # icons contains tuples (ID, name, length, width)
    icons = []

    with open(filename, "r", encoding="utf-8", newline="") as csvfile:
        # open file
        reader = csv.reader(csvfile)


        # read and parse each line
        for i, row in enumerate(reader):
            # i is the ID
            # row contains the name, dimensions, and link to photo
            if i == 0:
                # skip the header
                continue

            print(row[0])

            # Use regular expressions to search for the pattern:  _ x _
            dim = re.search(r"\d[\d|\s|\/]*х[\d|\s|\/]+", row[0])
            dim_start = dim.start()
            x = re.search(r" х [\d|\s|\/]+", row[0])
            x_start = x.start()+1

            name = row[0][:dim_start]
            width = row[0][dim_start:x_start]
            length = row[0][x_start+1:]


            # convert strings to ints
            # convert imperial measurements to metric (inch to mm)
            # multiply inches by 25.4 to get millimeters
            width = frac_str_to_int(width) * 25.4
            length = frac_str_to_int(length) * 25.4

            # print(i, name, width, length)
            print(i, name, "w =", width, "l =", length)

            # write to a new list
            icons.append([i, name, width, length])


    with open(f"converted_{filename}", "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        writer.writerows(icons)


    return icons





def main():

    parse_csv("sortly-list.csv")

    return

if __name__ == "__main__":
    main()
