from dash import html, Input, Output, callback, State
import dash_bootstrap_components as dbc

# Returns an input with callback
def tabA():
    tab1_content = html.Div(children=[
        dbc.Card( # This adds some styling, padding
                    dbc.CardBody([
                        html.Div(children = [
                            html.H1("End-to-end Application", style={"marginBottom": "25px", "marginTop": "-70px"}),
                            html.H3("Creating a pipeline for data analysis ", style={"marginBottom": "40px"}),
                            
                            html.Div("Data is important in the decision making of organizations. Data by itself is however not necessarily useful without some preparation, and for the data to reach this stage, it may require several steps of data ingestion, transforming and presentation."),
                            html.Div("",style={"marginBottom": "20px"}),

                            html.Div("The goal of this rapport was to develop an end-to-end analysis pipeline with realistic data, and to reach this goal the following questions would be answered: "),
                            html.Div("",style={"marginBottom": "20px"}),
                            html.Div("1.	Can we develop an E2E pipeline with SQL server, Azure, Python, Dash and Plotly."),
                            html.Div("2.	Can we use the pipeline with realistic data, and present the realistic data with data visualizations."),
                            html.Div("",style={"marginBottom": "20px"}),
                                                        html.Div("The answers is yes and yes. "),
                            html.Div("",style={"marginBottom": "20px"}),
                            html.Div("I decided to use SQL Server, Azure Data Factory, Data Lake Storage, Databricks, SQL, Python, Dash and Plotly to create this pipeline."),
                            html.Div("",style={"marginBottom": "20px"}),
                            # Layout with image and modal
                                html.Div([
                                    # The image that triggers the modal
                                    html.Img(
                                        src=r'assets/pipeline_logos.jpg',
                                        alt="Thumbnail",
                                        id="clickable-image",  # Assign an ID to the image
                                        style={"width": "70vw","marginBottom": "50px", "cursor": "pointer"}
                                    ),
                                    # Modal to display the original image
                                    dbc.Modal(
                                        [
                                            dbc.ModalBody(
                                                html.Img(
                                                    src=r'assets/pipeline_logos.jpg',  # Full-sized image in the modal
                                                    style={"width": "100%"}  # Ensure it scales nicely
                                                ),)
                                        ],
                                        id="image-modal",  # ID for the modal
                                        is_open=False,  # Initial state is closed
                                        size="xl",
                                    )
                                ],
                                ),







                           html.Div("For realistic data I used Microsofts Adventure Works database, here imported into SSMS in my local computer."),
                            html.Div("",style={"marginBottom": "20px"}),

                                html.Img(
                                        src=r'assets/ssms_aw_database.jpg',
                                        alt="Thumbnail",
                                        # id="clickable-image",  # Assign an ID to the image
                                        style={"width": "70vw","marginBottom": "50px", "cursor": "pointer"}
                                    ),
                                    

                           html.Div("I created the resource group I needed in Azure."),
                            html.Div("",style={"marginBottom": "20px"}),

                                html.Img(
                                        src=r'assets/Azure_resource_group.jpg',
                                        alt="Thumbnail",
                                        # id="clickable-image",  # Assign an ID to the image
                                        style={"width": "70vw","marginBottom": "50px", "cursor": "pointer"}
                                    ),

                           html.Div("I wanted to work with total sales per region over time, so I used SQL in SSMS to see what tables I needed. I then used Data Factory to transfer three chosen tables from SQL Server to Azure Data Lake Storage V2."),
                            html.Div("",style={"marginBottom": "20px"}),

                                html.Img(
                                        src=r'assets/DataFactory.jpg',
                                        alt="Thumbnail",
                                        # id="clickable-image",  # Assign an ID to the image
                                        style={"width": "70vw","marginBottom": "50px", "cursor": "pointer"}
                                    ),

                           html.Div("The chosen data are were saved as .csv files in a bronze layer on Datalake Storage v2, using medallion architecture."),
                            html.Div("",style={"marginBottom": "20px"}),

                                html.Img(
                                        src=r'assets/DatalakeStoragev2.jpg',
                                        alt="Thumbnail",
                                        # id="clickable-image",  # Assign an ID to the image
                                        style={"width": "70vw","marginBottom": "50px", "cursor": "pointer"}
                                    ),

                           html.Div("I connected to Databricks using a keyvault, and loaded the data into Databricks from the bronze layer."),
                            html.Div("",style={"marginBottom": "20px"}),

                                html.Img(
                                        src=r'assets/Load_and_save_tables_in_databricks.jpg',
                                        alt="Thumbnail",
                                        # id="clickable-image",  # Assign an ID to the image
                                        style={"width": "70vw","marginBottom": "50px", "cursor": "pointer"}
                                    ),

                           html.Div("In Databricks I joined the data, trained SARIMAX forecast models, one for each region, and made predictions with them."),
                           
                            html.Div("",style={"marginBottom": "20px"}),

                                html.Img(
                                        src=r'assets/model_training_in_databricks_V2.jpg',
                                        alt="Thumbnail",
                                        # id="clickable-image",  # Assign an ID to the image
                                        style={"width": "70vw","marginBottom": "50px", "cursor": "pointer"}
                                    ),

                           html.Div("I didn´t spend too much time training the best possible models by, for example, finding the best hyperparameters, because that wasn´t the focus of this project, and there is a cost factor to consider while using resources when making this type of pipeline."),

                            html.Div("",style={"marginBottom": "20px"}),

                                html.Img(
                                        src=r'assets/Azure_cost.jpg',
                                        alt="Thumbnail",
                                        # id="clickable-image",  # Assign an ID to the image
                                        style={"width": "70vw","marginBottom": "50px", "cursor": "pointer"}
                                    ),
                           html.Div("Four months of predictions were saved to a silver layer in Data Lake Storage V2."),
                            html.Div("",style={"marginBottom": "20px"}),

                                html.Img(
                                        src=r'assets/storage_silver.jpg',
                                        alt="Thumbnail",
                                        # id="clickable-image",  # Assign an ID to the image
                                        style={"width": "70vw","marginBottom": "50px", "cursor": "pointer"}
                                    ),




                           html.Div("With a python script and SQL queries I fetched both original and predicted data to this dash app, as local .csv files. I then created the rest of this app to visualize the data."),
                            # html.Div("",style={"marginBottom": "20px"}),

                            #     html.Img(
                            #             src=r'assets/codeA - Copy.jpg',
                            #             alt="Thumbnail",
                            #             # id="clickable-image",  # Assign an ID to the image
                            #             style={"width": "70vw","marginBottom": "50px", "cursor": "pointer"}
                            #         ),
                        #    html.Div(""),
                            html.Div("",style={"marginBottom": "20px"}),
                           html.Div("There are plenty of ways to improve this pipeline, tables can be joined earlier, there are ways to transfer data directly from SQL Server into Databricks removing the need for Data Factory, Microsoft Fabric has probably new ways to do this, and the ML can be improved in many ways, more EDA to find outliers, more granular data."),
                            html.Div("",style={"marginBottom": "20px"}),

                          ],
                            style={"display": "flex", "justifyContent": "center", "flexDirection": "column", "alignItems": "center", "margin": "100px"})
                    ],
                    style={"width": "100%", "display": "flex", "justifyContent": "center"}),
                    className="mt-3",                    
                ),




                
    ],
    )   
    return tab1_content





# Callback to toggle the modal
@callback(
    Output("image-modal", "is_open"),
    Input("clickable-image", "n_clicks"),
    State("image-modal", "is_open")
)
def toggle_modal(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open