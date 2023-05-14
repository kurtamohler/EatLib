import requests
import json
import os
import urllib.parse

from .error_checking import check

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
def _search_raw(food_name, only_nonbranded=True):
    check(isinstance(food_name, str), TypeError,
        "Expected 'food_name' to be a str, but got {type(food_name)}")
    food_name_formatted = urllib.parse.quote(food_name)

    api_key = get_api_key()
    check(api_key is not None, RuntimeError,
        "API key was not set. Please set it with either 'set_api_key' or with "
        f"environment variable '{_API_KEY_ENV_VAR}'")

    check(isinstance(only_nonbranded, bool), TypeError,
        "Expected 'only_nonbranded' to be a bool, but got "
        f"{type(only_nonbranded)}")

    data_type = ''
    if only_nonbranded:
        # Nonbranded foods include "Foundation" foods and "SR Legacy"
        data_type = '&dataType=Foundation'
        data_type += '&dataType=' + urllib.parse.quote('SR Legacy')

    # The FoodData Central API is documented here:
    # https://fdc.nal.usda.gov/api-spec/fdc_api.html#/FDC/getFoodsSearch
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={food_name}{data_type}"

    response = requests.get(url)
    data = json.loads(response.text)

    foods = {}

    if not data["foods"]:
        return foods

    for food in data['foods']:
        name = food['description']

        # TODO: For now, just skip duplicates, but maybe I should come up
        # with a better idea
        if name in foods:
            continue

        nutrients = {}
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

        foods[name] = nutrients

    return foods
