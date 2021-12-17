# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 20:48:35 2021

@author: Kyle Browne
"""

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

IPA = pd.read_csv("IPA.csv", index_col=0)

IPA.columns = IPA.columns.str.replace(' ', '_')
IPAC = IPA.columns.unique()
def generate_table(df, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns 
            ]) for i in range(min(len(df), max_rows))
        ])
    ])

app = dash.Dash(__name__, external_stylesheets=stylesheet)

IPATypes = IPA.Type.unique()

app.layout = html.Div([
    html.H1('Top 250 IPAs',
            style={'textAlign' : 'center'}),
    html.Br(),
    html.Br(), html.Div([dcc.Graph(id='the_graph')], title = 'Brewing Company' , style={'width' : '66%', 'float': 'right'}),
    dcc.Textarea(
        id='textarea',
        value='This dashboard allows the user to set a handful of parameters to determine what IPA suits their needs best. The user will input what type of IPA they want, the maximum alcohol percentage and the minimum average rating. All of this information was taken from www.beeradvocate.com and you can click on the link below to go directly to their website.',
        style={'width': '33%', 'height': 140},
    ),
    html.Div(id='textarea-output', style={'whiteSpace': 'pre-line'}),
    

    html.A('Click here to go to the Top Rated IPA List',
           href='https://www.beeradvocate.com/beer/top-rated/',
           target='_blank'),
    html.Br(),
    html.Br(),
    html.Div([dcc.Dropdown(options=[{
        'label' : i, 'value' : i } for i in IPATypes], placeholder= 'Choose IPA Type', id='type')
        ],style={'width' : '33%', 'float' : 'left'}),  
    
    html.Br(),
    html.Br(),
    html.Div(["Enter Maximum Alcohol %:", dcc.Input(placeholder='Enter maximum alcohol %',
                                   id='alcpercent', type='number', value=100)
              ],style={'width' : '20%', 'display': 'inline-block'}),
    html.Br(),
    html.Div(["Enter Minimum Avg Rating:", dcc.Input(placeholder='Enter minimum avg rating',
                                   id='minrating', type='number', value=0)
              ],style={'width' : '20%', 'display': 'inline-block'}),
    
    
    
    
    html.Div(id="IPA_div")
                
    ])

 
    
server = app.server
    
    
@app.callback(
    Output(component_id="IPA_div", component_property="children"),
    [Input(component_id="type", component_property="value"),
     Input(component_id="alcpercent", component_property="value"),
     Input(component_id="minrating", component_property="value")]
)
def update_table(IPAs, alcpercent, minrating):
    x = IPA[IPA.Type==IPAs].sort_values('Avg_Rating', ascending = False) 
    alc = IPA[IPA.Alcohol_Percent<=float(alcpercent)]
    minr = IPA[IPA.Avg_Rating>=float(minrating)]
    y = pd.merge(x, alc, how="inner")
    z = pd.merge(y, minr, how="inner")

    return generate_table(z)

@app.callback(
    Output(component_id="the_graph", component_property="figure"),
    [Input(component_id="type", component_property="value"),
     Input(component_id="alcpercent", component_property="value"),
     Input(component_id="minrating", component_property="value")]
)
def update_graph(IPAs, alcpercent, minrating):
    x = IPA[IPA.Type==IPAs].sort_values('Avg_Rating', ascending = False) 
    alc = IPA[IPA.Alcohol_Percent<=float(alcpercent)]
    minr = IPA[IPA.Avg_Rating>=float(minrating)]
    y = pd.merge(x, alc, how="inner")
    z = pd.merge(y, minr, how="inner")
    chart = z
    piechart=px.pie(
        data_frame=chart,
        names='Brewing_Company',
        hole=.3, title=('Brewing Company'))
    
    return (piechart)

if __name__ == '__main__':
    app.run_server(debug=True)

