# Nutrinaut
Food nutrition library with array operations

Nutrinaut makes diet tracking easy. It provides a simple interface to search for
foods in USDA's [FoodData Central](https://fdc.nal.usda.gov/) database.

Nutrition results are like numerical arrays, so they can be operated upon with
array arithmetic. This makes it easy to calculate how much of each nutrient
you've eaten, given a list of foods and the amounts of each, by weight.

## Install

Install Miniconda: [instructions](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

Run the following to create and activate an environment with all dependencies.

```bash
conda env create -f environment.yaml -n nutrinaut && conda activate nutrinaut
```

Install Nutrinaut.

```bash
pip install .
```

Install the Nutrinaut database.

```bash
python -c 'import nutrinaut; nutrinaut.install_database()'
```

## Basic usage

### Search for foods

You can search for foods by name, like so:

```python
>>> nutrinaut.search('peas', limit=10)
[('Cowpeas, leafy tips, raw', 90),
 ('Babyfood, peas and brown rice', 90),
 ('Peas, edible-podded, raw', 90),
 ('Pigeonpeas, immature seeds, raw', 90),
 ('Peas, green, raw', 90),
 ('Babyfood, peas, dices, toddler', 90),
 ('SMART SOUP, Moroccan Chick Pea', 77),
 ('Ice creams, vanilla, light', 68),
 ('Ice creams, vanilla, rich', 68),
 ('Ice creams, vanilla', 68)]
```

The results are sorted by a search relevance score.

### Get food nutrition

You can obtain the nutrition of a food with it's exact name from the search
results, like so:

```python
>>> nutrinaut.get('Peas, green, raw')
Nutrients(fat=0.004, carbs=0.14400000000000002, protein=0.0542, calories=0.8288000000000001)
```

The nutrient results from `nutrinaut.get` give the nutrients for 1 gram of the
food. So if you want to know the nutrients in 150 grams of peas, for instance,
you can just multiply the result by 150:

```python
>>> 150 * nutrinaut.get('Peas, green, raw')
Nutrients(fat=0.6, carbs=21.6, protein=8.129999999999999, calories=124.32000000000001)
```
