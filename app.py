# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 18:20:28 2020

@author: david
"""

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_daq as daq
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

buildings = [7,4,8,2,9,4]
prev_building = []
sunset = []

for building in buildings:
    
    if not prev_building or building > max(prev_building):
        sunset.append(True)
    else:
        sunset.append(False)

    prev_building.append(building)
    
sun_buildings = sunset.count(True)

external_stylesheets =['https://codepen.io/IvanNieto/pen/bRPJyb.css', dbc.themes.BOOTSTRAP, 
                       'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.0/css/all.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[
                    { 'name':'viewport','content':'width=device-width, initial-scale=1, shrink-to-fit=no' },
                    {
                        'name':'description',
                        'content':'An array of buildings is facing the sun. Theheights of each building from West to East isgiven in an integer array. You have to tell whichbuildings will be able to see the sunset.',
                    },
                    {
                        'name':'keywords',
                        'content':'SUNSET HILLS, CODING CHALLENGE',
                    },                        

                    {
                        'property':'og:image',
                        'content':'',
                    },
                    {
                        'name':'title',
                        'content':'Sunset Hills, Coding Challenge',                    
                    }
                ]
            )

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        {%css%}
        {%favicon%}
    </head>
    <body>
        <div></div>
        {%app_entry%}
        <footer> 
          {%config%} 
          {%scripts%} 
          {%renderer%}
        </footer>
    </body>
</html>
'''

app.title = 'Sunset Hills, Coding Challenge'

buildings = [7,4,8,2,9,4]
prev_building = []
sunset = []
sunrise = []

## sunset

for building in buildings:
    
    if not prev_building or building > max(prev_building):
        sunset.append(True)
    else:
        sunset.append(False)

    prev_building.append(building)
    
sun_buildings = sunset.count(True)

## sunrise
prev_building = []
sunrise = []

for building in buildings[::-1]:
    
    if not prev_building or building > max(prev_building):
        sunrise.append(True)
    else:
        sunrise.append(False)

    prev_building.append(building)
    
sunrise_buildings = sunrise.count(True)

sunrise = sunrise[::-1]

colors = {
            True:'yellow',
            False:'grey',
         }

def bar_fig(buildings, sunset):
            
    traces = go.Bar(#name=buildings, 
                 x=[*range(1, len(buildings)+1)],
                 y=buildings,
                 marker_color=[colors[x] for x in sunset]),
    
    layout = go.Layout(paper_bgcolor='rgba(0,0,0,0)',
               plot_bgcolor='rgba(0,0,0,0)',
                font={
                      #'family': 'Courier New, monospace',
                      #'size': 18,
                      'color': 'grey'
                      },
                xaxis={    
                    'showgrid': False, # thin lines in the background
                    'zeroline': False, # thick line at x=0
                    'visible': False,  # numbers below
                    'tickmode':'linear',
                    #'autorange':False,
                },                                                
                yaxis={
                    'showgrid': False,
                    'zeroline': False,
                    'visible': False,
                    #'gridcolor':'grey'
                },
                autosize=False,
                margin=dict(
                      l=0,
                      r=0,
                      b=0,
                      t=0,
                ),
            )
    
    fig = go.Figure(data=traces, layout=layout)

    return fig


buildings_card = [
    
                    dcc.Graph(figure=bar_fig(buildings,sunset), id='buildings-fig')        
        
                 ]

def theme():
    return html.Div([dbc.Button([html.Span(id='theme-icon')], className='fixed-btn2')], id='theme-button', className='button-container2')

def button():
    return html.Div([dbc.Button([html.Span(className='fab fa-github icon')], className='fixed-btn', href='https://github.com/addenergyx/cf-coding-challenge', external_link=True)], className='button-container')

# @app.callback(Output('buildings-fig', 'figure'),[Input("theme-button", "n_clicks")])
# def update_sun(clicks):
    
#     if clicks == None:
#         return bar_fig(buildings,sunset)
    
#     return bar_fig(buildings, sunrise)

@app.callback([Output("theme-icon", "className"), Output("background", "style"), Output("build","style"), Output('buildings-fig', 'figure')],
              [Input("theme-button", "n_clicks")],
              [State('theme-icon', "className")])
def update_thene(value, icon):
            
    if icon == 'fas fa-sun icon':
        return 'far fa-moon icon', {'background-image': 'url("./assets/img/sunset.jpg")'},  {'background': '#2A0892', 'box-shadow':  '12px -12px 24px #180555, -12px 12px 24px #3c0bcf'}, bar_fig(buildings, sunset) 
    return 'fas fa-sun icon', {'background-image': 'url("./assets/img/Tatooine.jpg")'}, {'background': '#FD7143', 'box-shadow' : '-12px 12px 24px #652d1b, 12px -12px 24px #ffb56b'}, bar_fig(buildings, sunrise)
    
def Homepage():
    return html.Div([
            #html.H2('Sunset Hills Coding Challenge', style={'text-align':'center'}),
            theme(),
            button(),
            html.Div(dbc.Card(buildings_card, id='build', className='card-style'), id='buildings-card', className='center-screen'),
        ], id='background')

# we need to set layout to be a function so that for each new page load                                                                                                       
# the layout is re-created with the current data, otherwise they will see                                                                                                     
# data that was generated when the Dash app was first initialised             
app.layout = Homepage()

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
