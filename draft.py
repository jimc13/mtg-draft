#!/usr/bin/env python3
import json
import random

# https://scryfall.com/docs/api/bulk-data
# https://archive.scryfall.com/json/scryfall-default-cards.json
with open("scryfall-default-cards.json") as f:
    all_cards = list(json.load(f))

with open("default_pack.json") as f:
    pack_template = json.load(f)

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
    foil_cards = []
    cards = []
    for sheet in pack_template["pack_contents"].values():
        possible_cards = cards_in_set[::]
        # Select one of the parameter sets based on weight
        sheet = random.choices(sheet, weights=[x.get("weight", 1) for x in sheet])[0]
        possible_cards = filter_params(possible_cards, sheet.get("params", {}))
        possible_cards = not_params(possible_cards, sheet.get("not_params", {}))
        possible_cards = contains_params(possible_cards, sheet.get("contains_params", {}))
        possible_cards = not_contains_params(possible_cards, sheet.get("not_contains_params", {}))
        chosen_cards = random.sample(possible_cards, sheet.get("count", 1))
        if sheet.get("foil"):
            foil_cards += chosen_cards
        else:
            cards += chosen_cards

    return foil_cards, cards
