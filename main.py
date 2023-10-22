import requests
from bs4 import BeautifulSoup
import csv

collection_url = "https://steamcommunity.com/sharedfiles/filedetails/?id=2902479114"

def parse_size(addon_url):
    page = requests.get(addon_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    size = soup.find("div", class_="detailsStatRight").text.strip()
    size = float(size[:-3].replace(",", ""))

    return size

def save_to_csv(filename, addon_details):
    with open(filename, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["name", "size", "url"])

        for addon in addon_details:
            writer.writerow([addon["title"], f'{addon["size"]} MB', addon["url"]])

def main():
    page = requests.get(collection_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    workshop_items = soup.find_all("div", class_="collectionItem")

    addon_details = []

    for addon in workshop_items:
        details = addon.find("div", class_="collectionItemDetails")

        addon_url = details.find("a")["href"]
        addon_title = details.find("div", class_="workshopItemTitle").text.strip()
        addon_size = parse_size(addon_url)

        print(addon_url, addon_title, addon_size)

        addon_details.append({
            "title": addon_title,
            "size": addon_size,
            "url": addon_url
        })

    # sort addon_details by size
    addon_details.sort(key=lambda addon: addon["size"], reverse=True)

    save_to_csv("addons.csv", addon_details)

if __name__ == "__main__":
    main()