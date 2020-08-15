# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

import InfoTrayectosModule as Tracks
from DecoderModule import Decoder
import InfoStationsModule as Stations
from datetime import datetime as dt


import plotly.express as px
import plotly.graph_objects as go
mapbox_access_token = 'pk.eyJ1IjoiamJlbml0b2wiLCJhIjoiY2tkZW92bnNyMDBmeTJ5cXBmcXNxanFxOCJ9.PDhf4kysLJ7TFJZAEjT8wA'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


filePath = "../DataFrames/Stations/"
data = Stations.concatenateAll(filePath)

Decode = Decoder('../DataFrames/DatosEstaticos.txt')
# df = Decode._obj

StartDate = '2020-5-06 00:48'
EndDate = '2020-5-13 00:50'
Value = 'DockBikes'
Comparator = 'dow'
Accuracy = "d"


df = Stations.ChooseInterval(data, StartDate, EndDate, Value)
df = Stations.ChooseAccuracy(df, Accuracy)


# fig = go.Figure(go.Scattermapbox(
#     lat=df.Latitude,
#     lon=df.Longitude,
#     mode='markers',
#     marker=go.scattermapbox.Marker(
#         size=8, showscale=True
#     ),
#     text=df.Address,


# ))

# fig.update_layout(


#     autosize=True,
#     hovermode='closest',
#     width=750,
#     height=500,
#     margin=dict(
#         l=50,
#         r=0,
#         b=50,
#         t=50

#     ),
#     mapbox=dict(
#         accesstoken=mapbox_access_token,
#         bearing=0,
#         center=dict(
#             lat=float(df.Latitude.iloc[0]),
#             lon=float(df.Longitude.iloc[0])
#         ),
#         pitch=0,
#         zoom=10
#     ),
# )


app.layout = html.Div(children=[
    html.H1(children='JBicisPro'),
    html.H2(children='Chequea las bicis disponibles!'),
    html.Label('Agrupa las estaciones en:'),
    dcc.Dropdown(
        id="clusters",
        options=[
            {'label': 'Estaciones', 'value': 'id'},
            {'label': 'Distritos', 'value': 'DistritoName'},
            {'label': 'Barrios', 'value': 'BarrioName'},
            {'label': 'Puntos cardinales', 'value': 'RegionName'}
        ],
        value='id'
    ),


    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=dt(2019, 5, 3),
        end_date=dt(2019, 5, 5)
    ),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='graph-with-slider'

    ),
    dcc.Slider(
        id='year-slider',
        min=0,
        max=len(df),
        value=0,
        marks={str(year): str(year) for year in range(0, len(df))},
        step=None
    ),
])


@app.callback(
    [Output('year-slider', 'max'),
     Output('year-slider', 'marks')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')])
def slidermax(start_date, end_date):
    df = Stations.ChooseInterval(data, start_date, end_date, Value)

    df = Stations.ChooseAccuracy(df, Accuracy)
    return len(df), {str(year): str(year) for year in range(0, len(df))}


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value'),
     Input('clusters', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')])
def update_figure(selected_year, ClusterName, start_date, end_date):

    df = Stations.ChooseInterval(data, start_date, end_date, Value)

    df = Stations.ChooseAccuracy(df, Accuracy)
    print(len(df))

    toPlot = Stations.Ploteo(df.iloc[selected_year], Decode)
    if ClusterName != 'id':
        toPlot.getClusterMeans(df.iloc[selected_year], Decode, ClusterName)
    fig = go.Figure(go.Scattermapbox(
        lat=toPlot.Latitude,
        lon=toPlot.Longitude,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=toPlot.Value, color=toPlot.Value, showscale=True, colorscale=px.colors.sequential.Reds
        ),
        text=toPlot.Address,


    ))

    fig.update_layout(
        title=dict(
            text=str(toPlot.Date),
            x=0.5,
        ),

        autosize=True,
        hovermode='closest',
        width=750,
        height=500,
        margin=dict(
            l=50,
            r=0,
            b=50,
            t=50

        ),
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=sum(toPlot.Latitude)/len(toPlot.Latitude),
                lon=sum(toPlot.Longitude)/len(toPlot.Longitude)
            ),
            pitch=0,
            zoom=11.45
        ),
    )
    # fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
