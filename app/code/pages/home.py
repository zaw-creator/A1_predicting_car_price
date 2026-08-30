import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1("Chaky Car Price Predictor"),

    html.P(
        "Wondering how much your car is worth? This tool uses a machine "
        "learning model trained on thousands of real used car listings to "
        "estimate a fair selling price based on details like the car's "
        "brand, year, mileage, engine size, and more."
    ),

    html.P(
        "Just head to the Predict page, fill in as much information as you "
        "know about the car, and get an instant price estimate. Don't "
        "worry if you're missing a detail or two — the tool can fill in "
        "reasonable estimates for anything you leave blank."
    ),

    dcc.Link(
        html.Button("Get a Price Prediction", className="predict-button"),
        href="/predict"
    ),
], className="page-container")