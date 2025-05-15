from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import dcc, html, Input, Output, callback, Patch
import dash_ag_grid as dag
from datetime import date
import plotly.express as px
import dash_bootstrap_components as dbc

# Column names for the data, and the data
colnames=['OrderDate', 'Region', 'Total Sales']
aw_data = (
    pd.read_csv("./sales_data.csv", 
                # names=colnames, 
                header=0)    
    .astype({"OrderDate": "datetime64[ns]"})
)

# function to create a date object from a date string "YYYY-MM-DD"
date_obj = "d3.utcParse('%Y-%m-%dT%H:%M:%S')(params.data.OrderDate)"

# Individually specified column headers.
columnDefs = [
    {
        "headerName": "Date",
        "valueFormatter": {"function": f"d3.timeFormat('%Y-%m')({date_obj})"},
        # "sortable": True,
        "field": "OrderDate",
        "unSortIcon": True,
        # "filter": "agDateColumnFilter",
    
    },
    {
        "headerName": "Region",
        "field": "Region",
    },
    {
        "headerName": "Total Sales",
        "field": "Total Sales",
        "editable": True, # Only this column is editable
        "filter": "agNumberColumnFilter",
    },
]
def tab3():
    tab3_content = html.Div(children=[
    dbc.Card(
        dbc.CardBody([    
            html.Div(children=[   
                html.Div(children=[
                    html.Div(children=[          
                        dcc.DatePickerRange(
                            id="date picker",
                            min_date_allowed=aw_data["OrderDate"].min(),
                            max_date_allowed=aw_data["OrderDate"].max(),
                            initial_visible_month=aw_data["OrderDate"].min(),
                            start_date=aw_data["OrderDate"].min(),
                            end_date=aw_data["OrderDate"].max(),
                            style={"backgroundColor": "#333333", "color": "#FFFFFF"},
                        ),
                        dcc.Dropdown(
                            id="color dropdown",
                            options=[{"label": i.capitalize(), "value": i} for i in ["red", "lightgreen", "lightblue", "lightgrey"]],
                            value="lightgrey",
                            style={"backgroundColor": "#FFFFFF", "color": "black", "width": "250px", "marginTop": "10px"},  # Dark styling
                        ),
                        dcc.RadioItems(
                            id="metric radio",
                            options=[{"label": i, "value": i} for i in ["sum", "mean", "median", "min", "max"]],
                            value="sum",
                            style={"backgroundColor": "#1E1E1E", "color": "#FFFFFF", "marginTop": "10px"},
                            inline=False  
                        ),
                        dcc.Graph(id="graph"),
                    ],),

                    html.Div(children=[
                            dcc.Input(id="quick-filter-input", placeholder="filter...", style={"marginBottom": "5px"}),
                            dag.AgGrid(
                            id="aggrid_2",
                            className="ag-theme-alpine-dark",
                            rowData=aw_data.to_dict("records"),
                            columnDefs=columnDefs,
                            defaultColDef={"flex": 1, "cellClass": "align-right", "enableCellChangeFlash": True, "filter": "agTextColumnFilter"},
                            dashGridOptions = {'quickFilterText': ''},
                            style={"height": "100%", "width": "100%"}
                            ),
                    ],style={"width": "50%"},),
                ],style={"display": "flex"},),
                dcc.Graph(id="graph2",style={"width": "100%"},),
            ],
            style={"backgroundColor": "#1E1E1E", "color": "#FFFFFF", "padding": "20px"},
            ) 
        ]),
        className="mt-3",
        ),
        # Button and collapsable component for showing code.
        html.Div(children=
        [
            dbc.Button("Show code", id="collapse-button03", color="success", outline=True, style={"width": "500px", "margin": "auto"}),
            dbc.Collapse(
                dbc.Card(dbc.CardBody(
                    html.Img(src=r'assets/code03.jpg', alt='image',
                            style={"width": "90vw"}
                                ),style={"margin": "auto"}
                )),
                id="collapse03",
                is_open=False,
            ),
        ],
        style={"width": "100%"},
        className="d-grid gap-2 col-6 mx-auto mt-5",
        )
    ])   
    return tab3_content


# Callback for handling collapsable component, returns True/False depending on state of is_open
@callback(
    Output("collapse03", "is_open"),
    Input("collapse-button03", "n_clicks"),
    [State("collapse03", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Filter the ag grid
@callback(
    Output("aggrid_2", "dashGridOptions"),
    Input("quick-filter-input", "value"),
    prevent_initial_call=True,
)
def update_filter(filter_value):
    new_grid_option = Patch() # This is used to update only one targeted thing, if there is more grid options.
    new_grid_option['quickFilterText'] = filter_value
    return new_grid_option

# Callback for updating graphs, triggered by cellchanged or dropdown etc.
@callback(
    Output("graph", "figure"), 
    Output("graph2", "figure"), 
    [Input("date picker", "start_date"), Input("date picker", "end_date")],
    Input("metric radio", "value"),
    Input("color dropdown", "value"),
    Input("aggrid_2", "cellValueChanged"),
    State("aggrid_2", "rowData"), # This keeps the rowdata ready to use.
)
def plots(start_date, end_date, metric, color, n, rowData): 
    aw_data = pd.DataFrame.from_dict(rowData) # makes dataframe from the dict rowdata
    df = aw_data.loc[aw_data["OrderDate"].between(start_date, end_date)] # Filter data by date range
    
    # Plotly express bar chart
    fig = px.bar(
        (df
         .groupby("Region", as_index=False)
         .agg({"Total Sales": metric}) # Aggregate with metric input from radio button.
        )
        ,
        x="Total Sales",
        y="Region",
        title=f"Total monthly sales in regions between {start_date[:10]} and {end_date[:10]}"
    ).update_traces(marker_color=color) # Use color from dropdown input value
    fig.update_layout(template="plotly_dark", # Dark styling
                      paper_bgcolor="#1E1E1E",
                      plot_bgcolor="#222628")
    # Plotly express line chart
    fig2 = px.line(
        df,
        x="OrderDate",
        y="Total Sales",
        color="Region", # This groups the data by unique values in the region column, making multiple lines.,
        labels={
        "OrderDate": "Order Date",
        "line_style": "Line Type"}
    )
    fig2.update_layout(template="plotly_dark",
                      paper_bgcolor="#1E1E1E",
                      plot_bgcolor="#181D1F")
    
    return fig , fig2 # return the charts.