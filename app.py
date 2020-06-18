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

# buildings = [7,4,8,2,9,4]
# prev_building = []
# sunset = []

# for building in buildings:
    
#     if not prev_building or building > max(prev_building):
#         sunset.append(True)
#     else:
#         sunset.append(False)

#     prev_building.append(building)
    
# sun_buildings = sunset.count(True)

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

## sunset

def generate_sunset(buildings):
    
    prev_building = []
    sunset = []
    for building in buildings:
        
        if not prev_building or building > max(prev_building):
            sunset.append(True)
        else:
            sunset.append(False)
    
        prev_building.append(building)
        
    sunset_buildings = sunset.count(True)
    
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
        
    sunrise_buildings = sunrise.count(True)
    
    sunrise = sunrise[::-1]
    
    return sunrise

colors = {
            True:'yellow',
            False:'grey',
         }

def bar_fig(buildings, sun):
            
    traces = go.Bar(#name=buildings, 
                 x=[*range(1, len(buildings)+1)],
                 y=buildings,
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
    
    fig = go.Figure(data=traces, layout=layout)

    return fig


buildings_card = [
                    dcc.Graph(id='buildings-fig')        
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

# @app.callback(Output('buildings-fig', 'figure'),[Input("theme-button", "n_clicks")])
# def update_sun(clicks):
    
#     if clicks == None:
#         return bar_fig(buildings, sunset)
    
#     return bar_fig(buildings, sunrise)

@app.callback(
    Output("modal", "is_open"),
    [Input("input-button", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(
    Output("row-buildings", "children"),
    [Input("num-buildings", "value")],
)
def update_buildings(value):
    return html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(html.P(f'Building {a} height', className='util-name')),
                            dbc.Col(dcc.Input(value=0, id={"building":'building-input-{a}', 'height':value}, type='number')),
                        ], className='settings-block'
                    ) for a in range(1, value+1)
                ], id='user-input'
            )

# @app.callback(
#     Output("button-options", "style"),
#     [Input("nav-bars", "n_clicks")],
# )
# def toggle_nav(n_click):
    
#     if n_click is None:
#         return {'opacity' : 0, 'transform': 'scale(0)'}
    
#     if n_click%2 == 1:
#         return {'opacity' : 1, 'transform': 'scale(1)'}
    
#     return {'opacity' : 0, 'transform': 'scale(0)'}

        
# @app.callback(
#     Output('buildings-fig', 'figure'),
#     [Input('user-input', 'children'), Input('user-submit', 'n_clicks')],
#     [State('theme-icon', "className")]
# )
# def display_output(values, click, icon):
    
#     if click:
#         print(values)
    
#     #aaa = values
      
#     # Example of values
#     #aaa = [{'props': {'children': [{'props': {'children': {'props': {'children': 'Building 1 height', 'className': 'util-name'}, 'type': 'P', 'namespace': 'dash_html_components'}}, 'type': 'Col', 'namespace': 'dash_bootstrap_components/_components'}, {'props': {'children': {'props': {'id': {'building': 'building-input-{a}', 'height': 3}, 'value': 2, 'type': 'number', 'n_blur': 1, 'n_blur_timestamp': 1592295227768}, 'type': 'Input', 'namespace': 'dash_core_components'}}, 'type': 'Col', 'namespace': 'dash_bootstrap_components/_components'}], 'className': 'settings-block'}, 'type': 'Row', 'namespace': 'dash_bootstrap_components/_components'}, {'props': {'children': [{'props': {'children': {'props': {'children': 'Building 2 height', 'className': 'util-name'}, 'type': 'P', 'namespace': 'dash_html_components'}}, 'type': 'Col', 'namespace': 'dash_bootstrap_components/_components'}, {'props': {'children': {'props': {'id': {'building': 'building-input-{a}', 'height': 3}, 'value': 1, 'type': 'number', 'n_blur': 1, 'n_blur_timestamp': 1592295229722}, 'type': 'Input', 'namespace': 'dash_core_components'}}, 'type': 'Col', 'namespace': 'dash_bootstrap_components/_components'}], 'className': 'settings-block'}, 'type': 'Row', 'namespace': 'dash_bootstrap_components/_components'}, {'props': {'children': [{'props': {'children': {'props': {'children': 'Building 3 height', 'className': 'util-name'}, 'type': 'P', 'namespace': 'dash_html_components'}}, 'type': 'Col', 'namespace': 'dash_bootstrap_components/_components'}, {'props': {'children': {'props': {'id': {'building': 'building-input-{a}', 'height': 3}, 'value': 4, 'type': 'number', 'n_blur': 1, 'n_blur_timestamp': 1592295233023}, 'type': 'Input', 'namespace': 'dash_core_components'}}, 'type': 'Col', 'namespace': 'dash_bootstrap_components/_components'}], 'className': 'settings-block'}, 'type': 'Row', 'namespace': 'dash_bootstrap_components/_components'}]
    
#     user_ = [a['props']['children'][1]['props']['children']['props']['value'] for a in values]
    
#     if icon == 'fas fa-sun icon':
#         fig = bar_fig(user_, generate_sunrise(user_))
#     if icon == 'far fa-moon icon':
#         fig = bar_fig(user_, generate_sunset(user_))
    
#     return fig

@app.callback([Output("theme-icon", "className"), Output("background", "style"), 
               Output("build","style"), Output('title', 'children'), Output('buildings-fig', 'figure')],
              [Input("theme-button", "n_clicks"), Input('user-input', 'children'), Input('user-submit', 'n_clicks')],
              [State('theme-icon', "className"), State('title', 'style')])
def update_theme(value, values, click, icon, state):
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print([p['prop_id'] for p in dash.callback_context.triggered])
    
    user_ = [a['props']['children'][1]['props']['children']['props']['value'] for a in values]

    ## If user leaves input blank replace none with 0
    user_ = [0 if v is None else v for v in user_]

    if 'user-input.children' in changed_id:
        #return 'fas fa-sun icon', {'background-image': 'url("./assets/img/Tatooine.jpg")'}, {'background': '#FD7143', 'box-shadow' : '-12px 12px 24px #652d1b, 12px -12px 24px #ffb56b'}, {'color':'black'}, bar_fig(user_, generate_sunrise(user_))
        return 'fas fa-cloud-sun icon', {}, {}, '', bar_fig(user_, generate_sunrise(user_))

    if 'user-submit.n_clicks' in changed_id:        
        if icon == 'fas fa-sun icon':
            fig = bar_fig(user_, generate_sunrise(user_))
            background = {'background-image': 'url("./assets/img/Tatooine.jpg")'}
            block = {'background': '#FD7143', 'box-shadow' : '-12px 12px 24px #652d1b, 12px -12px 24px #ffb56b'}
            text = html.H1('Sunrise Fields', style={'color':'black'})
        else:
            fig = bar_fig(user_, generate_sunset(user_))
            background = {'background-image': 'url("./assets/img/sunset.jpg")'}
            block = {'background': '#2A0892', 'box-shadow':  '12px -12px 24px #180555, -12px 12px 24px #3c0bcf'}
            text = html.H1('Sunset Hills', style={'color':'white'})
            
    if 'theme-button.n_clicks' in changed_id:
        if icon == 'fas fa-sun icon':
            icon = 'far fa-moon icon'
            fig = bar_fig(user_, generate_sunset(user_))
            background = {'background-image': 'url("./assets/img/sunset.jpg")'}
            block = {'background': '#2A0892', 'box-shadow':  '12px -12px 24px #180555, -12px 12px 24px #3c0bcf'}
            text = [html.H1('Sunset Hills', style={'color':'white'})]
        else: 
            icon ='fas fa-sun icon'
            fig = bar_fig(user_, generate_sunrise(user_))
            background = {'background-image': 'url("./assets/img/Tatooine.jpg")'}
            block = {'background': '#FD7143', 'box-shadow' : '-12px 12px 24px #652d1b, 12px -12px 24px #ffb56b'}
            text = [html.H1('Sunrise Fields', style={'color':'black'})]
    
    # if not user_:
    #     user_ = [0,0,0,0,0]
    
    # fig = bar_fig(user_, generate_sunrise(user_))
    
    return icon, background, block, text, fig
    
    # if icon == 'fas fa-sun icon':
    #     return 'far fa-moon icon', {'background-image': 'url("./assets/img/sunset.jpg")'},  {'background': '#2A0892', 'box-shadow':  '12px -12px 24px #180555, -12px 12px 24px #3c0bcf'}, {'color':'white'}, bar_fig(user_, generate_sunset(user_))
    # return 'fas fa-sun icon', {'background-image': 'url("./assets/img/Tatooine.jpg")'}, {'background': '#FD7143', 'box-shadow' : '-12px 12px 24px #652d1b, 12px -12px 24px #ffb56b'}, {'color':'black'}, bar_fig(user_, generate_sunrise(user_))
    
def Homepage():
    return html.Div([
            html.Div(id='title'),
            theme(),
            html.Div(button()),
            html.Div(modal),
            html.Div(dbc.Card(buildings_card, id='build', className='card-style'), id='buildings-card', className='center-screen'),
            html.Div(id='data'),
        ], id='background')

# we need to set layout to be a function so that for each new page load                                                                                                       
# the layout is re-created with the current data, otherwise they will see                                                                                                     
# data that was generated when the Dash app was first initialised             
app.layout = Homepage()

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
