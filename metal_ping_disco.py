import os
import sys
import logging

import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"
)

AWS_S3_BUCKET = os.getenv("METAL_PING_DISCO_AWS_S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("METAL_PING_DISCO_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT = os.getenv("METAL_PING_DISCO_AWS_S3_ENDPOINT")

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])

metal_logo = "https://downloads.intercomcdn.com/i/o/255228/7796738b4070441bbb515486/a2f83ed0182096ecbb0056a328f55190.jpg"

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=metal_logo, height="30px")),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "Equinix Metal: Ping Disco", className="ms-2"
                            )
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://metal.equinix.com",
                style={"textDecoration": "none"},
            ),
        ]
    ),
)

app.layout = html.Div(
    html.Div(
        [
            navbar,
            dcc.Graph(id="metal_ping_disco", animate=True),
            dcc.Interval(id="interval-component", interval=10 * 1000, n_intervals=0),
            dcc.Markdown(
                """
            - Latencies to various endpoints from an Equinix Metal instance
        """
            ),
        ]
    )
)


@app.callback(
    Output("metal_ping_disco", "figure"), Input("interval-component", "n_intervals")
)
def update_graph_live(n):
    try:
        network_data = pd.read_csv(
            "s3://{}/metal_ping_disco_network_data.csv".format(AWS_S3_BUCKET),
            storage_options={
                "key": AWS_ACCESS_KEY_ID,
                "secret": AWS_SECRET_ACCESS_KEY,
                "client_kwargs": {
                    "endpoint_url": AWS_S3_ENDPOINT,
                },
            },
        )
    except:
        logging.exception("Fatal error interacting with s3, exiting")
        sys.exit(1)

    fig = px.line(
        network_data, x="time", y="latency", color="ip", symbol="ip", template="ggplot2"
    )

    return fig


if __name__ == "__main__":
    app.run_server(host="0.0.0.0")
