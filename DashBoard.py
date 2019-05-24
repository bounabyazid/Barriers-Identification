#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:45:53 2019

@author: polo
"""

import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

Tariff = {
		"Direction" : 0,
		"Purpose" : 0,
		"Time length" : 0,
		"Import restraints" : 0,
		"Rates" : 0,
		"Distribution points" : 0
	}
NonTariff = {
		"Government participation in trade" : 0,
		"Customs and entry procedures" : 0,
		"Product requirements" : 0,
		"Quotas" : 0,
		"Financial control" : 0
	}


df = pd.read_csv('/home/polo/.config/spyder-py3/Barriers Identification/Barriers DashBoard/Journals-DataSet/ACM.csv')


#app = dash.Dash('offline example')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
   html.Div([
        html.Div([
            dcc.Dropdown(id='TextSources',
                options=[{'label': i, 'value': i} for i in ['Link', 'Text', 'Forums']],
                value='Text'
            ),
            dcc.RadioItems(id='Barrier-Categories',
                options=[{'label': i, 'value': i} for i in ['Tariff', 'NonTariff', 'All']],
                value='Tariff',
                labelStyle={'display': 'inline-block'})
        ],style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(id='Journals-DataSet',
                options=[{'label': i, 'value': i} for i in ['ACM', 'IEEE', 'ScienceDirect', 'Business journals','Yazid']],
                value='ACM')
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
    
    ], style={'borderBottom': 'thin lightgrey solid','backgroundColor': 'rgb(250, 250, 250)','padding': '10px 5px' }),

#______________________________________________________________________________
      html.Div([
        html.Div([
            dcc.Textarea(id='TextArea',
                placeholder='Enter a value...',
                value='This is a TextArea component',
                style={'width':'100%','height': 300, 'padding': '0 20'}
            
        )], className="six columns"),
        
        html.Div([
            dcc.Upload(['Drag and Drop or ',html.A('Select a File')]
                , style={'height': 300,'lineHeight': '60px','borderWidth': '1px',
                         'borderStyle': 'dashed','borderRadius': '5px','textAlign': 'center'
                })
        ], className="six columns"),
    ], className="row"),
      
#______________________________________________________________________________
    html.Div([
        html.Div([
            dcc.Graph(id='proportion-text-graph',
            figure={
            'data': [
                {'x': list(Tariff.keys()), 'y': [4, 1, 2, 6, 9], 'type': 'bar', 'name': 'SF'},
                {'x': list(Tariff.keys()), 'y': [2, 4, 5, 3, 1.5], 'type': 'bar', 'name': u'Montréal'},
            ]},
        ),
            dcc.Slider(id='year-slider', min=2000, max=2019, value=2019,
            marks={str(year): str(year) for year in range(2000,2019,2)})
        ], className="six columns"),
        
        html.Div([
            dcc.Graph(id='proportion-journal-graph'),
            dcc.Slider(id='year-slider2', min=2000, max=2019, value=2019,
            marks={str(year): str(year) for year in range(2000,2019,2)})
        ], className="six columns"),
    ], className="row"), 
    html.Div(id='slider-output-container')

])

@app.callback([Output('proportion-text-graph', 'figure'),
               Output('proportion-journal-graph', 'figure')],
              [Input('Journals-DataSet', 'value'),
               Input('year-slider2', 'value')])

def update_figure(Journal,Year):
    df = pd.read_csv('/home/polo/.config/spyder-py3/Barriers Identification/Barriers DashBoard/Journals-DataSet/'+Journal+'.csv')

    filtered_df = df[df.Year == Year]
    for key in Tariff.keys():
        Tariff[key] = (filtered_df[key].values).sum()
   
    for key in NonTariff.keys():
        NonTariff[key] = (filtered_df[key].values).sum()
        
    trace1 = go.Bar(
    x=list(Tariff.keys()),
    y=list(Tariff.values()),
    marker=dict(
        color=['rgba(255,0,0,10)', 
               'rgba(0,255,0,0.3)',
               'rgba(0,0,255,0.3)',
               'rgba(255,255,0,0.3)',
               'rgba(255,0,255,0.3)',
               'rgba(204,204,204,1)']))
    
    trace2 = go.Bar(
    x=list(NonTariff.keys()),
    y=list(NonTariff.values()),
    name='NonTariff',
    marker=dict(
        color=['rgba(204,204,204,1)', 
               'rgba(222,45,38,0.8)',
               'rgba(222,45,70,0.8)',
               'rgba(222,50,100,0.8)',
               'rgba(222,45,0,10)']))

    layout1 = go.Layout(title='Tariff Barriers')
    layout2 = go.Layout(title='NonTariff Barriers')

    return go.Figure(data=[trace1], layout=layout1),go.Figure(data=[trace2], layout=layout2)
    #data = [trace1, trace2]
    #layout = go.Layout(barmode='group')
    return trace1,trace2
    #return go.Figure(data=data, layout=layout)
    

if __name__ == '__main__':
    app.run_server(debug=True)