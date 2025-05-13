from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
image_path = 'assets/code01.jpg'

# Returns an input with callback
def tab1():
    tab1_content = html.Div(children=[
        dbc.Card( # This adds some styling, padding
                    dbc.CardBody([
                            html.Div(children=[ # This is needed for multiple elements
                                html.H3("Dash with callback", style={"marginTop": "0px"}),
                                html.Div([
                                    "Input:  ",
                                    dcc.Input(id='inputDivId', value='', type='text') # Input with id for callback output
                                ], style={"margin-top": "20px"}),
                                html.Div(id='outputDivId', style={"marginTop": "20px"}), # Id for callback output
                            ]),
                    ],
                    style={"width": "100%", "display": "flex", "justifyContent": "center"}),
                    className="mt-3",
                    
                ),
                # Button and collapsable component for showing code.
                html.Div(children=
                [
                    dbc.Button("Show code", id="collapse-button01", color="success", outline=True, style={"width": "500px", "margin": "auto"}),
                    dbc.Collapse(
                        dbc.Card(dbc.CardBody(
                            html.Img(src=r'assets/code01.jpg', alt='image',
                                    style={"width": "90vw"}
                                     ),style={"margin": "auto"}
                        )),
                        id="collapse",
                        is_open=False,
                    ),
                ],
                style={"width": "100%"},
                className="d-grid gap-2 col-6 mx-auto mt-5",
            )
    ])   
    return tab1_content

# Callback for displaying input field value
@callback( # The chosen input below -triggers the function below the callback, and returns to the chosen output.
    Output(component_id='outputDivId', component_property='children'),
    Input(component_id='inputDivId', component_property='value')
)
def update_output_div(input_value): # The parameter is the first (only) input component property above
    return f'Output:  {input_value}' # It gets returned to the first (only) output.

# Callback for handling collapsable component, returns True/False depending on state of is_open
@callback(
    Output("collapse", "is_open"),
    Input("collapse-button01", "n_clicks"),
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open