import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

# Load data
actual_data = pd.read_csv("./sales_data.csv")
predicted_data = pd.read_csv("./sales_data_predict.csv")

# Convert 'ds' column in predicted data to match 'OrderDate' format Year and months
predicted_data["OrderDate"] = pd.to_datetime(predicted_data["ds"]).dt.strftime("%Y-%m")

# Rename predicted columns to match actual data columns
predicted_data.rename(columns={"mean": "Total Sales"}, inplace=True)
predicted_data = predicted_data[["OrderDate", "Region", "Total Sales"]]

# Extract the first 4 months of predicted data
first_three_months = predicted_data["OrderDate"].unique()[:4]
next_three_months = predicted_data[predicted_data["OrderDate"].isin(first_three_months)].reset_index(drop=True)

# Combine actual and predicted data into one dataframe, an option would be to load them separately into the same graph.
combined_data = pd.concat([actual_data, next_three_months], ignore_index=True)

# Create column line style, and add solid or dash depending on when predicted data starts.
# The lack of day-granularity creates a hole. Loading the data frames separately into the same graph didn´t solve this.
transition_date = pd.to_datetime(next_three_months["OrderDate"]).min().tz_localize(None)
combined_data["line_style"] = combined_data["OrderDate"].apply(lambda x: "solid" if pd.to_datetime(x) < transition_date else "solid")

def tab4():
    return html.Div([
        dcc.Input(id="hidden_input", style={"display": "none"}),
        html.H5("This is the original data and 4 months of predicted data, from ML training and forecasting made in Databricks, combined in a line graph.", 
                 style={"marginLeft": "50px", "marginTop": "50px"}),                 

        dcc.Graph(id="predictionGraph"),
                # Button and collapsable component for showing code.
        html.Div(children=
        [
            dbc.Button("Show code", id="collapse-button04", color="success", outline=True, style={"width": "500px", "margin": "auto"}),
            dbc.Collapse(
                dbc.Card(dbc.CardBody(
                    html.Img(src=r'assets/code04.jpg', alt='image',
                            style={"width": "90vw"}
                                ),style={"margin": "auto"}
                )),
                id="collapse04",
                is_open=False,
            ),
        ],
        style={"width": "100%"},
        className="d-grid gap-2 col-6 mx-auto mt-5",)
    ])

# Callback for updating the graph
@callback(
    Output("predictionGraph", "figure"), 
    Input("hidden_input", "value")
)
def plots(value): 
    fig = px.line(
        combined_data, 
        x="OrderDate", 
        y="Total Sales", 
        color="Region", 
        line_dash="line_style",
        title="Original and Predicted Total Sales",
        labels={
        "OrderDate": "Order Date",
        "line_style": "Line Type"
    }

    )   
    fig.add_vline(x="2013-12", line_width=2, line_dash="dash", line_color="white") # Vertical line to show where predicted data begins.
    fig.add_vrect(x0="2013-12", x1="2014-04", 
              annotation_text=" Predicted data", annotation_position="top left",
              fillcolor="green", opacity=0.25, line_width=0)
    fig.update_layout(template="plotly_dark",
                      paper_bgcolor="#1E1E1E",
                      plot_bgcolor="#181D1F")

    return fig

# Callback for handling collapsable component, returns True/False depending on state of is_open
@callback(
    Output("collapse04", "is_open"),
    Input("collapse-button04", "n_clicks"),
    [State("collapse04", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open