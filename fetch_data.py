import requests
import json
import time 
import pandas as pd
import os 
# importing necessary functions from dotenv library
from dotenv import load_dotenv

load_dotenv()  # take environment variables

# Function to get data, actual or predicted.
def getData(typeOfData):
    sql_query = ""
    column_names = []
    csv_filename = ""

    if (typeOfData == "actual"):
        # Query to get actual sales data
        # Joins the tables by their IDs, groups by Region and Month, and sums the sales.
        sql_query = """
        SELECT 
        DATE_FORMAT(soh.OrderDate, 'yyyy-MM') AS OrderMonth, 
        st.Name AS Region, 
        CAST(ROUND(SUM(sod.LineTotal), 2) AS DECIMAL(18, 2)) AS TotalSales
        FROM dan_endtoend_db.default.salesorderheader AS soh
        INNER JOIN dan_endtoend_db.default.salesorderdetail AS sod ON soh.SalesOrderID = sod.SalesOrderID
        INNER JOIN dan_endtoend_db.default.salesterritory AS st ON soh.TerritoryID = st.TerritoryID
        WHERE YEAR(soh.OrderDate) IN (2012, 2013)
        GROUP BY DATE_FORMAT(soh.OrderDate, 'yyyy-MM'), st.Name
        ORDER BY OrderMonth, st.Name;
        """
        column_names = ["OrderDate", "Region", "Total Sales"]
        csv_filename = os.path.join(os.getcwd(), "sales_data.csv")

    elif(typeOfData == "predicted"):  
        # Query to get predicted data
        sql_query = """
        SELECT * FROM dan_endtoend_db.default.predicted_sales_by_region;
        """
        column_names = ["date", "mean", "mean_ci_lower", "mean_ci_upper", "Region"] 
        csv_filename = os.path.join(os.getcwd(), "sales_data_predict.csv")


    # Databricks API configuration
    databricks_url = os.getenv('DATABRICKS_URL')
    api_token = os.getenv('API_TOKEN')

    # API Request to submit query
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    data = {
        "statement": sql_query,
        "warehouse_id": os.getenv('WAREHOUSE_ID'),
        "catalog": os.getenv('CATALOG'),
        "format": "JSON"
    }

    # recieve the post response from databricks
    response = requests.post(databricks_url, headers=headers, json=data)

    # Check status, and try to save the respones. 
    # Copilot helped with many of the checks here.
    if response.status_code == 200:
        statement_id = response.json().get("statement_id")
        print(f"Query submitted successfully! Statement ID: {statement_id}")

        # Poll for query status until results are ready
        status_url = f"https://adb-3574350398571093.13.azuredatabricks.net/api/2.0/sql/statements/{statement_id}"

        while True:
            status_response = requests.get(status_url, headers=headers) # Fetch the status
            status_result = status_response.json()
            current_state = status_result["status"]["state"]
            print(f"Current Status: {current_state}")

            if current_state == "RUNNING":
                time.sleep(2)  # Wait a bit and poll again
            elif current_state == "SUCCEEDED":
                print("Query completed! Saving results to CSV...")
                # Extract result set from API response
                result_data = status_result.get("result", {}).get("data_array", [])
                if result_data:
                    # Convert result into a Pandas DataFrame, with column names
                    df = pd.DataFrame(result_data, columns=column_names)
                    try:
                        df.to_csv(csv_filename, index=False) # Save the file
                        print(f"Data saved successfully as '{csv_filename}'!")
                    except Exception as e:
                        print(f"Error saving CSV: {e}")
                break
    else:
        print(f"Error {response.status_code}: {response.text}")

# There is no point connecting this to page load since there is no compute/new data.
getData("predicted")