import pyodbc
import json
from datetime import datetime, timezone
import os # Import the os module to access environment variables

# --- Database Connection Configuration ---
# IMPORTANT: Replace this with your actual SQL Server connection string.
# Example: "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=LoanPASS_DB;UID=your_username;PWD=your_password"
# For Windows Authentication: "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=LoanPASS_DB;Trusted_Connection=yes;"
# You might need to install the appropriate ODBC driver for SQL Server.
# For Windows: 'ODBC Driver 17 for SQL Server' is common.
# For Linux/macOS: Refer to Microsoft's documentation for ODBC drivers.
# DB_CONFIG is removed as the connection string will be passed directly.

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


def insert_product_offering(cursor, product_data):
    """
    Inserts or updates data into dbo.LoanPASS_Product_Offerings (upsert)
    based on Product_Code__c and returns its Id.
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

    # SQL MERGE statement for upsert
    sql = """
    MERGE INTO dbo.LoanPASS_Product_Offerings AS target
    USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS source (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        Product_Id__c, Product_Name__c, Product_Code__c,
        Investor_Name__c, Investor_Code__c, Is_Pricing_Enabled__c,
        Status__c, Rate_Sheet_Effective_Timestamp__c
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
            target.IsDeleted = source.IsDeleted -- Also update IsDeleted if it changes
    WHEN NOT MATCHED THEN
        INSERT (
            Name, CreatedDate, LastModifiedDate, IsDeleted,
            Product_Id__c, Product_Name__c, Product_Code__c,
            Investor_Name__c, Investor_Code__c, Is_Pricing_Enabled__c,
            Status__c, Rate_Sheet_Effective_Timestamp__c
        )
        VALUES (
            source.Name, source.CreatedDate, source.LastModifiedDate, source.IsDeleted,
            source.Product_Id__c, source.Product_Name__c, source.Product_Code__c,
            source.Investor_Name__c, source.Investor_Code__c, source.Is_Pricing_Enabled__c,
            source.Status__c, source.Rate_Sheet_Effective_Timestamp__c
        )
    OUTPUT INSERTED.Id;
    """
    try:
        cursor.execute(
            sql,
            name,
            current_time, # CreatedDate for new insert
            current_time, # LastModifiedDate for new insert
            False,        # IsDeleted
            product_id_c,
            product_name_c,
            product_code_c,
            investor_name_c,
            investor_code_c,
            is_pricing_enabled_c,
            status_c,
            rate_sheet_effective_timestamp_c,
            current_time # LastModifiedDate for update
        )
        product_offering_id = cursor.fetchone()[0]
        print(f"Upserted Product Offering with Id: {product_offering_id}")
        return int(product_offering_id)
    except pyodbc.Error as ex:
        print(f"Error upserting Product Offering '{name}' (Code: {product_code_c}): {ex}")
        raise

def insert_product_calculated_fields(cursor, product_offering_id, product_fields_data, is_calculated=False):
    """
    Inserts data into dbo.LoanPASS_Product_Calculated_Fields.
    Can handle both 'productFields' and 'calculatedFields' from the top level.
    """
    table_name = "dbo.LoanPASS_Product_Calculated_Fields"
    print(f"Inserting {'Calculated' if is_calculated else 'Product'} Fields for Product Offering Id: {product_offering_id}")
    sql = """
    INSERT INTO {} (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Product_Offering_Id, Field_Id__c, Value_Type__c,
        Enum_Type_Id__c, Variant_Id__c, Number_Value__c,
        String_Value__c, Duration_Count__c, Duration_Unit__c
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                extracted_values['Duration_Unit__c']
            )
            print(f"  Inserted Product {'Calculated' if is_calculated else ''} Field: {name}")
        except pyodbc.Error as ex:
            print(f"  Error inserting Product {'Calculated' if is_calculated else ''} Field '{name}': {ex}")
            raise

def insert_price_scenario(cursor, product_offering_id, scenario_data):
    """Inserts data into dbo.LoanPASS_Price_Scenarios and returns its Id."""
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
    # Ensure all values passed to SQL are not None if the target column is NOT NULL
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
        Starting_Adjusted_Price__c, Status__c, Scenario_Business_Id__c
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        scenario_business_id
    )

    try:
        # Print SQL and parameters *before* execution for debugging
        print(f"Executing SQL: {sql}")
        print(f"With parameters: {params}")

        cursor.execute(sql, *params)
        
        # Fetch the ID after insertion
        cursor.execute("SELECT SCOPE_IDENTITY()")
        price_scenario_id_result = cursor.fetchone()

        if price_scenario_id_result and price_scenario_id_result[0] is not None:
            price_scenario_id = price_scenario_id_result[0]
            print(f"  Inserted Price Scenario with Id: {price_scenario_id}")
            return int(price_scenario_id)
        else:
            print(f"  WARNING: Failed to insert Price Scenario '{name}' or retrieve its ID. SCOPE_IDENTITY() returned None.")
            # Re-print SQL and parameters here for clarity in error logs
            print(f"  Failed SQL (SCOPE_IDENTITY returned None): {sql}")
            print(f"  Failed Parameters: {params}")
            # Raise an error or return a specific value to indicate failure
            raise ValueError(f"Failed to insert Price Scenario '{name}' or retrieve its ID.")

    except pyodbc.Error as ex:
        print(f"Error inserting Price Scenario '{name}': {ex}")
        # Dump SQL and parameters on pyodbc error
        print(f"  Failed SQL (pyodbc.Error): {sql}")
        print(f"  Failed Parameters: {params}")
        # Re-raise the exception to ensure the transaction rollback occurs
        raise

def insert_price_scenario_calculated_fields(cursor, price_scenario_id, calculated_fields_data):
    """Inserts data into dbo.LoanPASS_Price_Scenario_Calculated_Fields."""
    print(f"  Inserting Price Scenario Calculated Fields for Scenario Id: {price_scenario_id}")
    sql = """
    INSERT INTO dbo.LoanPASS_Price_Scenario_Calculated_Fields (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Field_Id__c, Value_Type__c,
        Enum_Type_Id__c, Variant_Id__c, Number_Value__c,
        String_Value__c, Duration_Count__c, Duration_Unit__c
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
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
                price_scenario_id,
                field_id,
                extracted_values['Value_Type__c'],
                extracted_values['Enum_Type_Id__c'],
                extracted_values['Variant_Id__c'],
                extracted_values['Number_Value__c'],
                extracted_values['String_Value__c'],
                extracted_values['Duration_Count__c'],
                extracted_values['Duration_Unit__c']
            )
            print(f"  Inserted Price Scenario Calculated Field: {name}")
        except pyodbc.Error as ex:
            print(f"  Error inserting Price Scenario Calculated Field '{name}': {ex}")
            # Re-print SQL and parameters for debugging on error
            print(f"  Failed SQL: {sql}")
            print(f"  Failed Parameters: {(name, current_time, current_time, False, price_scenario_id, field_id, extracted_values['Value_Type__c'], extracted_values['Enum_Type_Id__c'], extracted_values['Variant_Id__c'], extracted_values['Number_Value__c'], extracted_values['String_Value__c'], extracted_values['Duration_Count__c'], extracted_values['Duration_Unit__c'])}")
            raise

def insert_price_scenario_errors(cursor, price_scenario_id, errors_data):
    """Inserts data into dbo.LoanPASS_Price_Scenario_Errors."""
    print(f"  Inserting Price Scenario Errors for Scenario Id: {price_scenario_id}")
    sql = """
    INSERT INTO dbo.LoanPASS_Price_Scenario_Errors (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Source_Type__c, Source_Rule_Id__c,
        Error_Type__c, Error_Field_Id__c, Message__c
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                price_scenario_id,
                source_type,
                source_rule_id,
                error_type,
                error_field_id,
                message
            )
            print(f"    Inserted Price Scenario Error: {name} (Field: {error_field_id})")
        except pyodbc.Error as ex:
            print(f"    Error inserting Price Scenario Error '{name}': {ex}")
            # Re-print SQL and parameters for debugging on error
            print(f"    Failed SQL: {sql}")
            print(f"    Failed Parameters: {(name, current_time, current_time, False, price_scenario_id, source_type, source_rule_id, error_type, error_field_id, message)}")
            raise

def insert_price_scenario_rejections(cursor, price_scenario_id, rejections_data):
    """Inserts data into dbo.LoanPASS_Price_Scenario_Rejections."""
    print(f"  Inserting Price Scenario Rejections for Scenario Id: {price_scenario_id}")
    sql = """
    INSERT INTO dbo.LoanPASS_Price_Scenario_Rejections (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Source_Type__c, Source_Rule_Id__c, Message__c
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
                price_scenario_id,
                source_type,
                source_rule_id,
                message
            )
            print(f"    Inserted Price Scenario Rejection: {name}")
        except pyodbc.Error as ex:
            print(f"    Error inserting Price Scenario Rejection '{name}': {ex}")
            # Re-print SQL and parameters for debugging on error
            print(f"    Failed SQL: {sql}")
            print(f"    Failed Parameters: {(name, current_time, current_time, False, price_scenario_id, source_type, source_rule_id, message)}")
            raise

def insert_price_scenario_review_requirements(cursor, price_scenario_id, review_requirements_data):
    """Inserts data into dbo.LoanPASS_Price_Scenario_Review_Requirements."""
    if not review_requirements_data:
        print(f"  No Review Requirements to insert for Scenario Id: {price_scenario_id}")
        return

    print(f"  Inserting Price Scenario Review Requirements for Scenario Id: {price_scenario_id}")
    sql = """
    INSERT INTO dbo.LoanPASS_Price_Scenario_Review_Requirements (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Description__c, Requirement_Type__c, Source_Details__c
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
                price_scenario_id,
                description,
                req_type,
                source_details
            )
            print(f"    Inserted Price Scenario Review Requirement: {name}")
        except pyodbc.Error as ex:
            print(f"    Error inserting Price Scenario Review Requirement '{name}': {ex}")
            # Re-print SQL and parameters for debugging on error
            print(f"    Failed SQL: {sql}")
            print(f"    Failed Parameters: {(name, current_time, current_time, False, price_scenario_id, description, req_type, source_details)}")
            raise

def insert_price_scenario_adjustments(cursor, price_scenario_id, adjustments_data, category):
    """Inserts data into dbo.LoanPASS_Price_Scenario_Adjustments."""
    if not adjustments_data:
        print(f"  No {category} Adjustments to insert for Scenario Id: {price_scenario_id}")
        return

    print(f"  Inserting {category} Adjustments for Scenario Id: {price_scenario_id}")
    sql = """
    INSERT INTO dbo.LoanPASS_Price_Scenario_Adjustments (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Adjustment_Category__c, Description__c,
        Adjustment_Value_Numeric__c, Adjustment_Value_Text__c,
        Source_Rule_Id__c, Source_Field_Id__c, Notes__c
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                price_scenario_id,
                category,
                description,
                adj_value_numeric,
                adj_value_text,
                source_rule_id,
                source_field_id,
                notes
            )
            print(f"    Inserted Price Scenario Adjustment ({category}): {name}")
        except pyodbc.Error as ex:
            print(f"    Error inserting Price Scenario Adjustment ({category}) '{name}': {ex}")
            # Re-print SQL and parameters for debugging on error
            print(f"    Failed SQL: {sql}")
            print(f"    Failed Parameters: {(name, current_time, current_time, False, price_scenario_id, category, description, adj_value_numeric, adj_value_text, source_rule_id, source_field_id, notes)}")
            raise

def insert_price_scenario_stipulations(cursor, price_scenario_id, stipulations_data):
    """Inserts data into dbo.LoanPASS_Price_Scenario_Stipulations."""
    if not stipulations_data:
        print(f"  No Stipulations to insert for Scenario Id: {price_scenario_id}")
        return

    print(f"  Inserting Price Scenario Stipulations for Scenario Id: {price_scenario_id}")
    sql = """
    INSERT INTO dbo.LoanPASS_Price_Scenario_Stipulations (
        Name, CreatedDate, LastModifiedDate, IsDeleted,
        LoanPASS_Price_Scenario_Id, Description__c, Stipulation_Code__c,
        Source_Details__c, Is_Satisfied__c
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                price_scenario_id,
                description,
                stip_code,
                source_details,
                is_satisfied
            )
            print(f"    Inserted Price Scenario Stipulation: {name}")
        except pyodbc.Error as ex:
            print(f"    Error inserting Price Scenario Stipulation '{name}': {ex}")
            # Re-print SQL and parameters for debugging on error
            print(f"    Failed SQL: {sql}")
            print(f"    Failed Parameters: {(name, current_time, current_time, False, price_scenario_id, description, stip_code, source_details, is_satisfied)}")
            raise


def process_loanpass_json(json_data, conn_str):
    """
    Processes the entire LoanPASS JSON structure and inserts data into the database.
    Accepts the database connection string as an argument.
    """
    conn = None
    try:
        conn = get_db_connection(conn_str) # Pass the connection string here
        cursor = conn.cursor()

        # 1. Insert LoanPASS_Product_Offerings (top-level JSON is the product offering)
        product_offering_id = insert_product_offering(cursor, json_data)

        # 2. Insert LoanPASS_Product_Calculated_Fields (from productFields array)
        if 'productFields' in json_data and json_data['productFields']:
            insert_product_calculated_fields(cursor, product_offering_id, json_data['productFields'], is_calculated=False)

        # 3. Insert LoanPASS_Product_Calculated_Fields (from calculatedFields array)
        if 'calculatedFields' in json_data and json_data['calculatedFields']:
            insert_product_calculated_fields(cursor, product_offering_id, json_data['calculatedFields'], is_calculated=True)

        # 4. Insert LoanPASS_Price_Scenarios and their nested data
        price_scenarios_data = json_data.get('status', {}).get('priceScenarios', [])
        if price_scenarios_data:
            for scenario in price_scenarios_data:
                price_scenario_id = insert_price_scenario(cursor, product_offering_id, scenario)

                # Insert nested data for each price scenario
                if 'calculatedFields' in scenario and scenario['calculatedFields']:
                    insert_price_scenario_calculated_fields(cursor, price_scenario_id, scenario['calculatedFields'])
                
                scenario_status = scenario.get('status', {})
                if 'errors' in scenario_status and scenario_status['errors']:
                    insert_price_scenario_errors(cursor, price_scenario_id, scenario_status['errors'])
                if 'rejections' in scenario_status and scenario_status['rejections']:
                    insert_price_scenario_rejections(cursor, price_scenario_id, scenario_status['rejections'])
                if 'reviewRequirements' in scenario_status and scenario_status['reviewRequirements']:
                    insert_price_scenario_review_requirements(cursor, price_scenario_id, scenario_status['reviewRequirements'])
                
                # Handle various adjustment types
                if 'priceAdjustments' in scenario_status and scenario_status['priceAdjustments']:
                    insert_price_scenario_adjustments(cursor, price_scenario_id, scenario_status['priceAdjustments'], 'PriceAdjustment')
                if 'marginAdjustments' in scenario_status and scenario_status['marginAdjustments']:
                    insert_price_scenario_adjustments(cursor, price_scenario_id, scenario_status['marginAdjustments'], 'MarginAdjustment')
                if 'rateAdjustments' in scenario_status and scenario_status['rateAdjustments']:
                    insert_price_scenario_adjustments(cursor, price_scenario_id, scenario_status['rateAdjustments'], 'RateAdjustment')
                if 'finalPriceAdjustments' in scenario_status and scenario_status['finalPriceAdjustments']:
                    insert_price_scenario_adjustments(cursor, price_scenario_id, scenario_status['finalPriceAdjustments'], 'FinalPriceAdjustment')
                if 'finalMarginAdjustments' in scenario_status and scenario_status['finalMarginAdjustments']:
                    insert_price_scenario_adjustments(cursor, price_scenario_id, scenario_status['finalMarginAdjustments'], 'FinalMarginAdjustment')
                if 'finalRateAdjustments' in scenario_status and scenario_status['finalRateAdjustments']:
                    insert_price_scenario_adjustments(cursor, price_scenario_id, scenario_status['finalRateAdjustments'], 'FinalRateAdjustment')
                
                if 'stipulations' in scenario_status and scenario_status['stipulations']:
                    insert_price_scenario_stipulations(cursor, price_scenario_id, scenario_status['stipulations'])

        conn.commit() # Commit the transaction if all insertions are successful
        print("All data successfully inserted and committed.")

    except pyodbc.Error as ex:
        if conn:
            conn.rollback() # Rollback on any error
            print("Transaction rolled back due to a database error.")
        print(f"A database error occurred during processing: {ex}")
    except Exception as e:
        if conn:
            conn.rollback()
            print("Transaction rolled back due to an unexpected error.")
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

# --- Sample JSON Data (Provided by user) ---
sample_json_data = {
  "productId": "76059",
  "productName": "DSCR 40 Year Fixed IO",
  "productCode": "LSFDSCRF40IO",
  "investorName": "Series 2",
  "investorCode": "LSFLENDZ",
  "isPricingEnabled": True,
  "productFields": [
    {
      "fieldId": "field@product-channel",
      "value": {
        "type": "enum",
        "enumTypeId": "channel",
        "variantId": "correspondent"
      }
    },
    {
      "fieldId": "field@mortgage-type",
      "value": {
        "type": "enum",
        "enumTypeId": "mortgage-type",
        "variantId": "non-qm"
      }
    },
    {
      "fieldId": "field@loan-term-type",
      "value": {
        "type": "enum",
        "enumTypeId": "loan-term-type",
        "variantId": "preset"
      }
    },
    {
      "fieldId": "field@preset-loan-term",
      "value": {
        "type": "duration",
        "count": "480",
        "unit": "months"
      }
    },
    {
      "fieldId": "field@preset-loan-maturity",
      "value": {
        "type": "duration",
        "count": "480",
        "unit": "months"
      }
    },
    {
      "fieldId": "field@payment-interval",
      "value": {
        "type": "duration",
        "count": "1",
        "unit": "months"
      }
    },
    {
      "fieldId": "field@amortization-type",
      "value": {
        "type": "enum",
        "enumTypeId": "amortization-type",
        "variantId": "fixed"
      }
    },
    {
      "fieldId": "field@interest-only-period",
      "value": {
        "type": "enum",
        "enumTypeId": "interest-only-period",
        "variantId": "yes"
      }
    },
    {
      "fieldId": "field@i-o-term",
      "value": {
        "type": "duration",
        "count": "120",
        "unit": "months"
      }
    },
    {
      "fieldId": "field@lien-priority",
      "value": {
        "type": "enum",
        "enumTypeId": "lien-priority",
        "variantId": "first"
      }
    },
    {
      "fieldId": "field@max-price-limit",
      "value": {
        "type": "enum",
        "enumTypeId": "yes-no",
        "variantId": "no"
      }
    }
  ],
  "calculatedFields": [
    {
      "fieldId": "calc@total-loan-balance",
      "value": None
    },
    {
      "fieldId": "calc@cash-out-amount",
      "value": {
        "type": "number",
        "value": "0"
      }
    },
    {
      "fieldId": "calc-field@sgcp-prime-connect-co-refi-matrix-output",
      "value": None
    },
    {
      "fieldId": "calc@loan-term-duration-calc",
      "value": {
        "type": "duration",
        "count": "360",
        "unit": "months"
      }
    },
    {
      "fieldId": "calc-field@lsf-all-investment-state-eligibility",
      "value": {
        "type": "enum",
        "enumTypeId": "yes-no",
        "variantId": "yes"
      }
    },
    {
      "fieldId": "calc@number-of-units-enum-to-int-conversion",
      "value": {
        "type": "number",
        "value": "1"
      }
    },
    {
      "fieldId": "calc-field@lsf-all-owner-occupied-state-eligibility",
      "value": {
        "type": "enum",
        "enumTypeId": "yes-no",
        "variantId": "yes"
      }
    },
    {
      "fieldId": "calc-field@lendz-lsf-dscr-non-warrantable-condo-llpa-output",
      "value": {
        "type": "number",
        "value": "-0.375"
      }
    },
    {
      "fieldId": "calc-field@lsm-ces-standard-full-doc-max-cltv-rt-refi",
      "value": None
    },
    {
      "fieldId": "calc-field@obfc-state-tier",
      "value": {
        "type": "string",
        "value": "Tier 1"
      }
    },
    {
      "fieldId": "calc-field@lsm-ces-standard-full-doc-max-cltv-purchase",
      "value": None
    },
    {
      "fieldId": "calc@lendz-lsf-consumer-non-warrantable-condo-llpa",
      "value": {
        "type": "number",
        "value": "-0.375"
      }
    },
    {
      "fieldId": "calc@combined-loan-amount",
      "value": None
    },
    {
      "fieldId": "calc@lsm-ces-alt-doc-final-max-cltv",
      "value": None
    },
    {
      "fieldId": "calc@financed-mi",
      "value": {
        "type": "number",
        "value": "0"
      }
    },
    {
      "fieldId": "calc@loan-term",
      "value": {
        "type": "duration",
        "count": "360",
        "unit": "months"
      }
    },
    {
      "fieldId": "calc-field@lsm-ces-dscr-max-cltv-co-refi",
      "value": None
    },
    {
      "fieldId": "calc@interest-only-allowed",
      "value": {
        "type": "enum",
        "enumTypeId": "interest-only-period",
        "variantId": "no"
      }
    },
    {
      "fieldId": "calc-field@lsm-ces-standard-full-doc-max-cltv-co-refi",
      "value": None
    },
    {
      "fieldId": "calc@months-since-chapter-11-bankruptcy",
      "value": None
    },
    {
      "fieldId": "calc@months-since-foreclosure",
      "value": None
    },
    {
      "fieldId": "calc@lendz-lsf-dscr-non-warrantable-condo-llpa",
      "value": {
        "type": "number",
        "value": "-0.625"
      }
    },
    {
      "fieldId": "calc@months-since-short-sale",
      "value": None
    },
    {
      "fieldId": "calc@channel-allowed",
      "value": {
        "type": "enum",
        "enumTypeId": "yes-no",
        "variantId": "yes"
      }
    },
    {
      "fieldId": "calc@ltv",
      "value": {
        "type": "number",
        "value": "55.00"
      }
    },
    {
      "fieldId": "calc@months-since-deed-in-lieu",
      "value": None
    },
    {
      "fieldId": "calc@second-lien-cltv",
      "value": {
        "type": "number",
        "value": "0"
      }
    },
    {
      "fieldId": "calc-field@lsm-ces-alt-doc-max-cltv-purchase",
      "value": None
    },
    {
      "fieldId": "calc-field@lendz-lsf-consumer-non-warrantable-condo-llpa-output",
      "value": {
        "type": "number",
        "value": "-0.125"
      }
    },
    {
      "fieldId": "calc-field@lendz-lsf-dscr-condo-llpa-output",
      "value": {
        "type": "number",
        "value": "-0.250"
      }
    },
    {
      "fieldId": "calc@total-loan-amount",
      "value": {
        "type": "number",
        "value": "550000.00"
      }
    },
    {
      "fieldId": "calc-field@lsm-ces-alt-doc-max-cltv-co-refi",
      "value": None
    },
    {
      "fieldId": "calc-field@sgcp-prime-connect-rt-refi-matrix-output",
      "value": None
    },
    {
      "fieldId": "calc-field@lsm-ces-dscr-max-cltv-purchase",
      "value": None
    },
    {
      "fieldId": "calc@residual-income",
      "value": {
        "type": "number",
        "value": "1000000.00"
      }
    },
    {
      "fieldId": "calc-field@state-business-only",
      "value": {
        "type": "string",
        "value": "No"
      }
    },
    {
      "fieldId": "calc-field@sgcp-prime-connect-purchase-matrix-output",
      "value": None
    },
    {
      "fieldId": "calc@lsm-ces-short-term-rental-leverage-reduction",
      "value": {
        "type": "number",
        "value": "0"
      }
    },
    {
      "fieldId": "calc-field@lsm-ces-select-full-doc-max-cltv-co-refi",
      "value": None
    },
    {
      "fieldId": "calc@lsm-ces-total-leverage-reduction",
      "value": {
        "type": "number",
        "value": "0"
      }
    },
    {
      "fieldId": "calc@mortgage-type-allowed",
      "value": {
        "type": "enum",
        "enumTypeId": "yes-no",
        "variantId": "yes"
      }
    },
    {
      "fieldId": "calc@cltv",
      "value": {
        "type": "number",
        "value": "55.00"
      }
    },
    {
      "fieldId": "calc@months-since-chapter-7-bankruptcy",
      "value": None
    },
    {
      "fieldId": "calc@lsm-ces-doc-type-leverage-reduction",
      "value": {
        "type": "number",
        "value": "0"
      }
    },
    {
      "fieldId": "calc@lien-position-allowed",
      "value": {
        "type": "enum",
        "enumTypeId": "yes-no",
        "variantId": "yes"
      }
    },
    {
      "fieldId": "calc-field@lsm-ces-dscr-max-cltv-rt-refi",
      "value": None
    },
    {
      "fieldId": "calc@hcltv",
      "value": {
        "type": "number",
        "value": "55.00"
      }
    },
    {
      "fieldId": "calc-field@lendz-lsf-consumer-condo-llpa-output",
      "value": {
        "type": "number",
        "value": "-0.250"
      }
    },
    {
      "fieldId": "calc-field@lsm-ces-alt-doc-max-cltv-rt-refi",
      "value": None
    },
    {
      "fieldId": "calc-field@state-license",
      "value": {
        "type": "string",
        "value": "Yes"
      }
    },
    {
      "fieldId": "calc@lsm-ces-select-full-doc-final-max-cltv",
      "value": {
        "type": "number",
        "value": "0"
      }
    },
    {
      "fieldId": "calc@loan-term-allowed",
      "value": {
        "type": "enum",
        "enumTypeId": "yes-no",
        "variantId": "no"
      }
    },
    {
      "fieldId": "calc@lsm-ces-standard-full-doc-final-max-cltv",
      "value": None
    },
    {
      "fieldId": "calc@mi-and-funding-fee-financed-amount",
      "value": {
        "type": "number",
        "value": "0"
      }
    },
    {
      "fieldId": "calc@lsm-ces-declining-market-leverage-reduction",
      "value": {
        "type": "number",
        "value": "0"
      }
    },
    {
      "fieldId": "calc@total-lien-balance",
      "value": None
    },
    {
      "fieldId": "calc@lsm-ces-dscr-final-max-cltv",
      "value": None
    },
    {
      "fieldId": "calc@months-since-forbearance",
      "value": None
    },
    {
      "fieldId": "calc-field@state-reject-reason",
      "value": {
        "type": "string",
        "value": "N/N"
      }
    },
    {
      "fieldId": "calc@amortization-type-allowed",
      "value": {
        "type": "enum",
        "enumTypeId": "yes-no",
        "variantId": "yes"
      }
    },
    {
      "fieldId": "calc@vista-point-default-credit-score",
      "value": None
    },
    {
      "fieldId": "calc@months-since-chapter-13-bankruptcy",
      "value": None
    }
  ],
  "status": {
    "type": "ok",
    "rateSheetEffectiveTimestamp": "2025-05-27T19:33:36.307949Z",
    "priceScenarios": [
      {
        "id": "d72eab949f1ef6ef24e944c5524e90e8",
        "priceScenarioFields": [
          {
            "fieldId": "base-interest-rate",
            "value": {
              "type": "number",
              "value": "5.5"
            }
          },
          {
            "fieldId": "rate-lock-period",
            "value": {
              "type": "duration",
              "count": "30",
              "unit": "days"
            }
          },
          {
            "fieldId": "base-price",
            "value": {
              "type": "number",
              "value": "89.19901428"
            }
          }
        ],
        "calculatedFields": [
          {
            "fieldId": "calc@initial-mtg-payment",
            "value": {
              "type": "number",
              "value": "2520.83"
            }
          },
          {
            "fieldId": "calc@start-price",
            "value": {
              "type": "number",
              "value": "89.199015"
            }
          },
          {
            "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
            "value": None
          },
          {
            "fieldId": "calc@adjusted-interest-rate",
            "value": {
              "type": "number",
              "value": "5.5"
            }
          },
          {
            "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
            "value": None
          },
          {
            "fieldId": "calc@est-payment",
            "value": {
              "type": "number",
              "value": "2520.83"
            }
          },
          {
            "fieldId": "calc@mtg-payment",
            "value": {
              "type": "number",
              "value": "2520.83"
            }
          },
          {
            "fieldId": "calc@intermediate-rate",
            "value": {
              "type": "number",
              "value": "5.5"
            }
          },
          {
            "fieldId": "calc@eresi-dscr-total-leverage-reduction",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc@eresi-dscr-final-max-ltv",
            "value": {
              "type": "number",
              "value": "75"
            }
          },
          {
            "fieldId": "calc@eresi-dscr-ltv-calc-2",
            "value": {
              "type": "number",
              "value": "999"
            }
          },
          {
            "fieldId": "calc@arm-fully-indexed-rate",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc@adjusted-rate-lock-period",
            "value": {
              "type": "duration",
              "count": "30",
              "unit": "days"
            }
          },
          {
            "fieldId": "calc@eresi-dscr-initial-max-ltv",
            "value": {
              "type": "number",
              "value": "75"
            }
          },
          {
            "fieldId": "calc@initial-io-payment",
            "value": {
              "type": "number",
              "value": "2520.83"
            }
          },
          {
            "fieldId": "calc@final-dscr",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc@io-payment",
            "value": {
              "type": "number",
              "value": "2520.83"
            }
          },
          {
            "fieldId": "calc@final-est-payment",
            "value": {
              "type": "number",
              "value": "2520.83"
            }
          },
          {
            "fieldId": "calc@est-front-dti",
            "value": {
              "type": "number",
              "value": "0.253"
            }
          },
          {
            "fieldId": "calc@final-est-dti",
            "value": {
              "type": "number",
              "value": "0.253"
            }
          },
          {
            "fieldId": "calc@dscr",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc@monthly-mi",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc@dti-enum-to-int-conversion",
            "value": None
          },
          {
            "fieldId": "calc@eresi-dscr-ltv-calc-1",
            "value": {
              "type": "number",
              "value": "75"
            }
          },
          {
            "fieldId": "calc@est-dti",
            "value": {
              "type": "number",
              "value": "0.253"
            }
          },
          {
            "fieldId": "calc@initial-pi-payment",
            "value": {
              "type": "number",
              "value": "3122.84"
            }
          },
          {
            "fieldId": "calc@final-est-front-dti",
            "value": {
              "type": "number",
              "value": "0.253"
            }
          },
          {
            "fieldId": "calc@pi-payment",
            "value": {
              "type": "number",
              "value": "3122.84"
            }
          },
          {
            "fieldId": "calc@1st-lien-est-payment",
            "value": {
              "type": "number",
              "value": "2520.83"
            }
          },
          {
            "fieldId": "calc@final-interest-rate",
            "value": {
              "type": "number",
              "value": "5.5"
            }
          },
          {
            "fieldId": "calc@start-interest-rate",
            "value": {
              "type": "number",
              "value": "5.5"
            }
          }
        ],
        "status": {
          "type": "rejected",
          "rejections": [
            {
              "source": {
                "type": "rule",
                "ruleId": "39371"
              },
              "message": "Product is not eligible for the desired loan term."
            },
            {
              "source": {
                "type": "rule",
                "ruleId": "124523"
              },
              "message": "Rate falls below floor allowed."
            },
            {
              "source": {
                "type": "rule",
                "ruleId": "124525"
              },
              "message": "Investment occupancy only. (Your Occupancy: Primary Residence) DSCR documentation type required. (Your Documentation Type: Bank Statements)"
            }
          ],
          "reviewRequirements": [],
          "errors": [
            {
              "source": {
                "type": "rule",
                "ruleId": "146234"
              },
              "kind": {
                "type": "blank-field",
                "fieldId": "field@decision-credit-score"
              }
            }
          ],
          "priceAdjustments": [],
          "marginAdjustments": [],
          "rateAdjustments": [],
          "finalPriceAdjustments": [],
          "finalMarginAdjustments": [],
          "finalRateAdjustments": [],
          "stipulations": []
        }
      },
      {
        "id": "dcfdc9728be65ce326477abaf12a5fcf",
        "priceScenarioFields": [
          {
            "fieldId": "base-interest-rate",
            "value": {
              "type": "number",
              "value": "5.625"
            }
          },
          {
            "fieldId": "rate-lock-period",
            "value": {
              "type": "duration",
              "count": "30",
              "unit": "days"
            }
          },
          {
            "fieldId": "base-price",
            "value": {
              "type": "number",
              "value": "90.26151428"
            }
          }
        ],
        "calculatedFields": [
          {
            "fieldId": "calc@initial-mtg-payment",
            "value": {
              "type": "number",
              "value": "2578.13"
            }
          },
          {
            "fieldId": "calc@final-dscr",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
            "value": None
          },
          {
            "fieldId": "calc@initial-pi-payment",
            "value": {
              "type": "number",
              "value": "3166.12"
            }
          },
          {
            "fieldId": "calc@est-dti",
            "value": {
              "type": "number",
              "value": "0.258"
            }
          },
          {
            "fieldId": "calc@eresi-dscr-final-max-ltv",
            "value": {
              "type": "number",
              "value": "75"
            }
          },
          {
            "fieldId": "calc@dti-enum-to-int-conversion",
            "value": None
          },
          {
            "fieldId": "calc@start-interest-rate",
            "value": {
              "type": "number",
              "value": "5.625"
            }
          },
          {
            "fieldId": "calc@pi-payment",
            "value": {
              "type": "number",
              "value": "3166.12"
            }
          },
          {
            "fieldId": "calc@1st-lien-est-payment",
            "value": {
              "type": "number",
              "value": "2578.13"
            }
          },
          {
            "fieldId": "calc@final-interest-rate",
            "value": {
              "type": "number",
              "value": "5.625"
            }
          },
          {
            "fieldId": "calc@eresi-dscr-total-leverage-reduction",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc@io-payment",
            "value": {
              "type": "number",
              "value": "2578.13"
            }
          },
          {
            "fieldId": "calc@eresi-dscr-ltv-calc-2",
            "value": {
              "type": "number",
              "value": "999"
            }
          },
          {
            "fieldId": "calc@adjusted-interest-rate",
            "value": {
              "type": "number",
              "value": "5.625"
            }
          },
          {
            "fieldId": "calc@initial-io-payment",
            "value": {
              "type": "number",
              "value": "2578.13"
            }
          },
          {
            "fieldId": "calc@dscr",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc@eresi-dscr-initial-max-ltv",
            "value": {
              "type": "number",
              "value": "75"
            }
          },
          {
            "fieldId": "calc@final-est-front-dti",
            "value": {
              "type": "number",
              "value": "0.258"
            }
          },
          {
            "fieldId": "calc@mtg-payment",
            "value": {
              "type": "number",
              "value": "2578.13"
            }
          },
          {
            "fieldId": "calc@final-est-dti",
            "value": {
              "type": "number",
              "value": "0.258"
            }
          },
          {
            "fieldId": "calc@est-payment",
            "value": {
              "type": "number",
              "value": "2578.13"
            }
          },
          {
            "fieldId": "calc@monthly-mi",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc@final-est-payment",
            "value": {
              "type": "number",
              "value": "2578.13"
            }
          },
          {
            "fieldId": "calc@intermediate-rate",
            "value": {
              "type": "number",
              "value": "5.625"
            }
          },
          {
            "fieldId": "calc@arm-fully-indexed-rate",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc@est-front-dti",
            "value": {
              "type": "number",
              "value": "0.258"
            }
          },
          {
            "fieldId": "calc@adjusted-rate-lock-period",
            "value": {
              "type": "duration",
              "count": "30",
              "unit": "days"
            }
          },
          {
            "fieldId": "calc@eresi-dscr-ltv-calc-1",
            "value": {
              "type": "number",
              "value": "75"
            }
          },
          {
            "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
            "value": None
          },
          {
            "fieldId": "calc@start-price",
            "value": {
              "type": "number",
              "value": "90.261515"
            }
          }
        ],
        "status": {
          "type": "rejected",
          "rejections": [
            {
              "source": {
                "type": "rule",
                "ruleId": "39371"
              },
              "message": "Product is not eligible for the desired loan term."
            },
            {
              "source": {
                "type": "rule",
                "ruleId": "124523"
              },
              "message": "Rate falls below floor allowed."
            },
            {
              "source": {
                "type": "rule",
                "ruleId": "124525"
              },
              "message": "Investment occupancy only. (Your Occupancy: Primary Residence) DSCR documentation type required. (Your Documentation Type: Bank Statements)"
            }
          ],
          "reviewRequirements": [],
          "errors": [
            {
              "source": {
                "type": "rule",
                "ruleId": "146234"
              },
              "kind": {
                "type": "blank-field",
                "fieldId": "field@decision-credit-score"
              }
            }
          ],
          "priceAdjustments": [],
          "marginAdjustments": [],
          "rateAdjustments": [],
          "finalPriceAdjustments": [],
          "finalMarginAdjustments": [],
          "finalRateAdjustments": [],
          "stipulations": []
        }
      },
      {
        "id": "69ddf4aebb446bb41c3a6c0be4d37a5d",
        "priceScenarioFields": [
          {
            "fieldId": "base-interest-rate",
            "value": {
              "type": "number",
              "value": "5.75"
            }
          },
          {
            "fieldId": "rate-lock-period",
            "value": {
              "type": "duration",
              "count": "30",
              "unit": "days"
            }
          },
          {
            "fieldId": "base-price",
            "value": {
              "type": "number",
              "value": "91.29276428"
            }
          }
        ],
        "calculatedFields": [
          {
            "fieldId": "calc@initial-io-payment",
            "value": {
              "type": "number",
              "value": "2635.42"
            }
          },
          {
            "fieldId": "calc@eresi-dscr-initial-max-ltv",
            "value": {
              "type": "number",
              "value": "75"
            }
          },
          {
            "fieldId": "calc@final-interest-rate",
            "value": {
              "type": "number",
              "value": "5.75"
            }
          },
          {
            "fieldId": "calc@start-interest-rate",
            "value": {
              "type": "number",
              "value": "5.75"
            }
          },
          {
            "fieldId": "calc@initial-mtg-payment",
            "value": {
              "type": "number",
              "value": "2635.42"
            }
          },
          {
            "fieldId": "calc@final-est-front-dti",
            "value": {
              "type": "number",
              "value": "0.264"
            }
          },
          {
            "fieldId": "calc@dti-enum-to-int-conversion",
            "value": None
          },
          {
            "fieldId": "calc@est-dti",
            "value": {
              "type": "number",
              "value": "0.264"
            }
          },
          {
            "fieldId": "calc@initial-pi-payment",
            "value": {
              "type": "number",
              "value": "3209.66"
            }
          },
          {
            "fieldId": "calc@adjusted-interest-rate",
            "value": {
              "type": "number",
              "value": "5.75"
            }
          },
          {
            "fieldId": "calc@1st-lien-est-payment",
            "value": {
              "type": "number",
              "value": "2635.42"
            }
          },
          {
            "fieldId": "calc@pi-payment",
            "value": {
              "type": "number",
              "value": "3209.66"
            }
          },
          {
            "fieldId": "calc@final-est-dti",
            "value": {
              "type": "number",
              "value": "0.264"
            }
          },
          {
            "fieldId": "calc@io-payment",
            "value": {
              "type": "number",
              "value": "2635.42"
            }
          },
          {
            "fieldId": "calc-field@sgcp-investor-connect-purchase-matrix-output",
            "value": None
          },
          {
            "fieldId": "calc@eresi-dscr-final-max-ltv",
            "value": {
              "type": "number",
              "value": "75"
            }
          },
          {
            "fieldId": "calc@eresi-dscr-ltv-calc-2",
            "value": {
              "type": "number",
              "value": "999"
            }
          },
          {
            "fieldId": "calc@start-price",
            "value": {
              "type": "number",
              "value": "91.292765"
            }
          },
          {
            "fieldId": "calc@eresi-dscr-total-leverage-reduction",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc@monthly-mi",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc@dscr",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc@arm-fully-indexed-rate",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc@est-payment",
            "value": {
              "type": "number",
              "value": "2635.42"
            }
          },
          {
            "fieldId": "calc-field@sgcp-investor-connect-refinance-matrix-output",
            "value": None
          },
          {
            "fieldId": "calc@final-est-payment",
            "value": {
              "type": "number",
              "value": "2635.42"
            }
          },
          {
            "fieldId": "calc@est-front-dti",
            "value": {
              "type": "number",
              "value": "0.264"
            }
          },
          {
            "fieldId": "calc@mtg-payment",
            "value": {
              "type": "number",
              "value": "2635.42"
            }
          },
          {
            "fieldId": "calc@final-dscr",
            "value": {
              "type": "number",
              "value": "0"
            }
          },
          {
            "fieldId": "calc@adjusted-rate-lock-period",
            "value": {
              "type": "duration",
              "count": "30",
              "unit": "days"
            }
          },
          {
            "fieldId": "calc@eresi-dscr-ltv-calc-1",
            "value": {
              "type": "number",
              "value": "75"
            }
          },
          {
            "fieldId": "calc@intermediate-rate",
            "value": {
              "type": "number",
              "value": "5.75"
            }
          }
        ],
        "status": {
          "type": "rejected",
          "rejections": [
            {
              "source": {
                "type": "rule",
                "ruleId": "39371"
              },
              "message": "Product is not eligible for the desired loan term."
            },
            {
              "source": {
                "type": "rule",
                "ruleId": "124523"
              },
              "message": "Rate falls below floor allowed."
            },
            {
              "source": {
                "type": "rule",
                "ruleId": "124525"
              },
              "message": "Investment occupancy only. (Your Occupancy: Primary Residence) DSCR documentation type required. (Your Documentation Type: Bank Statements)"
            }
          ],
          "reviewRequirements": [],
          "errors": [
            {
              "source": {
                "type": "rule",
                "ruleId": "146234"
              },
              "kind": {
                "type": "blank-field",
                "fieldId": "field@decision-credit-score"
              }
            }
          ],
          "priceAdjustments": [],
          "marginAdjustments": [],
          "rateAdjustments": [],
          "finalPriceAdjustments": [],
          "finalMarginAdjustments": [],
          "finalRateAdjustments": [],
          "stipulations": []
        }
      }
    ]
  }
}

if __name__ == "__main__":
    # Define your connection string here
    # IMPORTANT: Set the 'SQL_CONNECTION_STRING' environment variable before running.
    # Example (Linux/macOS): export SQL_CONNECTION_STRING="DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=LoanPASS_DB;UID=your_username;PWD=your_password"
    # Example (Windows CMD): set SQL_CONNECTION_STRING="DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=LoanPASS_DB;Trusted_Connection=yes;"
    
    my_connection_string = os.getenv('SQL_CONNECTION_STRING')

    if not my_connection_string:
        raise ValueError("SQL_CONNECTION_STRING environment variable not set. Please set it before running the script.")

    # You can load JSON from a file:
    # with open('your_data.json', 'r') as f:
    #     json_data = json.load(f)

    # Or use the sample_json_data directly
    process_loanpass_json(sample_json_data, my_connection_string)