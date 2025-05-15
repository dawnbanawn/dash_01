import dash
from dash import html
import dash_bootstrap_components as dbc
# Import module content
# from Pages.page01 import tab1
# from Pages.page02 import tab2
from Pages.page03 import tab3
from Pages.page04 import tab4
from Pages.pageA import tabA

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# application = app.server
# App layout with tabs and functions calling the imported content.
# The hidden tabs are practice examples that I in the end didn´t think had a place here.
# app.layout = html.Div(
#     [
#         dbc.Tabs([
#             dbc.Tab(tabA(), label="Intro", activeLabelClassName="text-success"),
#             # dbc.Tab(tab1(), label="Example: Dash with callback", activeLabelClassName="text-success"),
#             # dbc.Tab(tab2(), label="Example: Ag grid with grid api", activeLabelClassName="text-success"),
#             dbc.Tab(tab3(), label="Fetched Data Visualized", activeLabelClassName="text-success"),
#             dbc.Tab(tab4(), label="Fetched Actual & Predicted Data", activeLabelClassName="text-success"),
#         ]),
#     ], style={"marginTop": "10px", "marginLeft": "10px", "marginRight": "10px", "position": "sticky"}
# )

app.layout = html.Div([
    dbc.Tabs([
        dbc.Tab(tabA(), label="Intro", activeLabelClassName="text-success"),
        dbc.Tab(tab3(), label="Original Data Visualized", activeLabelClassName="text-success"),
        dbc.Tab(tab4(), label="Original & Predicted Data Visualized", activeLabelClassName="text-success"),
    ], 
    style={"position": "sticky", "top": "0", "backgroundColor": "#343a40", "zIndex": "1000"}
    ),
    html.Div([
        # Your tab content goes here
    ], style={"height": "500px", "overflowY": "auto", "padding": "10px"})
])




if __name__ == '__main__':
    app.run(debug=False)

# if __name__ == "__main__":
#     app.run_server(host='0.0.0.0', debug=False)