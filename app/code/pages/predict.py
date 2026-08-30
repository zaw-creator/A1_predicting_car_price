import dash
from dash import html, dcc, Input, Output, State
import joblib
import pandas as pd
import numpy as np

dash.register_page(__name__, path='/predict')

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = joblib.load(os.path.join(BASE_DIR, 'model.pkl'))
columns = joblib.load(os.path.join(BASE_DIR, 'columns.pkl'))
medians = joblib.load(os.path.join(BASE_DIR, 'medians.pkl'))

layout = html.Div([
    html.H1("Car Price Predictor"),
    html.P("Enter your car's details below to get a predicted selling price. Leave a field blank if you don't know it."),

    html.Label("Year"),
    dcc.Input(id='input-year', type='number', placeholder='e.g. 2015'),

    html.Label("Km Driven"),
    dcc.Input(id='input-km_driven', type='number', placeholder='e.g. 50000'),

    html.Label("Owner"),
    dcc.Dropdown(
        id='input-owner',
        options=[
            {'label': 'First Owner', 'value': 1},
            {'label': 'Second Owner', 'value': 2},
            {'label': 'Third Owner', 'value': 3},
            {'label': 'Fourth & Above Owner', 'value': 4},
        ],
        placeholder='Select owner history'
    ),

    html.Label("Mileage (kmpl)"),
    dcc.Input(id='input-mileage', type='number', placeholder='e.g. 20.5'),

    html.Label("Engine (CC)"),
    dcc.Input(id='input-engine', type='number', placeholder='e.g. 1200'),

    html.Label("Max Power (bhp)"),
    dcc.Input(id='input-max_power', type='number', placeholder='e.g. 90'),

    html.Label("Seats"),
    dcc.Input(id='input-seats', type='number', placeholder='e.g. 5'),

    html.Label("Fuel"),
    dcc.Dropdown(
        id='input-fuel',
        options=[
            {'label': 'Diesel', 'value': 'Diesel'},
            {'label': 'Petrol', 'value': 'Petrol'},
        ],
        placeholder='Select fuel type'
    ),

    html.Label("Seller Type"),
    dcc.Dropdown(
        id='input-seller_type',
        options=[
            {'label': 'Individual', 'value': 'Individual'},
            {'label': 'Dealer', 'value': 'Dealer'},
            {'label': 'Trustmark Dealer', 'value': 'Trustmark Dealer'},
        ],
        placeholder='Select seller type'
    ),

    html.Label("Transmission"),
    dcc.Dropdown(
        id='input-transmission',
        options=[
            {'label': 'Manual', 'value': 'Manual'},
            {'label': 'Automatic', 'value': 'Automatic'},
        ],
        placeholder='Select transmission'
    ),

    html.Label("Brand"),
    dcc.Dropdown(
        id='input-brand',
        options=[
            {'label': c.replace('brand_', ''), 'value': c.replace('brand_', '')}
            for c in columns if c.startswith('brand_')
        ],
        placeholder='Select brand'
    ),

    html.Br(),
    html.Button('Predict Price', id='predict-button', n_clicks=0),

    html.Br(), html.Br(),
    html.Div(id='prediction-output'),
], className="page-container")


@dash.callback(
    Output('prediction-output', 'children'),
    Input('predict-button', 'n_clicks'),
    State('input-year', 'value'),
    State('input-km_driven', 'value'),
    State('input-owner', 'value'),
    State('input-mileage', 'value'),
    State('input-engine', 'value'),
    State('input-max_power', 'value'),
    State('input-seats', 'value'),
    State('input-fuel', 'value'),
    State('input-seller_type', 'value'),
    State('input-transmission', 'value'),
    State('input-brand', 'value'),
)
def predict_price(n_clicks, year, km_driven, owner, mileage, engine,
                   max_power, seats, fuel, seller_type, transmission, brand):

    if n_clicks == 0:
        return ""  # don't predict until the button has actually been clicked

    # Start with a row of all zeros, matching the model's expected columns
    row = pd.Series(0, index=columns, dtype=float)

    # Numeric fields: use the user's value if given, otherwise fall back to
    # the training-set median we saved earlier (this is the "graceful
    # handling of missing fields" the assignment asked for)
    row['year'] = year if year is not None else medians['year']
    row['km_driven'] = km_driven if km_driven is not None else medians['km_driven']
    row['owner'] = owner if owner is not None else medians['owner']
    row['mileage'] = mileage if mileage is not None else medians['mileage']
    row['engine'] = engine if engine is not None else medians['engine']
    row['max_power'] = max_power if max_power is not None else medians['max_power']
    row['seats'] = seats if seats is not None else medians['seats']

    # Categorical fields: set the matching one-hot column to 1, if it exists.
    # (If the user picked the category that was dropped during training via
    # drop_first=True, no column needs to be set — leaving everything 0 is
    # exactly what represents that dropped category.)
    for value, prefix in [
        (fuel, 'fuel_'),
        (seller_type, 'seller_type_'),
        (transmission, 'transmission_'),
        (brand, 'brand_'),
    ]:
        if value is not None:
            col_name = f"{prefix}{value}"
            if col_name in row.index:
                row[col_name] = 1

    # Reshape into a single-row DataFrame (model expects a 2D input)
    X_new = pd.DataFrame([row])[columns]  # [columns] enforces correct column order

    pred_log_price = model.predict(X_new)[0]
    pred_price = np.exp(pred_log_price)

    return f"Predicted Selling Price: ₹{pred_price:,.0f}"