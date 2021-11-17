import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

from app import app
from app import server #not used in file but necessary for heroku deployment
from apps import home, datapreview, dashboard


navbar = dbc.Nav(
    className="navbar navbar-expand-sm navbar-dark bg-dark rounded mb-2",
    children=[
        html.Div(
            className="collapse navbar-collapse justify-content-sm-center d-flex",
            children=[
                dbc.Nav(
                    className="navbar-nav",
                    children=[
                        dbc.Nav(
                            className="nav-item px-4",
                            children=[
                                dcc.Link(className="nav-link active", children=["Home"], href="/")
                            ]
                        ),
                        dbc.Nav(
                            className="navbar-nav px-4",
                            children=[
                                dcc.Link(className="nav-link active", children=["Data Preview"], href="/data-preview")
                            ]
                        ),
                        dbc.Nav(
                            className="navbar-nav px-4",
                            children=[
                                dcc.Link(className="nav-link active", children=["Dashboard"], href="/dashboard")
                            ]
                        ),
                        dbc.DropdownMenu(
                            className="navbar-nav rounded px-4",
                            label="Contact",
                            color="secondary",
                            children=[
                                dcc.Link(className="dropdown-item", children="LinkedIn", href="https://www.linkedin.com/in/kvn-chu/", target="_blank"),
                                dcc.Link(className="dropdown-item", children="GitHub", href="https://github.com/aLeadPencil", target="_blank"),
                                dcc.Link(className="dropdown-item", children="Email Me", href="mailto:kchu8150@gmail.com", target="_blank")
                            ],
                        )
                    ]
                )
            ]
        )
    ]
)

error_page = dbc.Container(
    className="bg-light rounded",
    children=[
        html.H1(
            className="text-center rounded mt-3",
            children=[
                "PAGE DOESN'T EXIST",
                html.Hr(),
                dbc.Button(
                    className="btn btn-secondary",
                    children="Click Here To Return Home",
                    href="/"
                )
            ]
        )
    ]
)

app.layout = html.Div(
    children=[
        dbc.Row(
            className="justify-content-sm-center mx-1",
            children=[
                dbc.Col(children=[navbar], xl = 6)
            ]
        ),

        dcc.Location(id="url", refresh=False),
        html.Div(id='page-content')
    ]
)

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname =='/':
        return home.layout
    elif pathname == '/data-preview':
        return datapreview.layout
    elif pathname == '/dashboard':
        return dashboard.layout
    else:
        return error_page


if __name__ == '__main__':
    app.run_server(debug=True)