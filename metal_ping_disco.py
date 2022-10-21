import os
import sys
import logging

import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z"
)

AWS_S3_BUCKET = os.getenv("METAL_PING_DISCO_AWS_S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("METAL_PING_DISCO_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT = os.getenv("METAL_PING_DISCO_AWS_S3_ENDPOINT")

app = dash.Dash(__name__)

app.layout = html.Div(
    html.Div([
        html.H1('Equinix Metal Ping Disco'),
        dcc.Graph(id='metal_ping_disco', animate=True),
        dcc.Interval(id='interval-component',  interval=10*1000, n_intervals=0)
    ])
)

@app.callback(Output('metal_ping_disco', 'figure'), Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    try:
        network_data = pd.read_csv(
            "s3://{}/metal_ping_disco_network_data.csv".format(AWS_S3_BUCKET),
            storage_options = {
                "key": AWS_ACCESS_KEY_ID,
                "secret": AWS_SECRET_ACCESS_KEY,
                "client_kwargs": {
                    "endpoint_url": AWS_S3_ENDPOINT,
                },
            },
        )
    except:
        logging.exception('Fatal error interacting with s3, exiting')
        sys.exit(1)

    fig = px.line(network_data, x='time',y='latency', color='ip', symbol='ip')

    return fig

if __name__ == "__main__":
    app.run_server(host='0.0.0.0')
