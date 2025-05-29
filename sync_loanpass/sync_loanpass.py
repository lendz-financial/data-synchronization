import pyodbc
import datetime
from decimal import Decimal
import json
import sys
import requests # Import the requests library for making HTTP requests

# --- 1. Database Connection String ---
# IMPORTANT: Replace this placeholder with your actual Azure SQL Server connection string.
# For production, use environment variables or a secure secrets management solution
# (e.g., Azure Key Vault) instead of hardcoding credentials.
CONNECTION_STRING = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:lendz.database.windows.net,1433;Database=Lexi_DEV;Uid=lexi;Pwd=H3n4y*_D@;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# --- 2. LoanPASS API Configuration ---
LOANPASS_API_TOKEN = "hdzuN0bgsYcCdp4JM8HOFQ4mbJn8l6"

# Endpoints
LOANPASS_SUMMARY_API_ENDPOINT = "https://api.loanpass.io/v1/execute-summary"
LOANPASS_PRODUCT_API_ENDPOINT = "https://api.loanpass.io/v1/execute-product"

# --- 3. JSON Data Structures for API Calls ---
# Template for the initial /execute-summary API call
loanpass_summary_api_request_template = {
    "currentTime": None, # This will be replaced dynamically
    "pricingProfileId": "291",
    "creditApplicationFields": [],
    "publishedVersionRequest": {
        "type": "current"
    },
    "pipelineRecordId": None,
    "engine": "original",
    "bypassWorstCase": False
}

# Template for the subsequent /execute-product API calls
loanpass_product_api_request_template = {
    "currentTime": None, # This will be replaced dynamically
    "productId": None,   # This will be replaced dynamically for each product
    "pricingProfileId": "291",
    "creditApplicationFields": [],
    "outputFieldsFilter": {
        "type": "all"
    },
    "publishedVersionRequest": {
        "type": "current"
    },
    "pipelineRecordId": None,
    "engine": "original",
    "bypassWorstCase": False
}


def get_db_connection(conn_str):
    """Establishes and returns a pyodbc connection to the SQL Server database."""
    return pyodbc.connect(conn_str, autocommit=False) # Use autocommit=False for manual transaction control

def call_loanpass_api(endpoint, json_data_for_api):
    """
    Generic function to call a LoanPASS API endpoint with the provided JSON data.
    """
    headers = {
        "Authorization": f"Bearer {LOANPASS_API_TOKEN}",
        "Content-Type": "application/json"
    }

    print(f"\nCalling LoanPASS API: {endpoint}")
    print(f"Request Payload: {json.dumps(json_data_for_api, indent=2)}") # Un-commented for logging
    try:
        response = requests.post(endpoint, headers=headers, json=json_data_for_api, timeout=60) # Increased timeout
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        print(f"LoanPASS API call successful. Status Code: {response.status_code}")
        api_response_json = response.json()
        print("API Response JSON received.")
        print(f"API Response: {json.dumps(api_response_json, indent=2)}") # Added for logging API response
        return api_response_json # Return the JSON response from the API
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred during API call to {endpoint}: {http_err}")
        print(f"Response content: {response.text}")
        raise # Re-raise the exception to be caught by the main processing logic
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred during API call to {endpoint}: {conn_err}")
        raise
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout occurred during API call to {endpoint}: {timeout_err}")
        raise
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred during API call to {endpoint}: {req_err}")
        raise
    except json.JSONDecodeError as json_err:
        print(f"Error decoding JSON response from API {endpoint}: {json_err}")
        print(f"Raw response content: {response.text}")
        raise


def insert_product_offering(cursor, data):
    """
    Inserts or updates data into LoanPASS_Product_Offerings and returns the generated Id.
    It checks for an existing record based on Product_Id__c.
    """
    # Map JSON fields to SQL columns
    # This mapping assumes 'data' contains the product offering details
    # similar to the original large JSON structure.
    name = data.get("productName") # Using productName as Name
    product_id_c = data.get("productId")
    product_name_c = data.get("productName")
    product_code_c = data.get("productCode")
    investor_name_c = data.get("investorName")
    investor_code_c = data.get("investorCode")
    is_pricing_enabled_c = data.get("isPricingEnabled")
    status_c = data.get("status")
    rate_sheet_effective_timestamp_c = None
    if data.get("rateSheetEffectiveTimestamp"):
        # Convert ISO 8601 string to datetime object
        rate_sheet_effective_timestamp_c = datetime.datetime.fromisoformat(
            data["rateSheetEffectiveTimestamp"].replace('Z', '+00:00')
        )

    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    is_deleted = 0 # Default value for new inserts, can be updated for existing records if needed

    product_offering_id = None

    # First, check if a record with this Product_Id__c already exists
    check_sql = "SELECT Id FROM LoanPASS_Product_Offerings WHERE Product_Id__c = ?;"
    cursor.execute(check_sql, product_id_c)
    existing_record = cursor.fetchone()

    if existing_record:
        # Record exists, perform an UPDATE
        product_offering_id = existing_record[0]
        print(f"Updating existing Product Offering with Id: {product_offering_id} (Product_Id__c: {product_id_c})")
        update_sql = """
        UPDATE LoanPASS_Product_Offerings
        SET
            Name = ?,
            LastModifiedDate = ?,
            Product_Name__c = ?,
            Product_Code__c = ?,
            Investor_Name__c = ?,
            Investor_Code__c = ?,
            Is_Pricing_Enabled__c = ?,
            Status__c = ?,
            Rate_Sheet_Effective_Timestamp__c = ?
        OUTPUT INSERTED.Id
        WHERE Product_Id__c = ?;
        """
        update_params = (
            name, current_utc_time,
            product_name_c, product_code_c,
            investor_name_c, investor_code_c, is_pricing_enabled_c,
            status_c, rate_sheet_effective_timestamp_c,
            product_id_c # WHERE clause parameter
        )
        cursor.execute(update_sql, update_params)
        product_offering_id = cursor.fetchone()[0] # Get the Id again from OUTPUT INSERTED.Id
    else:
        # Record does not exist, perform an INSERT
        print(f"Inserting new Product Offering with Product_Id__c: {product_id_c}")
        insert_sql = """
        INSERT INTO LoanPASS_Product_Offerings (
            Name, CreatedDate, LastModifiedDate, IsDeleted,
            Product_Id__c, Product_Name__c, Product_Code__c,
            Investor_Name__c, Investor_Code__c, Is_Pricing_Enabled__c,
            Status__c, Rate_Sheet_Effective_Timestamp__c
        )
        OUTPUT INSERTED.Id
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        insert_params = (
            name, current_utc_time, current_utc_time, is_deleted,
            product_id_c, product_name_c, product_code_c,
            investor_name_c, investor_code_c, is_pricing_enabled_c,
            status_c, rate_sheet_effective_timestamp_c
        )
        cursor.execute(insert_sql, insert_params)
        product_offering_id = cursor.fetchone()[0]

    print(f"Operation completed for Product Offering. Final Id: {product_offering_id}")
    return product_offering_id

def insert_product_calculated_fields(cursor, product_offering_id, calculated_fields_data):
    """
    Inserts data into LoanPASS_Product_Calculated_Fields.
    """
    if not calculated_fields_data:
        return

    sql = """
    INSERT INTO LoanPASS_Product_Calculated_Fields (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Product_Offering_Id, Field_Id__c, Value_Type__c,
        Enum_Type_Id__c, Variant_Id__c, Number_Value__c,
        String_Value__c, Duration_Count__c, Duration_Unit__c
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    is_deleted = 0

    for field in calculated_fields_data:
        field_id = field.get("fieldId")
        value_data = field.get("value")

        value_type = value_data.get("type") if value_data else None
        enum_type_id = value_data.get("enumTypeId") if value_data and value_data.get("type") == "enum" else None
        variant_id = value_data.get("variantId") if value_data and value_data.get("type") == "enum" else None
        number_value = None
        string_value = None
        duration_count = None
        duration_unit = None

        if value_data:
            if value_type == "number" and value_data.get("value") is not None:
                number_value = Decimal(value_data["value"])
            elif value_type == "string" and value_data.get("value") is not None:
                string_value = str(value_data["value"])
            elif value_type == "duration":
                if value_data.get("count") is not None:
                    duration_count = Decimal(value_data["count"]) # DECIMAL(18,0)
                if value_data.get("unit") is not None:
                    duration_unit = str(value_data["unit"])

        params = (
            field_id, current_utc_time, current_utc_time, is_deleted,
            product_offering_id, field_id, value_type,
            enum_type_id, variant_id, number_value,
            string_value, duration_count, duration_unit
        )
        cursor.execute(sql, params)
    print(f"Inserted {len(calculated_fields_data)} Product Calculated Fields for Product Offering Id: {product_offering_id}")


def insert_price_scenario(cursor, product_offering_id, scenario_data):
    """
    Inserts data into LoanPASS_Price_Scenarios and returns the generated Id.
    """
    # Map JSON fields to SQL columns
    name = scenario_data.get("id") # Using scenario 'id' as Name for now
    adjusted_rate = Decimal(scenario_data["adjustedRate"]) if scenario_data.get("adjustedRate") is not None else None
    adjusted_price = Decimal(scenario_data["adjustedPrice"]) if scenario_data.get("adjustedPrice") is not None else None

    adjusted_rate_lock_count = None
    adjusted_rate_lock_unit = None
    if scenario_data.get("adjustedRateLockPeriod"):
        if scenario_data["adjustedRateLockPeriod"].get("count") is not None:
            adjusted_rate_lock_count = Decimal(scenario_data["adjustedRateLockPeriod"]["count"])
        if scenario_data["adjustedRateLockPeriod"].get("unit") is not None:
            adjusted_rate_lock_unit = scenario_data["adjustedRateLockPeriod"]["unit"]

    undiscounted_rate = Decimal(scenario_data["undiscountedRate"]) if scenario_data.get("undiscountedRate") is not None else None
    starting_adjusted_rate = Decimal(scenario_data["startingAdjustedRate"]) if scenario_data.get("startingAdjustedRate") is not None else None
    starting_adjusted_price = Decimal(scenario_data["startingAdjustedPrice"]) if scenario_data.get("startingAdjustedPrice") is not None else None
    status_c = scenario_data.get("status")

    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    is_deleted = 0

    sql = """
    INSERT INTO LoanPASS_Price_Scenarios (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Product_Offering_Id, Adjusted_Rate__c, Adjusted_Price__c,
        Adjusted_Rate_Lock_Count__c, Adjusted_Rate_Lock_Unit__c,
        Undiscounted_Rate__c, Starting_Adjusted_Rate__c,
        Starting_Adjusted_Price__c, Status__c
    )
    OUTPUT INSERTED.Id
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    params = (
        name, current_utc_time, current_utc_time, is_deleted,
        product_offering_id, adjusted_rate, adjusted_price,
        adjusted_rate_lock_count, adjusted_rate_lock_unit,
        undiscounted_rate, starting_adjusted_rate,
        starting_adjusted_price, status_c
    )

    cursor.execute(sql, params)
    price_scenario_id = cursor.fetchone()[0]
    print(f"  Inserted Price Scenario with Id: {price_scenario_id}")
    return price_scenario_id

def insert_price_scenario_calculated_fields(cursor, price_scenario_id, calculated_fields_data):
    """
    Inserts data into LoanPASS_Price_Scenario_Calculated_Fields.
    """
    if not calculated_fields_data:
        return

    sql = """
    INSERT INTO LoanPASS_Price_Scenario_Calculated_Fields (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Field_Id__c, Value_Type__c,
        Enum_Type_Id__c, Variant_Id__c, Number_Value__c,
        String_Value__c, Duration_Count__c, Duration_Unit__c
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    is_deleted = 0

    for field in calculated_fields_data:
        field_id = field.get("fieldId")
        value_data = field.get("value")

        value_type = value_data.get("type") if value_data else None
        enum_type_id = value_data.get("enumTypeId") if value_data and value_data.get("type") == "enum" else None
        variant_id = value_data.get("variantId") if value_data and value_data.get("type") == "enum" else None
        number_value = None
        string_value = None
        duration_count = None
        duration_unit = None

        if value_data:
            if value_type == "number" and value_data.get("value") is not None:
                number_value = Decimal(value_data["value"])
            elif value_type == "string" and value_data.get("value") is not None:
                string_value = str(value_data["value"])
            elif value_type == "duration":
                if value_data.get("count") is not None:
                    duration_count = Decimal(value_data["count"])
                if value_data.get("unit") is not None:
                    duration_unit = str(value_data["unit"])

        params = (
            field_id, current_utc_time, current_utc_time, is_deleted,
            price_scenario_id, field_id, value_type,
            enum_type_id, variant_id, number_value,
            string_value, duration_count, duration_unit
        )
        cursor.execute(sql, params)
    print(f"    Inserted {len(calculated_fields_data)} Price Scenario Calculated Fields for Scenario Id: {price_scenario_id}")


def insert_price_scenario_errors(cursor, price_scenario_id, errors_data):
    """
    Inserts data into LoanPASS_Price_Scenario_Errors.
    """
    if not errors_data:
        return

    sql = """
    INSERT INTO LoanPASS_Price_Scenario_Errors (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Source_Type__c, Source_Rule_Id__c,
        Error_Type__c, Error_Field_Id__c
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """
    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    is_deleted = 0

    for error in errors_data:
        source_data = error.get("source", {})
        source_type = source_data.get("type")
        source_rule_id = source_data.get("ruleId")
        error_type = error.get("type")
        error_field_id = error.get("fieldId")
        name = f"{error_type} - {error_field_id}" # Using a combination for Name

        params = (
            name, current_utc_time, current_utc_time, is_deleted,
            price_scenario_id, source_type, source_rule_id,
            error_type, error_field_id
        )
        cursor.execute(sql, params)
    print(f"    Inserted {len(errors_data)} Price Scenario Errors for Scenario Id: {price_scenario_id}")


def process_loan_pass_data():
    """
    Orchestrates the process:
    1. Calls the /execute-summary API to get a list of products.
    2. For each product, calls the /execute-product API to get detailed data.
    3. Inserts/updates the detailed product data into the database tables.
    Handles transactions for atomicity.
    """
    conn = None
    try:
        # --- 1. Prepare and Call /execute-summary API ---
        summary_request_data = loanpass_summary_api_request_template.copy()
        summary_request_data["currentTime"] = datetime.datetime.now().astimezone().isoformat()

        summary_response = call_loanpass_api(LOANPASS_SUMMARY_API_ENDPOINT, summary_request_data)

        if not summary_response or "products" not in summary_response:
            print("Summary API response was empty or missing 'products' key. Aborting database operations.")
            return

        products_list = summary_response["products"]
        if not products_list:
            print("No products found in the summary API response. Aborting database operations.")
            return

        print(f"Found {len(products_list)} products from summary API. Proceeding to fetch details and insert.")

        # Establish database connection once for all product insertions
        conn = get_db_connection(CONNECTION_STRING)
        cursor = conn.cursor()

        # --- 2. Iterate through products and call /execute-product API for each ---
        for product_summary in products_list:
            product_id_to_fetch = product_summary.get("productId")
            if not product_id_to_fetch:
                print(f"Skipping product due to missing 'productId' in summary: {product_summary}")
                continue

            print(f"\n--- Processing Product ID: {product_id_to_fetch} ---")

            # Prepare payload for /execute-product API
            product_detail_request_data = loanpass_product_api_request_template.copy()
            product_detail_request_data["currentTime"] = datetime.datetime.now().astimezone().isoformat()
            product_detail_request_data["productId"] = product_id_to_fetch

            try:
                # Call /execute-product API for detailed product data
                product_details_response = call_loanpass_api(LOANPASS_PRODUCT_API_ENDPOINT, product_detail_request_data)

                # IMPORTANT ASSUMPTION:
                # We assume 'product_details_response' has the structure needed for DB insertion.
                # If the actual API response structure is different, you will need to
                # transform 'product_details_response' into the expected database-friendly format here.
                data_for_db_insertion = product_details_response

                if not data_for_db_insertion:
                    print(f"No detailed data received for Product ID {product_id_to_fetch}. Skipping database insertion for this product.")
                    continue

                # Start a transaction for each product's full data insertion
                # (Alternatively, you could have one large transaction for all products,
                # but per-product transactions are safer if one product fails)
                conn.autocommit = False # Ensure transaction is active

                # 1. Insert/Update into LoanPASS_Product_Offerings
                product_offering_id = insert_product_offering(cursor, data_for_db_insertion)

                # 2. Insert into LoanPASS_Product_Calculated_Fields
                if "calculatedFields" in data_for_db_insertion:
                    insert_product_calculated_fields(cursor, product_offering_id, data_for_db_insertion["calculatedFields"])

                # 3. Process Price Scenarios and their nested data
                if "priceScenarios" in data_for_db_insertion:
                    for scenario in data_for_db_insertion["priceScenarios"]:
                        price_scenario_id = insert_price_scenario(cursor, product_offering_id, scenario)

                        # Insert into LoanPASS_Price_Scenario_Calculated_Fields
                        if "calculatedFields" in scenario:
                            insert_price_scenario_calculated_fields(cursor, price_scenario_id, scenario["calculatedFields"])

                        # Insert into LoanPASS_Price_Scenario_Errors
                        if "errors" in scenario:
                            insert_price_scenario_errors(cursor, price_scenario_id, scenario["errors"])

                # Commit the transaction for this product if all operations are successful
                conn.commit()
                print(f"Successfully inserted/updated data for Product ID: {product_id_to_fetch}")

            except (requests.exceptions.RequestException, pyodbc.Error, json.JSONDecodeError) as e:
                print(f"Error processing Product ID {product_id_to_fetch}: {e}")
                if conn:
                    conn.rollback() # Rollback current product's transaction on error
                    print(f"Transaction rolled back for Product ID: {product_id_to_fetch}.")
                # Continue to the next product even if one fails
                continue

    except requests.exceptions.RequestException as e:
        print(f"\nInitial API Call Error: {e}")
        # No database rollback needed here as no transaction was started or committed
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"\nDatabase Error (during initial setup or outer loop): {sqlstate}")
        print(f"Error details: {ex.args[1]}")
        if conn:
            conn.rollback() # Rollback any open transaction if error occurred outside per-product loop
            print("Database transaction rolled back due to outer error.")
    except Exception as e:
        print(f"\nAn unexpected error occurred (outer loop): {e}")
        if conn:
            conn.rollback() # Rollback on unexpected error during database operations
            print("Database transaction rolled back due to unexpected outer error.")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

# --- Main Execution ---
if __name__ == "__main__":
    # No need to load JSON from command line anymore, as the script now fetches it from API.
    # The command line argument for JSON file path is no longer used.
    if len(sys.argv) > 1:
        print("Note: Command-line argument for JSON file path is no longer used. Data is fetched from LoanPASS API.")

    print("Starting data processing and API calls...")
    process_loan_pass_data()
    print("Process finished.")
