import requests
import json
import os
import urllib.parse
import zipfile
import io

from .error_checking import (check, check_type)
from .nutrients import Nutrients

_data_dir = os.path.expanduser('~/.nutrinaut')
_data_path = os.path.join(_data_dir, 'nutrinaut_database.json')
_database = None

def _load_database_raw(url):
    req_result = requests.get(url)
    check(req_result.ok, RuntimeError,
        f"failed to get zipfile from URL: {url}")

    zip_result = zipfile.ZipFile(io.BytesIO(req_result.content))
    infolist = zip_result.infolist()

    check(len(infolist) == 1, RuntimeError,
        "expected zipfile from URL to have exactly one entry, but got "
        f"{len(infolist)}: {url}")

    with zip_result.open(infolist[0].filename) as json_file:
        data = json.loads(json_file.read())

    #with open(os.path.expanduser('~/tmp/nutrinaut_database_sr_raw.json'), 'w', encoding='utf-8') as f:
    #    json.dump(data, f)

    return data

def _extract_nutrient(nutrient_raw, expected_unit):
    nutrient_name = nutrient_raw['nutrient']['name']
    unit = nutrient_raw['nutrient']['unitName']
    check(unit == expected_unit, RuntimeError,
        f"expected nutrient '{nutrient_name}' to be in units "
        f"'{expected_unit}', but got '{unit}'")

    return float(nutrient_raw['amount'])

def _extract_grams(nutrient_raw):
    return _extract_nutrient(nutrient_raw, 'g')

def _extract_add_contributors(nutrients_raw, contributors):
    amount = None

    for nutrient_raw in nutrients_raw:
        nutrient_name_raw = nutrient_raw['nutrient']['name']

        if nutrient_name_raw in contributors:
            if amount is None:
                amount = 0
            amount += _extract_grams(nutrient_raw)

    return amount

def _nutrients_from_raw(food_raw):
    # NOTE: This shows how to calculate calories from macros for this
    # particular food
    #print(food_raw['nutrientConversionFactors'])

    nutrients_raw = food_raw['foodNutrients']

    nutrient_contributors_map = {
        'fat': [
            'Total lipid (fat)',
        ],
        'protein': [
            'Protein',
        ],
        'carbs by diff': [
            'Carbohydrate, by difference',
        ],
        #'carbs by sum': [
        #    'Carbohydrate, by summation',
        #],
        #'starch': [
        #    'Starch',
        #],
        #'fiber': [
        #    'Fiber, total dietary',
        #],
        'sugars': [
            'Sugars, Total',
        ],
    }

    nutrients_extracted = {}

    for nutrient_name, contributors in nutrient_contributors_map.items():
        nutrients_extracted[nutrient_name] = _extract_add_contributors(nutrients_raw, contributors)

    if nutrients_extracted['carbs by diff'] is None:
        check(False, RuntimeError, 'Need to decide what to do here')

    nutrients_dict = {
        'fat': (nutrients_extracted['fat'] or 0),
        'carbs': nutrients_extracted['carbs by diff'],
        'protein': (nutrients_extracted['protein'] or 0),
    }

    # Divide by 100g, since that is the amount stored in FoodData Central
    for key, value in nutrients_dict.items():
        nutrients_dict[key] = value / 100

    return nutrients_dict

def _convert_from_raw(data_raw):
    foods = list(data_raw.values())[0]

    food_data = {}

    for food in foods:
        name = food['description']
        nutrients = _nutrients_from_raw(food)

        check(name not in food_data, RuntimeError,
            f"multiple entries for food '{name}' found in database")
        food_data[name] = nutrients

    return food_data

def install_database(overwrite=False):
    if not overwrite:
        check(not os.path.exists(_data_path), RuntimeError,
            f"Database already installed to location '{_data_path}'. "
            "To overwrite it, set argument 'overwrite=True'")

    foundation_foods_url = 'https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_json_2023-04-20.zip'
    sr_legacy_url = 'https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_sr_legacy_food_json_2018-04.zip'

    #data_raw = _load_database_raw(foundation_foods_url)

    data_raw = _load_database_raw(sr_legacy_url)

    # Foundation Foods
    #file_raw = '~/tmp/nutrinaut_database_raw.json'

    # SR Legacy
    #file_raw = '~/tmp/nutrinaut_database_sr_raw.json'

    #with open(os.path.expanduser(file_raw)) as json_file:
    #    data_raw = json.loads(json_file.read())

    data = _convert_from_raw(data_raw)

    if not os.path.exists(_data_dir):
        os.makedirs(_data_dir)

    with open(_data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

def _maybe_load_database():
    global _database

    if _database is None:
        check(os.path.exists(_data_path), RuntimeError,
            "Cannot load database because it has not been installed "
            "please run 'nutrinaut.install_database()'")

        with open(_data_path) as json_file:
            _database = json.loads(json_file.read())

def search(food_name, page_size=10, page_num=0, only_nonbranded=True):
    _maybe_load_database()
    foods = []
    return foods

def get(food_name, only_nonbranded=True):
    res = search(food_name, page_size=1, page_num=0, only_nonbranded=only_nonbranded)
    check(len(res) != 0 and res[0][0] == food_name, ValueError,
        f"no food with exact name '{food_name}' was found")
    return res[0][1]
