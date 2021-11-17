import dash_bootstrap_components as dbc
from dash import html
from app import app

description = dbc.Container(
    className="bg-light rounded",
    children=[
        html.H1(className="text-center mt-3", children=['Analysis of Gun Violence in the US']),
        html.Hr(),
        html.P(className="mt-4", children=['Gun violence is a very controversial topic in the US. The topic has sparked many conversations about whether firearms should be banned or not. This dashboard aims to explore and reveal trends around firearm related crimes from 2013-2017.']),
        html.P(
            className="mt-3",
            children=[
                'The data used for analysis is sourced from the ',
                html.A(children=['Gun Violence Archive'], href="https://www.gunviolencearchive.org/", target="_blank", style = {'color': 'red'}),
                '. The scripts used to webscrape the data is written by James Qo and can be viewed at this ',
                html.A(children=['GitHub Repository'], href="https://github.com/jamesqo/gun-violence-data", target="_blank", style = {'color': 'red'}),
                '.'
            ],
        ),
        html.P(
            className="mt-3",
            children=[
                'View source on ',
                html.A(children=['GitHub'], href="https://github.com/aLeadPencil/gun-violence-dashboard", target="_blank", style = {'color': 'red'}),
                '.'
            ]
        )
    ]
)


layout = html.Div(
    dbc.Container(
        children=[
            description
        ]
    )
)

if __name__ == '__main__':
    print('This is the home layout file')