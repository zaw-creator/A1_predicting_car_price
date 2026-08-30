# A1: Predicting Car Price

A machine learning project that predicts the selling price of a used car, built for Chaky's company. Includes data cleaning and exploratory analysis, comparison of three regression models, and a deployed web app where users can get a price prediction from their car's details.

**Live demo:** https://chaky-car-price-predictor.onrender.com/

## Project Overview

Chaky's company struggles to price the used cars it takes in. This project builds a model that predicts a fair selling price from details like brand, year, mileage, engine size, and more — and wraps it in a simple web form so anyone can get an instant estimate.

## Repository Structure

```
.
├── notebook/
│   └── A1_car_price.ipynb      # data cleaning, EDA, model training & evaluation
├── data/
│   └── Cars.csv                 # raw dataset
├── app/
│   ├── Dockerfile
│   ├── docker-compose.yaml
│   └── code/
│       ├── app.py               # Dash app entry point
│       ├── model.pkl            # trained Random Forest model
│       ├── columns.pkl          # expected feature columns (for encoding user input)
│       ├── medians.pkl          # training-set medians (for imputing missing input)
│       ├── pages/
│       │   ├── home.py
│       │   └── predict.py
│       └── assets/
│           └── style.css
└── README.md
```

## Dataset

The dataset (`Cars.csv`) contains ~8,100 used car listings with features including brand/model name, year, selling price, kilometers driven, fuel type, seller type, transmission, ownership history, mileage, engine size, max power, torque, and seat count.

## Data Cleaning

- `owner` mapped to an ordinal scale (First Owner → 1, ..., Test Drive Car → 5)
- `fuel` filtered to Diesel/Petrol only (CNG/LPG removed — different mileage unit)
- `mileage`, `engine`, `max_power` stripped of their units and converted to numeric types
- `brand` extracted from the full car name (first word only)
- `torque` dropped
- Test Drive Car listings removed
- Remaining rows with missing values dropped (~2.7% of the data)
- `selling_price` log-transformed for training to reduce the effect of outliers/skew, with predictions converted back via `np.exp()` for evaluation and display

## Exploratory Findings

- **`max_power`** had the strongest correlation with price (0.75), followed by `year` (0.41) and `engine` (0.46)
- **`year` and `km_driven`** both showed non-linear relationships with price (rapid early depreciation, wedge-shaped mileage effect)
- **`transmission`** showed a clear price gap between Automatic and Manual cars; **`fuel`** type showed almost none
- **`brand`** strongly affects price (luxury brands like Lexus/BMW average several times more than volume brands like Maruti), but the feature is imbalanced — some brands have very few listings

## Model Comparison

Three models were trained and evaluated on the same 80/20 train/test split:

| Model | Test R² | Test RMSE | Train R² |
|---|---|---|---|
| Linear Regression | 0.86 | ₹307,196 | — |
| Decision Tree | 0.958 | ₹167,610 | 0.9996 (overfit) |
| **Random Forest** | **0.975** | **₹129,262** | 0.994 |

**Random Forest was selected as the final model** — best test performance and the smallest train/test gap, indicating it generalizes best. Full discussion in the notebook's closing summary.

## Running the Notebook

```bash
cd notebook
python3.13 -m venv venv
source venv/bin/activate
pip install pandas numpy scikit-learn matplotlib seaborn jupyter ipykernel
jupyter notebook
```

## Running the Web App Locally (without Docker)

```bash
cd app/code
pip install -r requirements.txt
python app.py
```
Visit `http://127.0.0.1:8050`.

## Running the Web App with Docker

```bash
cd app
docker compose up --build
```
Visit `http://localhost:8050`.

## How Prediction Handles Missing Fields

If a user leaves a numeric field blank, the app fills it in with that feature's median value from the training set (computed before the train/test split to avoid data leakage). Categorical fields left blank default to the baseline category dropped during one-hot encoding.