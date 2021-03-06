# clean_water_tool

A reporting tool to support safe drinking water in California’s disadvantaged communities


## Getting started

We use python virtual environments to standardize the software versions and make reproducible science easier. Cookiecutter-datascience supports two popular virtual environment platforms: `conda` and `virtualenv`. This README outlines how to proceed using the `conda` [virtual environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html), part of the [Anaconda python distribution](https://www.anaconda.com/distribution/).

We also use `make` and to organize groups of commands, defined in `Makefile`.


The following steps will 1) create and activate a virtual environment, 2) install the project requirements, 3) download the HR2W data.

```
make create_environment
conda activate clean_water_tool

make requirements  # install python modules in requirements.txt
make data  # download source tables and store to data/raw and data/interim
```

Next you might want to launch a jupyter notebook and start exploring the data.

```
jupyter lab
```


When you're all done, you can deactivate the virtual environment.

```
conda deactivate
```


## Contributing

Want to contribute to our project? Great! Start by making an issue describing in detail the problem you'd like to address or feature you'd like to see added. Assign anyone whose input you would like.

Make sure to pull the most recent version of `master`

```
git checkout master
git pull origin master


git branch a-descriptive-branch-name
git checkout a-descriptive-branch-name
```

Make changes to the code that address the issue.


```
git add src/main.py
git commit -m "Some nice commit message"

git push origin a-descriptive-branch-name
```

Create a pull request (PR) on github (https://github.com/r-b-g-b/clean-water-tool/pull/new/a-descriptive-branch-name).

Describe in as much detail as possible what you did, unforseen obstacles, and anything else you think would be important to know for someone to evaluate your code. In the PR message, link to any new issues you created by typing #< issue number >. You can also say "Closes #< issue number >".

Request any reviewers. When everyone is satisfied with the code, "Squash and merge."

Checkout master and pull the new changes.

```
git checkout master
git pull origin master
```

Repeat as needed!


## Project Organization

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
