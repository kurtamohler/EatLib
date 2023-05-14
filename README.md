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

Then install Nutrinaut.

```bash
pip install .
```

## Get a FoodData Central API key

Sign up for an API key [here](https://fdc.nal.usda.gov/api-key-signup.html).

The key will be sent to your email address. You can give this key to Nutrinaut in
two different ways:

  1. Set an environment variable before running a Nutrinaut application:

     ```bash
     export NUTRINAUT_API_KEY='<your FoodData Central API key>'
     ```

  2. Call `nutrinaut.set_api_key` in your application:

     ```bash
     nutrinaut.set_api_key('<your FoodData Central API key>')
     ```
