from dash import Dash, html, dcc
import dash
import os
app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.Div([
        dcc.Link("Home", href="/", className="nav-link"),
        dcc.Link("Predict Price", href="/predict", className="nav-link"),
    ], className="navbar"),

    dash.page_container
])

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(debug=False, host='0.0.0.0', port=port)