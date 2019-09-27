#!/usr/bin/env python3
import os
import time
import json
import requests

# Download files relative to this script rather than the user's cwd
scriptdir =  os.path.abspath(os.path.dirname(__file__))

def download(url, filename):
    # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(os.path.join(scriptdir, filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

def get_all_cards(cachedir="cache", filename="scryfall-default-cards.json", cache_ttl=604800):
    url = "https://archive.scryfall.com/json/scryfall-default-cards.json"
    filename = os.path.join(scriptdir, cachedir, filename)
    create_file = True
    try:
        st = os.stat(filename)
    except FileNotFoundError:
        pass
    else:
        if time.time() < st.st_mtime + cache_ttl:
            create_file = False

    if create_file:
        download(url, filename)

    with open(filename, encoding="utf_8") as f:
        return json.load(f)

def download_set_images(set):
    setname = requests.get("https://api.scryfall.com/sets/{}".format(set)).json()["name"]
    setdir = "art_crop_img_{}".format(setname.replace(" ", "_"))
    os.mkdir(os.path.join(scriptdir, setdir))
    for card in filter(lambda x: x["set"] == set, get_all_cards()):
        for card_face in card.get("card_faces", [card]):
            filename = "{}_{}_art_crop.jpg".format(card_face["name"].replace(" ", "_"), card["collector_number"])
            download(card_face["image_uris"]["art_crop"], os.path.join(setdir, filename))

if __name__ == "__main__":
    for set in ("ktk", "m19"):
        download_set_images(set)
