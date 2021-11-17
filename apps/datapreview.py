import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dash_table
from dash.dependencies import Input, Output, State
from app import app

data = pd.read_csv('data/cleaned_data/cleaned_data_1.csv', nrows=100)

data_table = dash_table.DataTable(
    style_cell = {
        'whiteSpace': 'normal',
        'height': 'auto',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 70,
    },

    style_table = {
        'overflowX': 'auto',
    },

    css = [
        {
            'selector': '.dash-spreadsheet td div',
            'rule': '''
                line-height: 15px
                max-height: 50px; 
                min-height: 50px; 
                height: 50px;
                display: block;
                overflow-y: hidden;
            '''
        }
    ],

    columns = [{'name': i, 'id': i} for i in data.columns],
    page_size = 10,
    data = data.to_dict('records')
)


offcanvas = html.Div(
    children=[
        dbc.Button(
            className="bg-dark text-light",
            id="open-offcanvas",
            n_clicks=0,
            outline=True,
            children=['Data Dictionary'],
        ),

        dbc.Offcanvas(
            html.P(
                children=[
                    html.Span('DATE: ', className="text-success"),
                    html.Span('Date of incident'),
                    html.Br(),
                    html.Br(),

                    html.Span('STATE: ', className="text-success"),
                    html.Span('State of incident'),
                    html.Br(),
                    html.Br(),

                    html.Span('CITY_OR_COUNTY: ', className="text-success"),
                    html.Span('City/County of incident'),
                    html.Br(),
                    html.Br(),

                    html.Span('N_KILLED: ', className="text-success"),
                    html.Span('# of people killed'),
                    html.Br(),
                    html.Br(),

                    html.Span('N_INJURED: ', className="text-success"),
                    html.Span('# of people injured'),
                    html.Br(),
                    html.Br(),

                    html.Span('GUN_TYPE: ', className="text-success"),
                    html.Span('List of gun types (rifle, handgun, shotgun)'),
                    html.Br(),
                    html.Br(),

                    html.Span('N_GUNS_INVOLVED: ', className="text-success"),
                    html.Span('# of guns involved'),
                    html.Br(),
                    html.Br(),

                    html.Span('PARTICIPANT_AGE: ', className="text-success"),
                    html.Span('List of participant ages'),
                    html.Br(),
                    html.Br(),

                    html.Span('PARTICIPANT_GENDER: ', className="text-success"),
                    html.Span('List of participant genders'),
                    html.Br(),
                    html.Br(),

                    html.Span('PARTICIPANT_STATUS: ', className="text-success"),
                    html.Span('List of participant statuses (injured, unharmed)'),
                    html.Br(),
                    html.Br(),

                    html.Span('PARTICIPANT_TYPE: ', className="text-success"),
                    html.Span('List of participant types (victim, suspect)'),
                ]
            ),
            id="offcanvas",
            title="Data Dictionary",
            is_open=False,
            scrollable=True
        ),
    ]
)


page_content_1 = dbc.Container(
    children=[
        dbc.Row(
            className="g-0",
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(className="text-center bg-dark text-light", children=['Data Table']),
                        body=True,
                        color="dark",
                        style={'height': '100%'}
                    ),
                    lg=9
                ),

                dbc.Col(
                    dbc.Card(
                        className="justify-content-center text-center",
                        children=[
                            offcanvas
                        ],
                        body=True,
                        color="dark",
                        style={'height': '100%'}
                    ),
                    lg=3
                )
            ],
        ),
        data_table
    ]
)


@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


layout = html.Div(
    children=[
        page_content_1
    ]
)

if __name__ == '__main__':
    print('This is the data preview layout file')