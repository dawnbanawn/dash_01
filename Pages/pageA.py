from dash import html, Input, Output, callback, State
import dash_bootstrap_components as dbc

# Returns an input with callback
def tabA():
    tab1_content = html.Div(children=[
        dbc.Card( # This adds some styling, padding
                    dbc.CardBody([
                        html.Div(children = [
                            html.H5("This app is the last step in the E2E data analysis pipeline. ", style={"marginBottom": "25px"}),
                            html.Img(src=r'assets/pipeline_logos.jpg', alt='image',
                            style={"width": "20vw","marginBottom": "25px"}
                                ),
                            html.Div("Data is fetched from Databricks from a local .py file, and saved locally as .csv. The data is displayed in graphs on the last two tabs."),
                            html.Div("",style={"marginBottom": "20px"}),
                            # html.Div("In the first two tabs I made basic examples with Dash, callbacks and a type of grid called Ag Grid with mock data, before using the technologies with the incoming data in the last two tabs. I made these for training before the last two tabs, and if I need more light weight examples when teaching someone how the technologies work."),
                            # html.Div("",style={"marginBottom": "20px"}),
                            html.Div("Press the button below to see a part of the code that fetches the data. These buttons can be found in every tab, showing some of the code used in that tab."), 
                            html.Div("",style={"marginBottom": "20px"}),
                            html.Div("Read more about this project in the report."),
                          ],
                            style={"display": "flex", "justifyContent": "center", "flexDirection": "column", "alignItems": "center", "margin": "100px"})
                    ],
                    style={"width": "100%", "display": "flex", "justifyContent": "center"}),
                    className="mt-3",                    
                ),


            html.Div(children=
        [
            dbc.Button("Show code", id="collapse-buttonA", color="success", outline=True, style={"width": "500px", "margin": "auto"}),
            dbc.Collapse(
                dbc.Card(dbc.CardBody(
                    html.Img(src=r'assets/codeA.jpg', alt='image',
                            style={"width": "90vw"}
                                ),style={"margin": "auto"}
                )),
                id="collapseA",
                is_open=False,
            ),
        ],
        style={"width": "100%"},
        className="d-grid gap-2 col-6 mx-auto mt-5",),  

                
    ],
    )   
    return tab1_content



# Callback for handling collapsable component, returns True/False depending on state of is_open
@callback(
    Output("collapseA", "is_open"),
    Input("collapse-buttonA", "n_clicks"),
    [State("collapseA", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open