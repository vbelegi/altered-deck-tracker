import os.path
import ast
from altered_deckfmt import encode, EncodeException, decode
import json

decksjson = "./database/decks.json"
cardsjson = "./database/card_database/cards.json"

def deckSaveInDatabase(name: str, deck: str):
    encoded_deck = encode(deck)
    deck_to_save = f"{{'{name}':'{encoded_deck}'}}"
    deck_dict = ast.literal_eval(deck_to_save)

    if os.path.exists(decksjson):
        with open(decksjson, "r", encoding="utf-8") as json_file:
            decklist = json.load(json_file)
    else:
        decklist = {}

    decklist.update(deck_dict)

    with open(decksjson, "w", encoding="utf-8") as json_file:
        json.dump(decklist, json_file)

def getDeckNames() -> list:
    with open(decksjson, "r", encoding="utf-8") as json_file:
        deck_json = json.load(json_file)
    deck_names = list(deck_json.keys())
    return deck_names

def getDeckCodeByName(deck_name: str) -> str:
    with open(decksjson, "r", encoding="utf-8") as json_file:
        deck_json = json.load(json_file)
    deck_code = deck_json[deck_name]

    return deck_code

def deckListFormater(encoded_deck: str) -> dict:
    deck_list = {}

    decoded_deck = decode(encoded_deck)

    for line in decoded_deck.strip().split("\n"):
        quantity, card_name = line.split(maxsplit=1)
        deck_list[card_name] = int(quantity)

    return deck_list

def getCardNameById(card_id: str) -> str:
    with open(cardsjson, "r", encoding="utf-8") as json_file:
        card_list = json.load(json_file)
    if card_id in card_list:
        card_name = card_list[card_id]["name"]["en"]
        if card_list[card_id]["rarity"] == "RARE" :
            card_name = "(R) " + card_name
    else:
        card_name = "Card Not Found"

    return card_name


def drawChance(total_cards_deck: int, max_value: int) -> str:
    total_cards_deck = total_cards_deck - 1
    draw_chance = max_value / total_cards_deck
    draw_chance = draw_chance*100
    if draw_chance < 0: draw_chance = 0
    draw_chance = f"{draw_chance:.2f}%"
    return draw_chance

def checkHero(card_name: str) -> bool:
    hero_names_list = [
        "Waru & Mack","Gulrang & Tocsin","Sigismar & Wingspan", #Blue
        "Treyst & Rossum","Sierra & Oddball","Subhash & Marmo", #Brown
        "Nevenka & Blotch","Fen & Crowbar","Auraq & Kibble", #Pink
        "Teija & Nauraa","Arjun & Spike","Rin & Orchid", #Green
        "Lindiwe & Maw","Afanas & Senka","Akesha & Taru", #Purple
        "Basira & Kaizaimon","Kojo & Booda","Atsadi & Surge" #Red
    ]

    if card_name in hero_names_list:
        return True
    else:
        return False

# Script by Maverick CHARDET
# CC-BY

LANGUAGE_HEADERS = {
    "en": {
        "Accept-Language": "en-en"
    },
    "fr": {
        "Accept-Language": "fr-fr"
    },
    "es": {
        "Accept-Language": "es-es"
    },
    "it": {
        "Accept-Language": "it-it"
    },
    "de": {
        "Accept-Language": "de-de"
    }
}

# Imports
import requests
import os
#import json

def create_folder_if_not_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def download_file(url, filename, log=False, headers=None):
    if log: print(f"Downloading {filename} from {url}")
    response = requests.get(url, stream=True, headers=headers)
    if not response.ok:
        print(response)
        return False
    with open(filename, 'wb') as handle:
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    return True

def dump_json(data, filename):
    with open(filename, 'w', encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(filename):
    with open(filename, encoding="utf8") as f:
        return json.load(f)

def load_txt(filename):
    with open(filename, encoding="utf8") as f:
        return f.read()
