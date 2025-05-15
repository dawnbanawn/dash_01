import pandas as pd
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import random
from dash import html, Input, Output, clientside_callback, State, callback

# Generate dataframe with random numbers.
def getRandInt():
    return [random.randint(0, 10000) for _ in range(10)]
df = pd.DataFrame({
    'a': getRandInt(),
    'b': getRandInt(),
    'c': getRandInt(),
    'd': getRandInt(),
    'e': getRandInt(),
    'f': getRandInt(),
})

# Function that returns tab 2.
def tab2():
    tab2_content = html.Div(children=[
        dbc.Card(
            dbc.CardBody([
                html.Div(
                    [
                        html.H3("Ag grid with grid api", style={"margin":"auto", "marginBottom": "20px"}),
                        dag.AgGrid( # Ag grid
                            id="gridId", # Id to reach it wich callback
                            className="ag-theme-alpine-dark", # dark theme
                            rowData=df.to_dict("records"), # Data
                            columnDefs=[{"field": i } for i in df.columns], # column headers
                            defaultColDef={"flex": 1,"cellClass": 'align-right', "enableCellChangeFlash": True}
                        ),
                        html.Div("", id="outputId"), # Output for the callback return cell value.
                    ], style={"display": "flex", "justifyContent":"center", "flexDirection": "column"}
                )]
            ),
            className="mt-3",
        ),
        # Button and collapsable component for showing code.
        html.Div(children=
        [
            dbc.Button("Show code", id="collapse-button02", color="success", outline=True, style={"width": "500px", "margin": "auto"}),
            dbc.Collapse(
                dbc.Card(dbc.CardBody(
                    html.Img(src=r'assets/code02.jpg', alt='image',
                            style={"width": "90vw"}
                                ),style={"margin": "auto"}
                )),
                id="collapse02",
                is_open=False,
            ),
        ],
        style={"width": "100%"},
        className="d-grid gap-2 col-6 mx-auto mt-5",
        )
    ])   
    return tab2_content

# Callback for handling collapsable component, returns True/False depending on state of is_open
@callback(
    Output("collapse02", "is_open"),
    Input("collapse-button02", "n_clicks"),
    [State("collapse02", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Clientside callbacks are written in javascript. 
# The api of the Ag Grid is used alongside the cell info from the grid when "cellClicked" is triggered.
clientside_callback( 
    """
    async function(n) {
            const gridApi = await window.dash_ag_grid.getApiAsync("gridId");
            const rowNode = gridApi.getDisplayedRowAtIndex(n.rowId);
            gridApi.flashCells({ rowNodes: [rowNode], columns: [n.colId] });
            rowNode.setDataValue(n.colId,100)
            return `Value: ${n.value.toString()}, Column: ${n.colId.toString()}, Row: ${n.rowId.toString()} `
    }
    """,
    Output("outputId", "children"), # The values are returned here. The api triggers the flashing cell inside the javascript code.
    Input("gridId", "cellClicked"),
    prevent_initial_call = True # Callbacks are usually also triggered when the browser loads, this prevents that.
)

# Sometimes client side callbacks can be used for improved performance. 
# A "normal" callback uses the dash server, but a client side callback 
# is run in the browser without using the server.
# If a callback callback requires interacting with databases, APIs, or 
# other server-side processes, it must run on the server.
# Larger data are best handled with server callback.
# To sum it up: Clientside callbacks are best for lightweight, browser-based operations, 
# but server-side callbacks are needed when dealing with sensitive data, 
# backend resources, or complex operations.