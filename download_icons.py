"""
TODO
"""
import csv
import urllib.request
from PIL import Image

def read_urls(csvname: str):
    """
    Takes the name of our csv file (which is provided by Sortly)
    Finds all URLs that point to pictures of Icons
    Downloads them and names them according to the ID of the Icon.
    """

    with open(csvname, "r", encoding="utf-8", newline="") as csvfile:
        # Read file
        reader = csv.reader(csvfile)

        for i, row in enumerate(reader):
            if i == 0:
                continue

            print(row[1])

            url = row[1]

            urllib.request.urlretrieve(url, f"icons/{i}.jpg")

    return


def jpg_2_png(directory: str):
    """
    Assumes there are 137 Icons
    """
    for i in range(1, 138):
        im = Image.open(f"{directory}/{i}.jpg")
        im.save(f"{directory}/{i}.png")

# read_urls("sortly-list.csv")
jpg_2_png("icons")
