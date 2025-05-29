import pyodbc
import datetime
from decimal import Decimal
import json
import sys # Import the sys module to access command-line arguments

# --- 1. Database Connection String ---
# IMPORTANT: Replace this placeholder with your actual Azure SQL Server connection string.
# For production, use environment variables or a secure secrets management solution
# (e.g., Azure Key Vault) instead of hardcoding credentials.
# Changed Driver to ODBC Driver 17 for SQL Server
CONNECTION_STRING = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:lendz.database.windows.net,1433;Database=Lexi_DEV;Uid=lexi;Pwd=H3n4y*_D@;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

# --- 2. Sample JSON Data (Now loaded from command line) ---
# This variable will now be populated from the command line argument.
loan_pass_data_json = {} # Initialize as empty, will be overwritten

def get_db_connection(conn_str):
    """Establishes and returns a pyodbc connection to the SQL Server database."""
    return pyodbc.connect(conn_str, autocommit=False) # Use autocommit=False for manual transaction control

def insert_product_offering(cursor, data):
    """
    Inserts or updates data into LoanPASS_Product_Offerings and returns the generated Id.
    It checks for an existing record based on Product_Id__c.
    """
    # Map JSON fields to SQL columns
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


def process_loan_pass_data(data):
    """
    Processes the entire LoanPASS JSON object and inserts data into all related tables.
    Handles transactions for atomicity.
    """
    conn = None
    try:
        conn = get_db_connection(CONNECTION_STRING) # Pass the connection string
        cursor = conn.cursor()

        # Start a transaction
        conn.autocommit = False

        # 1. Insert into LoanPASS_Product_Offerings (now handles upsert)
        product_offering_id = insert_product_offering(cursor, data)

        # 2. Insert into LoanPASS_Product_Calculated_Fields
        # Note: For calculated fields and price scenarios, if you need to update existing
        # child records instead of always inserting new ones, you would need to implement
        # similar upsert logic (check for existence, then update or insert) based on a
        # unique identifier for these child records (e.g., a combination of FK and Field_Id__c).
        # This current implementation will always insert new calculated fields/scenarios/errors
        # for a given product offering or price scenario.
        if "calculatedFields" in data:
            insert_product_calculated_fields(cursor, product_offering_id, data["calculatedFields"])

        # 3. Process Price Scenarios and their nested data
        if "priceScenarios" in data:
            for scenario in data["priceScenarios"]:
                price_scenario_id = insert_price_scenario(cursor, product_offering_id, scenario)

                # Insert into LoanPASS_Price_Scenario_Calculated_Fields
                if "calculatedFields" in scenario:
                    insert_price_scenario_calculated_fields(cursor, price_scenario_id, scenario["calculatedFields"])

                # Insert into LoanPASS_Price_Scenario_Errors
                if "errors" in scenario:
                    insert_price_scenario_errors(cursor, price_scenario_id, scenario["errors"])

        # Commit the transaction if all inserts are successful
        conn.commit()
        print("\nAll data successfully inserted and committed.")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"\nDatabase Error: {sqlstate}")
        print(f"Error details: {ex.args[1]}")
        if conn:
            conn.rollback() # Rollback on error
            print("Transaction rolled back due to error.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        if conn:
            conn.rollback() # Rollback on error
            print("Transaction rolled back due to unexpected error.")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

# --- Main Execution ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python your_script_name.py <json_file_path>")
        print("Please provide the path to the JSON data file as a command-line argument.")
        sys.exit(1)

    json_file_path = sys.argv[1]
    try:
        with open(json_file_path, 'r') as f:
            loan_pass_data_json = json.load(f)
        print(f"JSON data loaded from file: {json_file_path} successfully.")
        process_loan_pass_data(loan_pass_data_json)
    except FileNotFoundError:
        print(f"Error: The file '{json_file_path}' was not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{json_file_path}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during processing: {e}")
        sys.exit(1)
