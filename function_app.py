import datetime
import logging
import os
import requests
import time
import pytz
import pyodbc
import json
import datetime
from azure.storage.blob import BlobServiceClient
import azure.functions as func

storage_connection_string = 'DefaultEndpointsProtocol=https;AccountName=lendzdialpadscripts;AccountKey=XLwTu4FtAwh9r2mYUpkPdMOj16uD4RVbR5ivU3/XGDC3rINroLNkqQul2U216kFhhy6zJJ2U2FFP+AStGRx1WA==;EndpointSuffix=core.windows.net'
container_name = 'calls'
api_endpoint = 'https://dialpad.com/api/v2/call'
api_token = 'JzEWbTUAQ7Msvd2Qha58hk2dmthVdFVmrgmTGVXg2RbyTBU4BAzsBDk6x8EKc6YxC7XrLxMbvjNY37pWhtDC8mLRkuUFyaU7YjGD'
MAX_REQUESTS_PER_MINUTE = 1000  # Setting a slightly lower limit for safety
MIN_DELAY_SECONDS = 60.0 / MAX_REQUESTS_PER_MINUTE
connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:lendz.database.windows.net,1433;Database=Lexi_DEV;Uid=lexi;Pwd=H3n4y*_D@;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

app = func.FunctionApp()

@app.timer_trigger(schedule="0 5 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def get_dialpad_calls(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    dialpad_api_request()

def convert_milliseconds_to_datetime(milliseconds):
    """
    Converts milliseconds since the Unix epoch to a datetime object in UTC.

    Args:
        milliseconds (float): Milliseconds since the Unix epoch.

    Returns:
        datetime.datetime: A datetime object representing the time in UTC.
    """
    # Convert milliseconds to seconds.
    seconds = milliseconds / 1000.0
    # Create a datetime object from the timestamp (in UTC).
    utc_time = datetime.datetime.utcfromtimestamp(seconds)
    return utc_time

def write_dialpad_data_to_azure_sql(json_data, connection_string):
    """
    Writes Dialpad call data from a JSON structure to an Azure SQL database using a single bulk insert.

    Args:
        json_data (str): A JSON string containing the call data.  The expected structure
            is a dictionary with an "items" key containing a list of call records.
        connection_string (str): The connection string for the Azure SQL database.
    """
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format.  Details: {e}")
        return

    if not isinstance(data, dict) or "items" not in data:
        print("Error: Invalid JSON structure.  The JSON data should be a dictionary"
              " containing an 'items' key with a list of call records.")
        return

    items = data["items"]
    if not isinstance(items, list):
        print("Error: The 'items' key should contain a list of call records.")
        return

    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
    except pyodbc.Error as e:
        print(f"Error: Could not connect to the database.  Details: {e}")
        return

    # Define the table name
    table_name = "DialpadCalls"

    # Construct the INSERT statement.  It's good practice to explicitly name the columns.
    insert_statement = f"""
    INSERT INTO {table_name} (
        call_id, contact_email, contact_id, contact_name, contact_phone, contact_type,
        date_connected, date_ended, date_started, direction, duration,
        entry_point_target_id, event_timestamp, external_number, internal_number,
        is_transferred, mos_score, proxy_target_id, state, target_email,
        target_id, target_name, target_phone, target_type, total_duration, was_recorded
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
    """

    # Prepare the data for bulk insert.  This is a list of tuples, where each tuple
    # represents a row to be inserted.
    rows = []
    for item in items:
        try:
            # Handle the nested 'contact' and 'target' objects.  Extract the values.
            contact_data = item.get("contact", {})
            target_data = item.get("target", {})
            entry_point_target_data = item.get("entry_point_target", {})

            # Convert timestamps to datetime objects using the helper function.  Use None if the timestamp is missing.
            date_ended = convert_milliseconds_to_datetime(float(item.get("date_ended"))) if item.get("date_ended") else None
            date_started = convert_milliseconds_to_datetime(float(item.get("date_started"))) if item.get("date_started") else None
            event_timestamp = convert_milliseconds_to_datetime(float(item.get("event_timestamp"))) if item.get("event_timestamp") else None
            date_connected = None  # The example JSON doesn't have date_connected.
            if "date_rang" in item:
                date_connected = convert_milliseconds_to_datetime(float(item["date_rang"]))

            # Prepare the values for the INSERT statement.  The order must match the
            # order of the columns in the INSERT statement.
            values = (
                item.get("call_id"),
                contact_data.get("email"),
                contact_data.get("id"),
                contact_data.get("name"),
                contact_data.get("phone"),
                contact_data.get("type"),
                date_connected,
                date_ended,
                date_started,
                item.get("direction"),
                item.get("duration"),
                entry_point_target_data.get("id"),
                event_timestamp,
                item.get("external_number"),
                item.get("internal_number"),
                item.get("is_transferred"),
                item.get("mos_score"),
                None,  # proxy_target_id -  The example JSON doesn't have proxy_target.
                item.get("state"),
                target_data.get("email"),
                target_data.get("id"),
                target_data.get("name"),
                target_data.get("phone"),
                target_data.get("type"),
                item.get("total_duration"),
                item.get("was_recorded"),
            )
            rows.append(values)
        except Exception as e:
            print(f"Error processing record for call_id: {item.get('call_id')}. Details: {e}")
            print(f"Problematic data: {item}")
            #  Don't rollback here,  process the rest and log the errors

    # Perform the bulk insert if there are rows to insert.
    if rows:
        try:
            cursor.executemany(insert_statement, rows)
            conn.commit()
            print(f"Successfully inserted {len(rows)} records into {table_name}")
        except pyodbc.Error as e:
            print(f"Error performing bulk insert. Details: {e}")
            conn.rollback()  # Rollback the entire transaction on error
    else:
        print("No data to insert.")

    # Close the database connection.  Important to free up resources.
    cursor.close()
    conn.close()
    print("Successfully closed the database connection.")


def dialpad_api_request():
    # Load environment variables
    # api_endpoint = os.getenv('API_ENDPOINT')
    # api_token = os.getenv('API_TOKEN')
    # storage_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    # container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
    next_cursor = None
    request_count = 0
    start_time = time.time()

    # Initialize BlobServiceClient outside the loop
    try:
        blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    except Exception as e:
        logging.error(f'Error creating BlobServiceClient: {e}')
        return  # Exit if BlobServiceClient cannot be created

    # Get current time in seconds since epoch
    current_time = time.time()
    # Subtract 2 hours (2 * 3600 seconds)
    two_hours_ago = current_time - (2 * 3600)
    # Convert to milliseconds
    two_hours_ago_millis = int(two_hours_ago * 1000)
    started_after_timestamp = two_hours_ago_millis
    
    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if request_count >= MAX_REQUESTS_PER_MINUTE and elapsed_time < 60:
            remaining_time = 60 - elapsed_time
            logging.warning(f'Rate limit reached. Waiting for {remaining_time:.2f} seconds.')
            time.sleep(remaining_time)
            start_time = time.time()
            request_count = 0
        elif elapsed_time >= 60:
            start_time = time.time()
            request_count = 0

        current_endpoint = api_endpoint
        params = {'started_after': started_after_timestamp}
        if next_cursor:
            params['cursor'] = next_cursor
            logging.info(f'Making API request {request_count + 1} with cursor: {next_cursor} and started_after: {started_after_timestamp}')
        else:
            logging.info(f'Making initial API request {request_count + 1} with started_after: {started_after_timestamp}.')

        headers = {'Authorization': f'Bearer {api_token}'}
        try:
            response = requests.get(current_endpoint, headers=headers, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes

            logging.info('API request successful.')
            try:
                response_json = response.json()

                # Generate a unique blob name for each response
                blob_name = f"dialpad_response_page_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{request_count}.json"

                # Get BlobClient inside the loop
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

                # Upload the current JSON response to Azure Blob Storage
                blob_client.upload_blob(json.dumps(response_json), overwrite=True)
                logging.info(f'Response for page {request_count} uploaded to blob storage as {blob_name}')
                # Write the JSON data to Azure SQL database
                write_dialpad_data_to_azure_sql(json.dumps(response_json), connection_string)
                # Check if there's a next cursor
                if 'cursor' in response_json and response_json['cursor']:
                    next_cursor = response_json['cursor']
                    logging.info(f'Next cursor found: {next_cursor}')
                else:
                    logging.info('No more cursors found. Pagination complete.')
                    break  # Exit the loop if no cursor is present
            except json.JSONDecodeError:
                logging.error('Failed to decode JSON response.')
                break # Exit the loop if JSON decoding fails

        except requests.exceptions.RequestException as e:
            logging.error(f'API request failed: {e}')
            break # Exit the loop on request error
        finally:
            request_count += 1
            time.sleep(MIN_DELAY_SECONDS) # Add a small delay between requests

    logging.info('Pagination process completed.')



if __name__ == "__main__":
    dialpad_api_request()


