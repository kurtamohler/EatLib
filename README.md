# EatLib
Food nutrition library with array operations

EatLib makes diet tracking easy. It provides a simple interface to search for
foods in USDA's [FoodData Central](https://fdc.nal.usda.gov/) database.

Nutrition results are like numerical arrays, so they can be operated upon with
array arithmetic. This makes it easy to calculate how much of each nutrient
you've eaten, given a list of foods and the amounts of each, by weight.

## Install

Install Miniconda: [instructions](https://docs.conda.io/projects/conda/en/latest/user-guid    e/install/index.html)

Run the following to create and activate an environment with all dependencies.

```bash
conda env create -f environment.yaml -n eatlib && conda activate eatlib
```

Then install EatLib.

```bash
python setup.py install
```
