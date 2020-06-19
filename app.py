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
import random

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

app.config.suppress_callback_exceptions = True

server = app.server

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

def generate_sunset(buildings):
    
    prev_building = []
    sunset = []
    for building in buildings:
        
        if not prev_building or building > max(prev_building):
            sunset.append(True)
        else:
            sunset.append(False)
    
        prev_building.append(building)
        
    #sunset_buildings = sunset.count(True)
    
    return sunset

def generate_sunrise(buildings):

    prev_building = []
    sunrise = []
    for building in buildings[::-1]:
    
        if not prev_building or building > max(prev_building):
            sunrise.append(True)
        else:
            sunrise.append(False)
    
        prev_building.append(building)
        
    #sunrise_buildings = sunrise.count(True)
    
    sunrise = sunrise[::-1]
    
    return sunrise

colors = {
            True:'yellow',
            False:'maroon',
         }

def bar_fig(buildings, sun):
        
    traces = go.Bar(#name=buildings, 
                 x=list(buildings.keys()),
                 y=list(buildings.values()),
                 marker_color=[colors[x] for x in sun]),

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

    return go.Figure(data=traces, layout=layout)


buildings_card = [
                    dcc.Loading(
                        dcc.Graph(id='buildings-fig'), 
                        type="circle",        
                    )
                 ]

modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Sunset Hills Settings", style={'margin':'0 auto'}),
                dbc.ModalBody(
                    [
                        dbc.Row([
                            dbc.Col([
                                html.P("Number of buildings", style={'margin':0}),
                            ]),
                            dbc.Col([dcc.Input(value=0, id='num-buildings', type='number')])
                        ], className="align-items-center", style={'margin-bottom':'1rem'}),

                        html.Div(id='row-buildings')
                        
                    ],style={'textAlign':'center'}),
                dbc.ModalFooter(
                    [
                        dbc.Button("Worlds Tallest Buildings", id="tallest-buildings"),
                        dbc.Button("Submit", id="user-submit", className="ml-auto", style={'background-image': 'linear-gradient(to bottom right, #FD7143, #2A0892)'}),
                    ]
                ),
            ],
            id="modal",
            centered=True,
            scrollable=True,
        ), 
    ], style={'padding-right':'20px','padding-bottom':'40px'},
)

def theme():
    return html.Div([dbc.Button([html.Span(id='theme-icon')], className='fixed-btn2')], id='theme-button', className='button-container2')

def button():
    return html.Div(
                [
                    html.Div(dbc.Button([html.Span(className='fa fa-bars icon')], className='fixed-btn', id='nav-bars'), className='block'),
                    html.Ul(
                        [
                            html.Li(dbc.Button([html.Span(className='fa fa-cog icon')], id='input-button', className='fixed-btn')),
                            html.Li(dbc.NavLink(dbc.Button([html.Span(className='fab fa-github icon')], className='fixed-btn'), href='https://github.com/addenergyx/sunset-hills-coding-challenge', external_link=True)),
                        ],className='button-options', id='button-options')
                ], className='button-container'
              ),

@app.callback(
    Output("modal", "is_open"),
    [Input("input-button", "n_clicks"), Input('user-submit', 'n_clicks'), Input('tallest-buildings', 'n_clicks')],
    [State("modal", "is_open")],
)
def toggle_modal(n1, submit, tall, is_open):

    if n1 or submit is not None or tall is not None:
        return not is_open
    
    return is_open

@app.callback(
    Output("row-buildings", "children"),
    [Input("num-buildings", "value")],
)
def update_buildings(value):    
    if value is None:
        return ''
    return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.P(f'Building {a} height', className='util-name')),
                            dbc.Col(dcc.Input(value=0, id='building-input-{a}', type='number')),
                        ], className='settings-block'
                    ) for a in range(1, value+1)
                ], id='user-input'
            )

def tallest_towers():
    
    # Could scrape data from a site but may increase execution time considerably
    world_tallest_buildings = [828, 632, 601, 599, 554.5, 541.3, 530, 530, 528, 508]

    tallest_buildings_names = ['Burj Khalifa', 'Shanghai Tower', 'Abraj Al-Bait Clock Tower', 
         'Ping An Finance Center', 'Lotte World Tower', 'One World Trade Center', 
         'Guangzhou CTF Finance Center', 'Tianjin CTF Finance Center', 'China Zun', 'Taipei 101']
    
    c = list(zip(world_tallest_buildings, tallest_buildings_names))
    random.shuffle(c)
    a, b = zip(*c)
    
    # world_tallest_buildings = list(a)
    # tallest_buildings_names = list(b)
    
    towers_dict = dict(zip(list(b), list(a)))
    
    return towers_dict

@app.callback([Output("theme-icon", "className"), Output("background", "style"), 
               Output("build","style"), Output('title', 'children'), Output('buildings-fig', 'figure'), Output('data','children')],
              [Input("theme-button", "n_clicks"), Input('user-input', 'children'), Input('user-submit', 'n_clicks'), Input('tallest-buildings', 'n_clicks')],
              [State('theme-icon', "className"), State('data','children')])
def update_theme(value, values, click, tallest, icon, state):
    
    if state is None:
        state = []
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered]

    state.insert(0, changed_id)
    
    name_ = [a['props']['children'][0]['props']['children']['props']['children'].rstrip(' height') for a in values]
    user_ = [a['props']['children'][1]['props']['children']['props']['value'] for a in values]
        
    ## If user leaves input blank replace none with 0
    user_ = [0 if v is None else v for v in user_]
    
    user_dict = dict(zip(name_, user_))
            
    for a in state:
        # print(a)
        if a == ['tallest-buildings.n_clicks']:
            user_dict = tallest_towers()
            break
        if a == ['user-submit.n_clicks']:
            break
    
    if 'user-input.children' in changed_id:
        return 'fas fa-cloud-sun icon', {}, {}, '', bar_fig(user_dict, generate_sunrise(list(user_dict.values()))), state

    if 'user-submit.n_clicks' in changed_id:        
        if icon == 'fas fa-sun icon':
            fig = bar_fig(user_dict, generate_sunrise(list(user_dict.values())))
            background = {'background-image': 'url("./assets/img/Tatooine.jpg")'}
            block = {'background': '#FD7143', 'box-shadow' : '-12px 12px 24px #652d1b, 12px -12px 24px #ffb56b'}
            text = html.H1('Sunrise Fields', style={'color':'black'})
        else:
            fig = bar_fig(user_dict, generate_sunset(list(user_dict.values())))
            background = {'background-image': 'url("./assets/img/sunset.jpg")'}
            block = {'background': '#2A0892', 'box-shadow':  '12px -12px 24px #180555, -12px 12px 24px #3c0bcf'}
            text = html.H1('Sunset Hills', style={'color':'white'})
            
    if 'theme-button.n_clicks' in changed_id:
        if icon == 'fas fa-sun icon':
            icon = 'far fa-moon icon'
            fig = bar_fig(user_dict, generate_sunset(list(user_dict.values())))
            background = {'background-image': 'url("./assets/img/sunset.jpg")'}
            block = {'background': '#2A0892', 'box-shadow':  '12px -12px 24px #180555, -12px 12px 24px #3c0bcf'}
            text = [html.H1('Sunset Hills', style={'color':'white'})]
        else: 
            icon ='fas fa-sun icon'
            fig = bar_fig(user_dict, generate_sunrise(list(user_dict.values())))
            background = {'background-image': 'url("./assets/img/Tatooine.jpg")'}
            block = {'background': '#FD7143', 'box-shadow' : '-12px 12px 24px #652d1b, 12px -12px 24px #ffb56b'}
            text = [html.H1('Sunrise Fields', style={'color':'black'})]
    
    if 'tallest-buildings.n_clicks' in changed_id:
        
        user_dict = tallest_towers()
        
        if icon == 'fas fa-sun icon':
            background = {'background-image': 'url("./assets/img/Tatooine.jpg")'}
            text = html.H1('Sunrise Fields', style={'color':'black'})
            block = {'background': '#FD7143', 'box-shadow' : '-12px 12px 24px #652d1b, 12px -12px 24px #ffb56b'}
            fig = bar_fig(user_dict, generate_sunrise(list(user_dict.values())))
        else:
            background = {'background-image': 'url("./assets/img/sunset.jpg")'}
            block = {'background': '#2A0892', 'box-shadow':  '12px -12px 24px #180555, -12px 12px 24px #3c0bcf'}
            text = html.H1('Sunset Hills', style={'color':'white'})
            fig = bar_fig(user_dict, generate_sunset(list(user_dict.values())))
    
    return icon, background, block, text, fig, state
      
def Homepage():
    return html.Div([
            html.Div(id='title'),
            theme(),
            html.Div(button()),
            html.Div(modal),
            html.Div(dbc.Card(buildings_card, id='build', className='card-style'), id='buildings-card', className='center-screen'),
            html.Div(id='data', hidden=True),
        ], id='background')

# we need to set layout to be a function so that for each new page load                                                                                                       
# the layout is re-created with the current data, otherwise they will see                                                                                                     
# data that was generated when the Dash app was first initialised             
app.layout = Homepage

if __name__ == '__main__':
    # app.run_server()
    app.run_server(debug=True, use_reloader=False)

