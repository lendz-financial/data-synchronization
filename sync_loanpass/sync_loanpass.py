import pyodbc
import json
from datetime import datetime, timezone
import os
import random # Import the random module for generating random integers
import requests
import uuid # Import uuid for generating unique run IDs
import sys 

# --- Database Connection Configuration ---
# IMPORTANT: Replace this with your actual SQL Server connection string.
# Example: "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=LoanPASS_DB;UID=your_username;PWD=your_password"
# For Windows Authentication: "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=LoanPASS_DB;Trusted_Connection=yes;"
# You might need to install the appropriate ODBC driver for SQL Server.
# For Windows: 'ODBC Driver 17 for SQL Server' is common.
# For Linux/macOS: Refer to Microsoft's documentation for ODBC drivers.

def get_db_connection(conn_str):
    """Establishes and returns a database connection using the provided connection string."""
    try:
        conn = pyodbc.connect(conn_str)
        conn.autocommit = False # Ensure transactions are managed manually
        print("Successfully connected to the database.")
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Database connection error: {sqlstate}")
        print(ex)
        raise

def parse_datetimeoffset(dt_str):
    """Parses a datetime string into a datetime object with timezone info."""
    if dt_str is None:
        return None
    # Handle 'Z' as UTC and ensure timezone awareness for fromisoformat
    try:
        if dt_str.endswith('Z'):
            dt_str = dt_str[:-1] + '+00:00'
        # datetime.fromisoformat can handle various ISO 8601 formats
        return datetime.fromisoformat(dt_str)
    except (ValueError, TypeError):
        print(f"Warning: Could not parse datetime string '{dt_str}'. Returning None.")
        return None

def extract_field_values(field_data):
    """
    Extracts values from a generic field object (productFields, calculatedFields)
    and maps them to the appropriate SQL columns.
    Handles cases where 'value' itself might be null.
    """
    value_obj = field_data.get('value') # Get the 'value' object, which can be None
    
    value_type = None
    number_value = None
    string_value = None
    duration_count = None
    duration_unit = None
    enum_type_id = None
    variant_id = None

    # Only proceed if value_obj is not None (i.e., not 'null' in JSON)
    if value_obj is not None:
        value_type = value_obj.get('type')

        if value_type == 'number':
            try:
                number_value = float(value_obj.get('value'))
            except (ValueError, TypeError):
                number_value = None
        elif value_type == 'string':
            string_value = value_obj.get('value')
        elif value_type == 'duration':
            try:
                duration_count = float(value_obj.get('count'))
            except (ValueError, TypeError):
                duration_count = None
            duration_unit = value_obj.get('unit')
        elif value_type == 'enum':
            enum_type_id = value_obj.get('enumTypeId')
            variant_id = value_obj.get('variantId')

    return {
        'Value_Type__c': value_type,
        'Number_Value__c': number_value,
        'String_Value__c': string_value,
        'Duration_Count__c': duration_count,
        'Duration_Unit__c': duration_unit,
        'Enum_Type_Id__c': enum_type_id,
        'Variant_Id__c': variant_id
    }


def insert_product_offering(cursor, product_data, run_id):
    """
    Inserts or updates data into dbo.LoanPASS_Product_Offerings (upsert)
    based on Product_Code__c and returns its Id.
    Includes Run_Id.
    """
    current_time = datetime.now(timezone.utc)
    name = product_data.get('productName', f"Product {product_data.get('productId', 'Unknown')}")
    product_id_c = product_data.get('productId')
    product_name_c = product_data.get('productName')
    product_code_c = product_data.get('productCode')
    investor_name_c = product_data.get('investorName')
    investor_code_c = product_data.get('investorCode')
    is_pricing_enabled_c = product_data.get('isPricingEnabled')
    status_c = product_data.get('status', {}).get('type')
    rate_sheet_effective_timestamp_c = parse_datetimeoffset(product_data.get('status', {}).get('rateSheetEffectiveTimestamp'))

    print(f"Upserting Product Offering for Product Code: {product_code_c}")

    # SQL MERGE statement for upsert, including Run_Id
    sql = """
    MERGE INTO dbo.LoanPASS_Product_Offerings AS target
    USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS source (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        Product_Id__c, Product_Name__c, Product_Code__c,
        Investor_Name__c, Investor_Code__c, Is_Pricing_Enabled__c,
        Status__c, Rate_Sheet_Effective_Timestamp__c, Run_Id
    )
    ON (target.Product_Code__c = source.Product_Code__c)
    WHEN MATCHED THEN
        UPDATE SET
            target.Name = source.Name,
            target.LastModifiedDate = ?, -- Use current_time for LastModifiedDate on update
            target.Product_Id__c = source.Product_Id__c,
            target.Product_Name__c = source.Product_Name__c,
            target.Investor_Name__c = source.Investor_Name__c,
            target.Investor_Code__c = source.Investor_Code__c,
            target.Is_Pricing_Enabled__c = source.Is_Pricing_Enabled__c,
            target.Status__c = source.Status__c,
            target.Rate_Sheet_Effective_Timestamp__c = source.Rate_Sheet_Effective_Timestamp__c,
            target.IsDeleted = source.IsDeleted, -- Also update IsDeleted if it changes
            target.Run_Id = source.Run_Id -- Update Run_Id
    WHEN NOT MATCHED THEN
        INSERT (
            Name, CreatedDate, LastModifiedDate, IsDeleted,
            Product_Id__c, Product_Name__c, Product_Code__c,
            Investor_Name__c, Investor_Code__c, Is_Pricing_Enabled__c,
            Status__c, Rate_Sheet_Effective_Timestamp__c, Run_Id
        )
        VALUES (
            source.Name, source.CreatedDate, source.LastModifiedDate, source.IsDeleted,
            source.Product_Id__c, source.Product_Name__c, source.Product_Code__c,
            source.Investor_Name__c, source.Investor_Code__c, source.Is_Pricing_Enabled__c,
            source.Status__c, source.Rate_Sheet_Effective_Timestamp__c, source.Run_Id
        )
    OUTPUT INSERTED.Id;
    """
    try:
        cursor.execute(
            sql,
            name,
            current_time, # CreatedDate for new insert
            current_time, # LastModifiedDate for new insert
            False,       # IsDeleted
            product_id_c,
            product_name_c,
            product_code_c,
            investor_name_c,
            investor_code_c,
            is_pricing_enabled_c,
            status_c,
            rate_sheet_effective_timestamp_c,
            str(run_id), # Run_Id for source
            current_time # LastModifiedDate for update
        )
        product_offering_id = cursor.fetchone()[0]
        print(f"Upserted Product Offering with Id: {product_offering_id}")
        return int(product_offering_id)
    except pyodbc.Error as ex:
        print(f"Error upserting Product Offering '{name}' (Code: {product_code_c}): {ex}")
        raise

def insert_product_calculated_fields(cursor, product_offering_id, product_fields_data, run_id, is_calculated=False):
    """
    Inserts data into dbo.LoanPASS_Product_Calculated_Fields.
    Can handle both 'productFields' and 'calculatedFields' from the top level.
    Includes Run_Id.
    """
    table_name = "dbo.LoanPASS_Product_Calculated_Fields"
    print(f"Inserting {'Calculated' if is_calculated else 'Product'} Fields for Product Offering Id: {product_offering_id}")
    sql = """
    INSERT INTO {} (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Product_Offering_Id, Field_Id__c, Value_Type__c,
        Enum_Type_Id__c, Variant_Id__c, Number_Value__c,
        String_Value__c, Duration_Count__c, Duration_Unit__c, Run_Id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """.format(table_name)

    current_time = datetime.now(timezone.utc)
    for field in product_fields_data:
        field_id = field.get('fieldId')
        name = field.get('Name', field_id) # Use Name if present, else fieldId

        extracted_values = extract_field_values(field)

        try:
            cursor.execute(
                sql,
                name,
                current_time,
                current_time,
                False,
                product_offering_id,
                field_id,
                extracted_values['Value_Type__c'],
                extracted_values['Enum_Type_Id__c'],
                extracted_values['Variant_Id__c'],
                extracted_values['Number_Value__c'],
                extracted_values['String_Value__c'],
                extracted_values['Duration_Count__c'],
                extracted_values['Duration_Unit__c'],
                str(run_id) # Run_Id
            )
            print(f"  Inserted Product {'Calculated' if is_calculated else ''} Field: {name}")
        except pyodbc.Error as ex:
            print(f"  Error inserting Product {'Calculated' if is_calculated else ''} Field '{name}': {ex}")
            raise

def insert_price_scenario(cursor, product_offering_id, scenario_data, run_id):
    """
    Inserts data into dbo.LoanPASS_Price_Scenarios and returns its Id.
    Includes Run_Id.
    """
    current_time = datetime.now(timezone.utc)
    scenario_business_id = scenario_data.get('id')
    name = scenario_data.get('Name', f"Scenario {scenario_business_id or 'Unknown'}")
    status_type = scenario_data.get('status', {}).get('type')

    # Extract values from priceScenarioFields
    adjusted_rate = None
    adjusted_price = None
    adjusted_rate_lock_count = None
    adjusted_rate_lock_unit = None

    for field in scenario_data.get('priceScenarioFields', []):
        if field.get('fieldId') == 'base-interest-rate':
            try:
                adjusted_rate = float(field.get('value', {}).get('value'))
            except (ValueError, TypeError):
                adjusted_rate = None
        elif field.get('fieldId') == 'base-price':
            try:
                adjusted_price = float(field.get('value', {}).get('value'))
            except (ValueError, TypeError):
                adjusted_price = None
        elif field.get('fieldId') == 'rate-lock-period':
            try:
                duration_count_str = field.get('value', {}).get('count')
                adjusted_rate_lock_count = float(duration_count_str) if duration_count_str is not None else None
            except (ValueError, TypeError):
                adjusted_rate_lock_count = None
            adjusted_rate_lock_unit = field.get('value', {}).get('unit')

    # Defensive assignment: provide default values if None, assuming DB columns are NOT NULL
    name = name if name is not None else '' # Ensure name is not None
    status_type = status_type if status_type is not None else ''
    scenario_business_id = scenario_business_id if scenario_business_id is not None else ''

    adjusted_rate = adjusted_rate if adjusted_rate is not None else 0.0
    adjusted_price = adjusted_price if adjusted_price is not None else 0.0
    adjusted_rate_lock_count = adjusted_rate_lock_count if adjusted_rate_lock_count is not None else 0.0
    adjusted_rate_lock_unit = adjusted_rate_lock_unit if adjusted_rate_lock_unit is not None else ''

    # Ensure dependent fields also get the defaulted values
    undiscounted_rate = adjusted_rate
    starting_adjusted_rate = adjusted_rate
    starting_adjusted_price = adjusted_price


    print(f"Inserting Price Scenario: {name}")
    sql = """
    INSERT INTO dbo.LoanPASS_Price_Scenarios (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Product_Offering_Id, Adjusted_Rate__c, Adjusted_Price__c,
        Adjusted_Rate_Lock_Count__c, Adjusted_Rate_Lock_Unit__c,
        Undiscounted_Rate__c, Starting_Adjusted_Rate__c,
        Starting_Adjusted_Price__c, Status__c, Scenario_Business_Id__c, Run_Id
    ) OUTPUT INSERTED.Id VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        name,
        current_time,
        current_time,
        False,
        product_offering_id,
        adjusted_rate,
        adjusted_price,
        adjusted_rate_lock_count,
        adjusted_rate_lock_unit,
        undiscounted_rate,
        starting_adjusted_rate,
        starting_adjusted_price,
        status_type,
        scenario_business_id,
        str(run_id) # Run_Id
    )

    try:
        # Print SQL and parameters *before* execution for debugging
        print(f"Executing SQL: {sql}")
        print(f"With parameters: {params}")

        cursor.execute(sql, *params)
        
        # Fetch the ID directly from the OUTPUT clause
        price_scenario_id_raw_result = cursor.fetchone()

        price_scenario_id = None
        if price_scenario_id_raw_result is None or price_scenario_id_raw_result[0] is None:
            # Generate a random integer if the ID is not returned (shouldn't happen with OUTPUT)
            generated_random_id = random.randint(1000000000, 2147483647) # Max INT for SQL Server
            price_scenario_id = generated_random_id
            print(f"  WARNING: Failed to retrieve ID for Price Scenario '{name}' using OUTPUT INSERTED.Id. "
                  f"Generated a random integer ID '{generated_random_id}' as a placeholder. "
                  f"Subsequent child insertions using this ID will likely fail if the DB foreign key is INT and this ID does not exist.")
            # Re-print SQL and parameters here for clarity in error logs
            print(f"  Failed SQL (OUTPUT INSERTED.Id returned None): {sql}")
            print(f"  Failed Parameters: {params}")
        else:
            price_scenario_id = int(price_scenario_id_raw_result[0])
            print(f"  Inserted Price Scenario with Id: {price_scenario_id}")
        
        return price_scenario_id # This can now be an int or a random int

    except pyodbc.Error as ex:
        print(f"Error inserting Price Scenario '{name}': {ex}")
        # Dump SQL and parameters on pyodbc error
        print(f"  Failed SQL (pyodbc.Error): {sql}")
        print(f"  Failed Parameters: {params}")
        # Re-raise the exception to ensure the transaction rollback occurs
        raise

def insert_price_scenario_calculated_fields(cursor, price_scenario_id, calculated_fields_data, run_id):
    """
    Inserts data into dbo.LoanPASS_Price_Scenario_Calculated_Fields.
    Includes Run_Id.
    """
    if not isinstance(price_scenario_id, int):
        print(f"  Skipping insertion of Price Scenario Calculated Fields for Scenario Id: {price_scenario_id}. "
              "Parent scenario did not generate a valid integer ID.")
        return

    print(f"  Inserting Price Scenario Calculated Fields for Scenario Id: {price_scenario_id}")
    sql = """
    INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Field_Id__c, Value_Type__c,
        Enum_Type_Id__c, Variant_Id__c, Number_Value__c,
        String_Value__c, Duration_Count__c, Duration_Unit__c, Run_Id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """.format(table_name)

    current_time = datetime.now(timezone.utc)
    for field in calculated_fields_data:
        field_id = field.get('fieldId')
        name = field.get('Name', field_id) # Use Name if present, else fieldId

        extracted_values = extract_field_values(field)

        try:
            cursor.execute(
                sql,
                name,
                current_time,
                current_time,
                False,
                price_scenario_id, # This expects an integer ID
                field_id,
                extracted_values['Value_Type__c'],
                extracted_values['Enum_Type_Id__c'],
                extracted_values['Variant_Id__c'],
                extracted_values['Number_Value__c'],
                extracted_values['String_Value__c'],
                extracted_values['Duration_Count__c'],
                extracted_values['Duration_Unit__c'],
                str(run_id) # Run_Id
            )
            print(f"  Inserted Price Scenario Calculated Field: {name}")
        except pyodbc.Error as ex:
            print(f"  Error inserting Price Scenario Calculated Field '{name}': {ex}")
            # Re-print SQL and parameters for debugging on error
            print(f"  Failed SQL: {sql}")
            print(f"  Failed Parameters: {(name, current_time, current_time, False, price_scenario_id, field_id, extracted_values['Value_Type__c'], extracted_values['Enum_Type_Id__c'], extracted_values['Variant_Id__c'], extracted_values['Number_Value__c'], extracted_values['String_Value__c'], extracted_values['Duration_Count__c'], extracted_values['Duration_Unit__c'], str(run_id))}")
            raise

def insert_price_scenario_errors(cursor, price_scenario_id, errors_data, run_id):
    """
    Inserts data into dbo.LoanPASS_Price_Scenario_Errors.
    Includes Run_Id.
    """
    if not isinstance(price_scenario_id, int):
        print(f"  Skipping insertion of Price Scenario Errors for Scenario Id: {price_scenario_id}. "
              "Parent scenario did not generate a valid integer ID.")
        return

    print(f"  Inserting Price Scenario Errors for Scenario Id: {price_scenario_id}")
    sql = """
    INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Source_Type__c, Source_Rule_Id__c,
        Error_Type__c, Error_Field_Id__c, Message__c, Run_Id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    current_time = datetime.now(timezone.utc)
    for error in errors_data:
        source_type = error.get('source', {}).get('type')
        source_rule_id = error.get('source', {}).get('ruleId')
        error_type = error.get('kind', {}).get('type')
        error_field_id = error.get('kind', {}).get('fieldId')
        # Message is not directly available in the provided error JSON,
        # so we can construct one or leave it None.
        message = f"Field '{error_field_id}' is {error_type} (Rule: {source_rule_id})" if error_field_id else None
        name = error.get('Name', source_rule_id or error_field_id or "Error")

        try:
            cursor.execute(
                sql,
                name,
                current_time,
                current_time,
                False,
                price_scenario_id, # This expects an integer ID
                source_type,
                source_rule_id,
                error_type,
                error_field_id,
                message,
                str(run_id) # Run_Id
            )
            print(f"    Inserted Price Scenario Error: {name} (Field: {error_field_id})")
        except pyodbc.Error as ex:
            print(f"    Error inserting Price Scenario Error '{name}': {ex}")
            # Re-print SQL and parameters for debugging on error
            print(f"    Failed SQL: {sql}")
            print(f"    Failed Parameters: {(name, current_time, current_time, False, price_scenario_id, source_type, source_rule_id, error_type, error_field_id, message, str(run_id))}")
            raise

def insert_price_scenario_rejections(cursor, price_scenario_id, rejections_data, run_id):
    """
    Inserts data into dbo.LoanPASS_Price_Scenario_Rejections.
    Includes Run_Id.
    """
    if not isinstance(price_scenario_id, int):
        print(f"  Skipping insertion of Price Scenario Rejections for Scenario Id: {price_scenario_id}. "
              "Parent scenario did not generate a valid integer ID.")
        return

    print(f"  Inserting Price Scenario Rejections for Scenario Id: {price_scenario_id}")
    sql = """
    INSERT INTO dbo.LoanPASS_Price_Scenario_Rejections (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Source_Type__c, Source_Rule_Id__c, Message__c, Run_Id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    current_time = datetime.now(timezone.utc)
    for rejection in rejections_data:
        source_type = rejection.get('source', {}).get('type')
        source_rule_id = rejection.get('source', {}).get('ruleId')
        message = rejection.get('message')
        name = rejection.get('Name', source_rule_id or message[:50] if message else "Rejection")

        try:
            cursor.execute(
                sql,
                name,
                current_time,
                current_time,
                False,
                price_scenario_id, # This expects an integer ID
                source_type,
                source_rule_id,
                message,
                str(run_id) # Run_Id
            )
            print(f"    Inserted Price Scenario Rejection: {name}")
        except pyodbc.Error as ex:
            print(f"    Error inserting Price Scenario Rejection '{name}': {ex}")
            # Re-print SQL and parameters for debugging on error
            print(f"    Failed SQL: {sql}")
            print(f"    Failed Parameters: {(name, current_time, current_time, False, price_scenario_id, source_type, source_rule_id, message, str(run_id))}")
            raise

def insert_price_scenario_review_requirements(cursor, price_scenario_id, review_requirements_data, run_id):
    """
    Inserts data into dbo.LoanPASS_Price_Scenario_Review_Requirements.
    Includes Run_Id.
    """
    if not review_requirements_data:
        print(f"  No Review Requirements to insert for Scenario Id: {price_scenario_id}")
        return
    if not isinstance(price_scenario_id, int):
        print(f"  Skipping insertion of Price Scenario Review Requirements for Scenario Id: {price_scenario_id}. "
              "Parent scenario did not generate a valid integer ID.")
        return

    print(f"  Inserting Price Scenario Review Requirements for Scenario Id: {price_scenario_id}")
    sql = """
    INSERT INTO dbo.LoanPASS_Price_Scenario_Review_Requirements (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Description__c, Requirement_Type__c, Source_Details__c, Run_Id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    current_time = datetime.now(timezone.utc)
    for req in review_requirements_data:
        # Assuming a structure for review requirements if they were present.
        # This part might need adjustment if actual data comes in a different format.
        description = req.get('description')
        req_type = req.get('type')
        source_details = req.get('sourceDetails')
        name = req.get('Name', description[:50] if description else "Review Requirement")

        try:
            cursor.execute(
                sql,
                name,
                current_time,
                current_time,
                False,
                price_scenario_id, # This expects an integer ID
                description,
                req_type,
                source_details,
                str(run_id) # Run_Id
            )
            print(f"    Inserted Price Scenario Review Requirement: {name}")
        except pyodbc.Error as ex:
            print(f"    Error inserting Price Scenario Review Requirement '{name}': {ex}")
            # Re-print SQL and parameters for debugging on error
            print(f"    Failed SQL: {sql}")
            print(f"    Failed Parameters: {(name, current_time, current_time, False, price_scenario_id, description, req_type, source_details, str(run_id))}")
            raise

def insert_price_scenario_adjustments(cursor, price_scenario_id, adjustments_data, category, run_id):
    """
    Inserts data into dbo.LoanPASS_Price_Scenario_Adjustments.
    Includes Run_Id.
    """
    if not adjustments_data:
        print(f"  No {category} Adjustments to insert for Scenario Id: {price_scenario_id}")
        return
    if not isinstance(price_scenario_id, int):
        print(f"  Skipping insertion of {category} Adjustments for Scenario Id: {price_scenario_id}. "
              "Parent scenario did not generate a valid integer ID.")
        return

    print(f"  Inserting {category} Adjustments for Scenario Id: {price_scenario_id}")
    sql = """
    INSERT INTO dbo.LoanPASS_Price_Scenario_Adjustments (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Adjustment_Category__c, Description__c,
        Adjustment_Value_Numeric__c, Adjustment_Value_Text__c,
        Source_Rule_Id__c, Source_Field_Id__c, Notes__c, Run_Id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    current_time = datetime.now(timezone.utc)
    for adj in adjustments_data:
        # Assuming a structure for adjustments if they were present.
        # This part might need adjustment if actual data comes in a different format.
        description = adj.get('description')
        adj_value_numeric = adj.get('value')
        adj_value_text = adj.get('textValue')
        source_rule_id = adj.get('source', {}).get('ruleId')
        source_field_id = adj.get('source', {}).get('fieldId')
        notes = adj.get('notes')
        name = adj.get('Name', description[:50] if description else f"{category} Adjustment")

        try:
            cursor.execute(
                sql,
                name,
                current_time,
                current_time,
                False,
                price_scenario_id, # This expects an integer ID
                category,
                description,
                adj_value_numeric,
                adj_value_text,
                source_rule_id,
                source_field_id,
                notes,
                str(run_id) # Run_Id
            )
            print(f"    Inserted Price Scenario Adjustment ({category}): {name}")
        except pyodbc.Error as ex:
            print(f"    Error inserting Price Scenario Adjustment ({category}) '{name}': {ex}")
            # Re-print SQL and parameters for debugging on error
            print(f"    Failed SQL: {sql}")
            print(f"    Failed Parameters: {(name, current_time, current_time, False, price_scenario_id, category, description, adj_value_numeric, adj_value_text, source_rule_id, source_field_id, notes, str(run_id))}")
            raise

def insert_price_scenario_stipulations(cursor, price_scenario_id, stipulations_data, run_id):
    """
    Inserts data into dbo.LoanPASS_Price_Scenario_Stipulations.
    Includes Run_Id.
    """
    if not stipulations_data:
        print(f"  No Stipulations to insert for Scenario Id: {price_scenario_id}")
        return
    if not isinstance(price_scenario_id, int):
        print(f"  Skipping insertion of Price Scenario Stipulations for Scenario Id: {price_scenario_id}. "
              "Parent scenario did not generate a valid integer ID.")
        return

    print(f"  Inserting Price Scenario Stipulations for Scenario Id: {price_scenario_id}")
    sql = """
    INSERT INTO dbo.LoanPASS_Price_Scenario_Stipulations (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Description__c, Stipulation_Code__c,
        Source_Details__c, Is_Satisfied__c, Run_Id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    current_time = datetime.now(timezone.utc)
    for stip in stipulations_data:
        # Assuming a structure for stipulations if they were present.
        # This part might need adjustment if actual data comes in a different format.
        description = stip.get('description')
        stip_code = stip.get('stipulationCode')
        source_details = stip.get('sourceDetails')
        is_satisfied = stip.get('isSatisfied', False)
        name = stip.get('Name', description[:50] if description else "Stipulation")

        try:
            cursor.execute(
                sql,
                name,
                current_time,
                current_time,
                False,
                price_scenario_id, # This expects an integer ID
                description,
                stip_code,
                source_details,
                is_satisfied,
                str(run_id) # Run_Id
            )
            print(f"    Inserted Price Scenario Stipulation: {name}")
        except pyodbc.Error as ex:
            print(f"    Error inserting Price Scenario Stipulation '{name}': {ex}")
            # Re-print SQL and parameters for debugging on error
            print(f"    Failed SQL: {sql}")
            print(f"    Failed Parameters: {(name, current_time, current_time, False, price_scenario_id, description, stip_code, source_details, is_satisfied, str(run_id))}")
            raise


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

def call_loanpass_api(endpoint, json_data_for_api):
    """
    Generic function to call a LoanPASS API endpoint with the provided JSON data.
    """
    headers = {
        "Authorization": f"Bearer {LOANPASS_API_TOKEN}",
        "Content-Type": "application/json"
    }

    print(f"\nCalling LoanPASS API: {endpoint}")
    print(f"Request Payload: {json.dumps(json_data_for_api, indent=2)}")
    try:
        response = requests.post(endpoint, headers=headers, json=json_data_for_api, timeout=60) # Increased timeout
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        print(f"LoanPASS API call successful. Status Code: {response.status_code}")
        api_response_json = response.json()
        print("API Response JSON received.")
        print(f"API Response: {json.dumps(api_response_json, indent=2)}")
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

def process_loanpass_json(cursor, json_data, run_id):
    """
    Processes the entire LoanPASS JSON structure and inserts data into the database.
    This function is designed to insert only top-level product offerings and price scenarios.
    All other nested insertions (calculated fields, errors, rejections, review requirements, adjustments, stipulations)
    are intentionally suppressed for this version of the script.
    """
    try:
        # 1. Insert LoanPASS_Product_Offerings (top-level JSON is the product offering)
        product_offering_id = insert_product_offering(cursor, json_data, run_id)

        # 2. Suppress Insert into LoanPASS_Product_Calculated_Fields (from productFields array)
        # if 'productFields' in json_data and json_data['productFields']:
        #     insert_product_calculated_fields(cursor, product_offering_id, json_data['productFields'], run_id, is_calculated=False)

        # 3. Suppress Insert into LoanPASS_Product_Calculated_Fields (from calculatedFields array)
        # if 'calculatedFields' in json_data and json_data['calculatedFields']:
        #     insert_product_calculated_fields(cursor, product_offering_id, json_data['calculatedFields'], run_id, is_calculated=True)

        # 4. Insert LoanPASS_Price_Scenarios and suppress their nested data
        price_scenarios_data = json_data.get('status', {}).get('priceScenarios', [])
        if price_scenarios_data:
            for scenario in price_scenarios_data:
                # The insert_price_scenario function will now return an integer or a random integer.
                price_scenario_id = insert_price_scenario(cursor, product_offering_id, scenario, run_id)

                # Only proceed with child insertions if an integer ID was successfully obtained
                if isinstance(price_scenario_id, int):
                    # Suppress Insert nested data for each price scenario
                    # if 'calculatedFields' in scenario and scenario['calculatedFields']:
                    #     insert_price_scenario_calculated_fields(cursor, price_scenario_id, scenario['calculatedFields'], run_id)
                    
                    scenario_status = scenario.get('status', {})
                    # if 'errors' in scenario_status and scenario_status['errors']:
                    #     insert_price_scenario_errors(cursor, price_scenario_id, scenario_status['errors'], run_id)
                    # if 'rejections' in scenario_status and scenario_status['rejections']:
                    #     insert_price_scenario_rejections(cursor, price_scenario_id, scenario_status['rejections'], run_id)
                    # if 'reviewRequirements' in scenario_status and scenario_status['reviewRequirements']:
                    #     insert_price_scenario_review_requirements(cursor, price_scenario_id, scenario_status['reviewRequirements'], run_id)
                    
                    # Suppress Handle various adjustment types
                    # if 'priceAdjustments' in scenario_status and scenario_status['priceAdjustments']:
                    #     insert_price_scenario_adjustments(cursor, price_scenario_id, scenario_status['priceAdjustments'], 'PriceAdjustment', run_id)
                    # if 'marginAdjustments' in scenario_status and scenario_status['marginAdjustments']:
                    #     insert_price_scenario_adjustments(cursor, price_scenario_id, scenario_status['marginAdjustments'], 'MarginAdjustment', run_id)
                    # if 'rateAdjustments' in scenario_status and scenario_status['rateAdjustments']:
                    #     insert_price_scenario_adjustments(cursor, price_scenario_id, scenario_status['rateAdjustments'], 'RateAdjustment', run_id)
                    # if 'finalPriceAdjustments' in scenario_status and scenario_status['finalPriceAdjustments']:
                    #     insert_price_scenario_adjustments(cursor, price_scenario_id, scenario_status['finalPriceAdjustments'], 'FinalPriceAdjustment', run_id)
                    # if 'finalMarginAdjustments' in scenario_status and scenario_status['finalMarginAdjustments']:
                    #     insert_price_scenario_adjustments(cursor, price_scenario_id, scenario_status['finalMarginAdjustments'], 'FinalMarginAdjustment', run_id)
                    # if 'finalRateAdjustments' in scenario_status and scenario_status['finalRateAdjustments']:
                    #     insert_price_scenario_adjustments(cursor, price_scenario_id, scenario_status['finalRateAdjustments'], 'FinalRateAdjustment', run_id)
                    
                    # if 'stipulations' in scenario_status and scenario_status['stipulations']:
                    #     insert_price_scenario_stipulations(cursor, price_scenario_id, scenario_status['stipulations'], run_id)
                else:
                    # This block will be hit if a random integer was generated due to a failed parent insert.
                    print(f"  Skipping nested insertions for scenario '{scenario.get('id')}' because no valid integer ID was retrieved from the database.")
        print("All data successfully inserted for this product.")

    except pyodbc.Error as ex:
        print(f"A database error occurred during processing JSON data: {ex}")
        raise # Re-raise to allow outer function to handle rollback
    except Exception as e:
        print(f"An unexpected error occurred during processing JSON data: {e}")
        raise # Re-raise to allow outer function to handle rollback


def process_loan_pass_data(db_connection_string, initial_summary_request_data=None):
    """
    Orchestrates the process:
    1. Calls the /execute-summary API to get a list of products.
    2. For each product, calls the /execute-product API to get detailed data.
    3. Inserts/updates the detailed product data into the database tables.
    Handles transactions for atomicity.
    """
    conn = None
    # Generate a unique Run_Id for this execution using a human-readable timestamp and UUID.
    # Format: YYYY-MM-DD_HH-MM-SS_UUID
    current_run_id = f"{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')}_{uuid.uuid4()}"
    print(f"Starting data processing with Run ID: {current_run_id}")

    start_time = datetime.now()
    print(f"Run started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # --- 1. Prepare and Call /execute-summary API ---
        if initial_summary_request_data:
            summary_request_data = initial_summary_request_data
            # Ensure currentTime is updated even if provided via file
            summary_request_data["currentTime"] = datetime.now().astimezone().isoformat()
        else:
            summary_request_data = loanpass_summary_api_request_template.copy()
            summary_request_data["currentTime"] = datetime.now().astimezone().isoformat()

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
        conn = get_db_connection(db_connection_string)
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
            product_detail_request_data["currentTime"] = datetime.now().astimezone().isoformat()
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

                # Call the new process_loanpass_json function to handle insertion
                process_loanpass_json(cursor, data_for_db_insertion, current_run_id)
                
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
        end_time = datetime.now()
        duration = end_time - start_time
        print(f"\n--- Run Summary ---")
        print(f"Run ended at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total duration: {duration}")
        if conn:
            conn.close()
            print("Database connection closed.")

def main():
    """
    Main function to execute the JSON processing and database insertion.
    Reads connection string from environment variable.
    """
    my_connection_string = os.getenv('SQL_CONNECTION_STRING')

    if not my_connection_string:
        raise ValueError("SQL_CONNECTION_STRING environment variable not set. Please set it before running the script.")

    # Call the new orchestrating function to fetch data from LoanPASS API and process it
    process_loan_pass_data(my_connection_string)

if __name__ == "__main__":
    main()
