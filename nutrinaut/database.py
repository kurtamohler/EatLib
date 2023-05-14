import requests
import json
import os
import urllib.parse

from .error_checking import (check, check_type)
from .nutrients import Nutrients

_API_KEY_ENV_VAR = 'NUTRINAUT_API_KEY'
_API_KEY = None

def _init_api_key():
    if _API_KEY_ENV_VAR in os.environ:
        global _API_KEY
        _API_KEY = os.environ[_API_KEY_ENV_VAR]

def set_api_key(api_key):
    check(isinstance(api_key, str), TypeError,
        f"expected 'api_key' of type str, but got {type(api_key)}")
    global _API_KEY
    _API_KEY = api_key

def get_api_key():
    return _API_KEY

# TODO: Add paging args with low default value for better perf
def _search_raw(food_name, page_size=10, page_num=0, only_nonbranded=True):

    check_type(food_name, str, 'food_name')
    check_type(page_size, int, 'page_size')
    check_type(page_num, int, 'page_num')
    check_type(only_nonbranded, bool, 'only_nonbranded')

    check(page_size > 0, ValueError,
        f"expected 'page_size' > 0, but got {page_size}")

    check(page_size >= 0, ValueError,
        f"expected 'page_size' >= 0, but got {page_size}")

    food_name_formatted = urllib.parse.quote(food_name)

    api_key = get_api_key()
    check(api_key is not None, RuntimeError,
        "API key was not set. Please set it with either 'set_api_key' or with "
        f"environment variable '{_API_KEY_ENV_VAR}'")

    data_type = ''
    if only_nonbranded:
        # Nonbranded foods include "Foundation" foods and "SR Legacy"
        data_type = '&dataType=Foundation'
        data_type += '&dataType=' + urllib.parse.quote('SR Legacy')

    page_size_arg = f'&pageSize={page_size}'
    page_num_arg = f'&pageNumber={page_num}'

    # The FoodData Central API is documented here:
    # https://fdc.nal.usda.gov/api-spec/fdc_api.html#/FDC/getFoodsSearch
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={food_name}{data_type}{page_size_arg}{page_num_arg}"

    response = requests.get(url)
    data = json.loads(response.text)

    foods = []

    if not data["foods"]:
        return foods

    for food in data['foods']:
        name = food['description']

        nutrients = {}
        # TODO: Double check that nutrients are per 100g
        for nutrient in food["foodNutrients"]:
            nutrient_name = nutrient["nutrientName"]
            nutrient_value = nutrient['value']
            nutrient_unit = nutrient["unitName"]
            nutrient_id = nutrient['nutrientId']

            nutrients[nutrient_name] = {
                "value": nutrient_value,
                "unit": nutrient_unit,
                'id': nutrient_id
            }

        foods.append((name, nutrients))

    return foods

def search(food_name, page_size=10, page_num=0, only_nonbranded=True):
    foods_raw = _search_raw(food_name, page_size, page_num, only_nonbranded)

    foods = []

    # Convert nutrient dicts to `Nutrients` obj
    for food_name, nutrients_raw in foods_raw:

        # TODO: Create a function that converts the raw dict into a Nutrients obj
        # and does some error checking, like to make sure the units are
        # expected or convert them
        protein = nutrients_raw['Protein']['value']
        carbs = nutrients_raw['Carbohydrate, by difference']['value']
        fat = nutrients_raw['Total lipid (fat)']['value']
        nutrients = Nutrients(
            protein=protein,
            carbs=carbs,
            fat=fat) / 100
        foods.append((food_name, nutrients))

    return foods

def get(food_name, only_nonbranded=True):
    res = search(food_name, page_size=1, page_num=0, only_nonbranded=only_nonbranded)
    check(len(res) != 0 and res[0][0] == food_name, ValueError,
        f"no food with exact name '{food_name}' was found")
    return res[0][1]
