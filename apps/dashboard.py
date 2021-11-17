import dash_bootstrap_components as dbc
from dash import html, Input, Output, State
from app import app
from dashboard_functions import cleaned_data_reader, heatmap_generator, top_states_generator, top_cities_generator, incidents_per_day_generator, incidents_per_month_generator, incidents_per_year_generator, age_distribution_generator, gun_type_distribution_generator, gun_count_distribution_generator, suspect_gender_distribution_generator, victim_gender_distribution_generator


data = cleaned_data_reader()
incident_heatmap = heatmap_generator(data)
top_states = top_states_generator(data)
top_cities = top_cities_generator(data)
incidents_per_day = incidents_per_day_generator(data)
incidents_per_month = incidents_per_month_generator(data)
incidents_per_year = incidents_per_year_generator(data)
age_distribution = age_distribution_generator(data)
gun_type_distribution = gun_type_distribution_generator(data)
gun_count_distribution = gun_count_distribution_generator(data)
suspect_gender_distribution = suspect_gender_distribution_generator(data)
victim_gender_distribution = victim_gender_distribution_generator(data)


page_content_1_modal = html.Div(
    children=[
        dbc.Button(
            className="bg-dark text-light",
            id="open_modal_1",
            n_clicks=0,
            children=['...'],
            outline=True
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Severity of Incidents Across The US")),
                dbc.ModalBody(
                    children=[
                        html.P("From the charts it is clear that the states of California, Texas, Florida, and Illinois suffer from a high number of gun related crimes. When looking at cities/counties however, Chicago is by far the most dangerous one making up for around 75% of incidents in Illinois."),
                        html.P("Some possible explanations for why the 10 states have so many incidents could be due to their high population count or the states' leniency regarding gun laws.")
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_modal_1", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="page_content_1_modal",
            is_open=False,
        )
    ]
)


page_content_2_modal = html.Div(
    children=[
        dbc.Button(
            className="bg-dark text-light",
            id="open_modal_2",
            n_clicks=0,
            children=['...'],
            outline=True
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Incidents Per Day/Month/Year")),
                dbc.ModalBody(
                    children=[
                        html.P("When looking at the avg+total incidents per day, it appears that a gun related crime is more likely to happen on a Saturday and Sunday compared to the rest of the days. This could be attributed to the fact that people are more likely to go out during the weekend."),
                        html.P("From looking at the incidents per month, two of the safest months are November and December. This is likely due to it being the end of the year where most people are celebrating holidays (i.e. Thanksigiving, Christmas, Hanukkah)."),
                        html.P("As the years go by, gun violence crimes are increasing at a steady rate. In 2014, there were ~35k incidents whereas in 2017, there were 46.2k incidents.")
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_modal_2", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="page_content_2_modal",
            is_open=False,
        )
    ]
)


page_content_3_modal = html.Div(
    children=[
        dbc.Button(
            className="bg-dark text-light",
            id="open_modal_3",
            n_clicks=0,
            children=['...'],
            outline=True
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Age Distribution of People Involved")),
                dbc.ModalBody(
                    children=[
                        html.P("According to the data, most people involved in gun violence related crimes range from age 16-30. Suspects of gun violence related crimes see a dramatic increase from ages 12 to 19 where it then sees a dropoff until age 32. The increase could be due to how children and young adults see gun violence as a means of expressing power. The decrease could be due to how young adults mature and realize the consequences related to committing crimes.")
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_modal_3", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="page_content_3_modal",
            is_open=False,
        )
    ]
)


page_content_4_modal = html.Div(
    children=[
        dbc.Button(
            className="bg-dark text-light",
            id="open_modal_4",
            n_clicks=0,
            children=['...'],
            outline=True
        ),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Gun Types/Counts + Suspect/Victim Gender Distributions")),
                dbc.ModalBody(
                    children=[
                        html.P("The most common type of firearm used in gun violence crimes are handguns which account for 72% of incidents. Approximately 91% of incidents also only involved the use of 1 weapon."),
                        html.P("Both suspects and victims have a large imbalance between genders with males having a 93%/7% and 82%/18% ratio respectively.")
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_modal_4", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="page_content_4_modal",
            is_open=False,
        )
    ]
)


page_content_1 = dbc.Container(
    children=[
        dbc.Row(
            className="mt-4 g-0",
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(className="text-center bg-dark text-light", children=['Severity of Incidents Across The US']),
                        body=True,
                        color="dark",
                        style={'height': '100%'}
                    ),
                    lg=10
                ),

                dbc.Col(
                    dbc.Card(
                        className="justify-content-center text-center",
                        children=[
                            page_content_1_modal
                        ],
                        body=True,
                        color="dark",
                        style={'height': '100%'}
                    ),
                    lg=2
                )
            ]
        ),

        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Card(className="shadow-sm rounded", children=[incident_heatmap]),
                    ],
                    style={'height': '100%'},
                    lg=6
                ),

                dbc.Col(
                    children=[
                        dbc.Row(
                            dbc.Col(dbc.Card(className="shadow-sm rounded", children=[top_states])),
                        ),
                        dbc.Row(
                            dbc.Col(dbc.Card(className="shadow-sm rounded", children=[top_cities])),
                        )
                    ],
                    lg=6
                ),
            ]
        )
    ]
)


page_content_2 = dbc.Container(
    children=[
        dbc.Row(
            className="mt-4 g-0",
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(className="text-center bg-dark text-light", children=['Incidents Per Day/Month/Year']),
                        body=True,
                        color="dark",
                        style={'height': '100%'}
                    ),
                    lg=10
                ),

                dbc.Col(
                    dbc.Card(
                        className="justify-content-center text-center",
                        children=[
                            page_content_2_modal
                        ],
                        body=True,
                        color="dark",
                        style={'height': '100%'}
                    ),
                    lg=2
                )
            ]
        ),

        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Card(className="shadow-sm rounded", children=[incidents_per_day]),
                    ],
                    lg=4
                ),

                dbc.Col(
                    children=[
                        dbc.Card(className="shadow-sm rounded", children=[incidents_per_month]),
                    ],
                    lg=4
                ),

                dbc.Col(
                    children=[
                        dbc.Card(className="shadow-sm rounded", children=[incidents_per_year]),
                    ],
                    lg=4
                ),
            ]
        )
    ]
)


page_content_3 = dbc.Container(
    children=[
        dbc.Row(
            className="mt-4 g-0",
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(className="text-center bg-dark text-light", children=['Age Distribution of People Involved']),
                        body=True,
                        color="dark",
                        style={'height': '100%'}
                    ),
                    lg=10
                ),

                dbc.Col(
                    dbc.Card(
                        className="justify-content-center text-center",
                        children=[
                            page_content_3_modal
                        ],
                        body=True,
                        color="dark",
                        style={'height': '100%'}
                    ),
                    lg=2
                )
            ]
        ),

        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Card(className="shadow-sm rounded", children=[age_distribution]),
                    ],
                    lg=12
                )
            ]
        )
    ]
)


page_content_4 = dbc.Container(
    children=[
        dbc.Row(
            className="mt-4 g-0",
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(className="text-center bg-dark text-light", children=['Severity of Incidents Across The US']),
                        body=True,
                        color="dark",
                        style={'height': '100%'}
                    ),
                    lg=10
                ),

                dbc.Col(
                    dbc.Card(
                        className="justify-content-center text-center",
                        children=[
                            page_content_4_modal
                        ],
                        body=True,
                        color="dark",
                        style={'height': '100%'}
                    ),
                    lg=2
                )
            ]
        ),

        dbc.Row(
            className="g-0",
            children=[
                dbc.Col(
                    children=[
                        dbc.Card(className="shadow-sm rounded", children=[gun_type_distribution]),
                    ],
                    lg=6
                ),

                dbc.Col(
                    children=[
                        dbc.Card(className="shadow-sm rounded", children=[gun_count_distribution]),
                    ],
                    lg=6
                ),
            ]
        ),

        dbc.Row(
            className="g-0",
            children=[
                dbc.Col(
                    children=[
                        dbc.Card(className="shadow-sm rounded", children=[suspect_gender_distribution]),
                    ],
                    lg=6
                ),

                dbc.Col(
                    children=[
                        dbc.Card(className="shadow-sm rounded", children=[victim_gender_distribution]),
                    ],
                    lg=6
                ),
            ],
        )
    ]
)


@app.callback(
    Output("page_content_1_modal", "is_open"),
    [Input("open_modal_1", "n_clicks"), Input("close_modal_1", "n_clicks")],
    [State("page_content_1_modal", "is_open")],
)
def toggle_modal_1(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("page_content_2_modal", "is_open"),
    [Input("open_modal_2", "n_clicks"), Input("close_modal_2", "n_clicks")],
    [State("page_content_2_modal", "is_open")],
)
def toggle_modal_2(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("page_content_3_modal", "is_open"),
    [Input("open_modal_3", "n_clicks"), Input("close_modal_3", "n_clicks")],
    [State("page_content_3_modal", "is_open")],
)
def toggle_modal_3(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("page_content_4_modal", "is_open"),
    [Input("open_modal_4", "n_clicks"), Input("close_modal_4", "n_clicks")],
    [State("page_content_4_modal", "is_open")],
)
def toggle_modal_4(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


layout = html.Div(
    children=[
        page_content_1,
        page_content_2,
        page_content_3,
        page_content_4
    ]
)


if __name__ == '__main__':
    print('This is the dashboard layout file')