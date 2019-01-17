# MarchMadness2019

March madness bracket model.


## Setup

### Prerequisites
To work with this repo, you must have [Conda](https://conda.io/docs/user-guide/install/download.html) installed. Conda is a command line tool to manage dependencies within a virtual environment.

### Steps
1) In the desired parent directory of your project, run:
```
git clone https://github.com/tklutey/MarchMadness2019.git
```

2) From the project root directory, run:
```
conda env create -f environment.yml
```
This creates a conda environment with all of the necessary dependencies to run this package.

3) Run ```source activate [environment_name]``` on OSX or simply ```activate [environment_name]``` on Windows to activate the conda virtual environment.

**Note: see https://conda.io/docs/user-guide/tasks/manage-environments.html for more information on managing Conda environments**

### Executing/Developing
* I use Spyder as my IDE of choice since it is lightweight and has a console that easily display visuals like matlabplot. You can run Spyder once you've activated this environment by executing ```spyder``` from the CLI.
* To run the whole workflow start to end, execute ```main.py```.



## Project Organization

<p>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template.</a> I have not followed the below structure exactly, but as directories and files are added, they should roughly follow the below structure.</p>

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

