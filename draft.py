#!/usr/bin/env python3
import os
import glob
import json
import random

def filter_params(blob, params):
    for param in params:
        blob = list(filter(lambda x: params[param] == x[param], blob))

    return blob

def not_params(blob, params):
    for param in params:
        blob = list(filter(lambda x: params[param] != x[param], blob))

    return blob

def contains_params(blob, params):
    for param in params:
        blob = list(filter(lambda x: params[param] in x[param], blob))

    return blob

def not_contains_params(blob, params):
    for param in params:
        blob = list(filter(lambda x: params[param] not in x[param], blob))

    return blob

def generate_pack(set_code):
    cards_in_set = filter_params(all_cards, {"set": set_code})
    pack = {}
    pack_position = 0
    for sheet in pack_template.get(set_code, pack_template)["pack_contents"].values():
        possible_cards = cards_in_set[::]
        # Select one of the parameter sets based on weight
        sheet = random.choices(sheet, weights=[x.get("weight", 1) for x in sheet])[0]
        possible_cards = filter_params(possible_cards, sheet.get("params", {}))
        possible_cards = not_params(possible_cards, sheet.get("not_params", {}))
        possible_cards = contains_params(possible_cards, sheet.get("contains_params", {}))
        possible_cards = not_contains_params(possible_cards, sheet.get("not_contains_params", {}))
        chosen_cards = random.sample(possible_cards, sheet.get("count", 1))
        if (sheet.get("skip_if", {}).get("params") and
            filter_params(pack.values(), sheet.get("skip_if", {}).get("params"))) or\
            (sheet.get("skip_if", {}).get("not_params") and
            not_params(pack.values(), sheet.get("skip_if", {}).get("not_params"))) or\
            (sheet.get("skip_if", {}).get("contains_params") and
            contains_params(pack.values(), sheet.get("skip_if", {}).get("contains_params"))) or\
            (sheet.get("skip_if", {}).get("not_contains_params") and
            not_contains_params(pack.values(), sheet.get("skip_if", {}).get("not_contains_params"))):
            continue

        for card in chosen_cards:
            pack_position += 1
            if sheet.get("foil"):
                card["is_foil"] = True

            pack[pack_position] = card

    return pack

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# It might be better to use all cards and strip out non-english printings
# for war of the spark this is being done in the set file to remove Japanese
# planeswalkers as these only appear in Japanese packs
# https://magic.wizards.com/en/articles/archive/news/japanese-alternate-art-planeswalkers-2019-04-22
# https://scryfall.com/docs/api/bulk-data
# https://archive.scryfall.com/json/scryfall-default-cards.json
with open(os.path.join(__location__, "scryfall-default-cards.json")) as f:
    all_cards = list(json.load(f))
    all_cards = filter_params(all_cards, {"booster": True})

# Load in the default pack schema
with open(os.path.join(__location__, "default_pack.json")) as f:
    pack_template = json.load(f)

# Load set specific pack schema which overwrites the default
for filename in glob.glob(os.path.join(__location__, "sets", "*.json")):
    with open(filename) as f:
        pack_template[os.path.basename(filename).replace(".json", "")] = json.load(f)
