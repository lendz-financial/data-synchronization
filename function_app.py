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
connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:lendz.database.windows.net,1433;Database=Lexi;Uid=lexi;Pwd=H3n4y*_D@;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
#connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:lendz.database.windows.net,1433;Database=Lexi;Uid=lexi;Pwd=H3n4y*_D@;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

app = func.FunctionApp()

logging.basicConfig(level=logging.INFO) 

@app.timer_trigger(schedule="0 5 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def get_dialpad_calls(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')

    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', time.time())
    dialpad_api_request()
    
    
@app.timer_trigger(schedule="0 5 * * * *", arg_name="myTranscriptTimer", run_on_startup=True,
              use_monitor=False) 
def get_dialpad_call_transcripts(myTranscriptTimer: func.TimerRequest) -> None:
    if myTranscriptTimer.past_due:
        logging.info('The transcripts timer is past due!')

    logging.info('Python timer transcripts trigger function ran at %s', time.time())
    get_remaining_transcripts_in_batches() 

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
    Writes Dialpad call data from a JSON structure to an Azure SQL database using a bulk insert.

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
    MERGE {table_name} AS target
    USING (SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) AS source
           (call_id, contact_email, contact_id, contact_name, contact_phone, contact_type,
            date_connected, date_ended, date_started, direction, duration,
            entry_point_target_id, event_timestamp, external_number, internal_number,
            is_transferred, mos_score, proxy_target_id, state, target_email,
            target_id, target_name, target_phone, target_type, total_duration, was_recorded)
    ON (target.call_id = source.call_id)
    WHEN MATCHED THEN
        UPDATE SET
            target.contact_email = source.contact_email,
            target.contact_id = source.contact_id,
            target.contact_name = source.contact_name,
            target.contact_phone = source.contact_phone,
            target.contact_type = source.contact_type,
            target.date_connected = source.date_connected,
            target.date_ended = source.date_ended,
            target.date_started = source.date_started,
            target.direction = source.direction,
            target.duration = source.duration,
            target.entry_point_target_id = source.entry_point_target_id,
            target.event_timestamp = source.event_timestamp,
            target.external_number = source.external_number,
            target.internal_number = source.internal_number,
            target.is_transferred = source.is_transferred,
            target.mos_score = source.mos_score,
            target.proxy_target_id = source.proxy_target_id,
            target.state = source.state,
            target.target_email = source.target_email,
            target.target_id = source.target_id,
            target.target_name = source.target_name,
            target.target_phone = source.target_phone,
            target.target_type = source.target_type,
            target.total_duration = source.total_duration,
            target.was_recorded = source.was_recorded
    WHEN NOT MATCHED THEN
        INSERT (call_id, contact_email, contact_id, contact_name, contact_phone, contact_type,
                date_connected, date_ended, date_started, direction, duration,
                entry_point_target_id, event_timestamp, external_number, internal_number,
                is_transferred, mos_score, proxy_target_id, state, target_email,
                target_id, target_name, target_phone, target_type, total_duration, was_recorded)
        VALUES (source.call_id, source.contact_email, source.contact_id, source.contact_name, source.contact_phone, source.contact_type,
                source.date_connected, source.date_ended, source.date_started, source.direction, source.duration,
                source.entry_point_target_id, source.event_timestamp, source.external_number, source.internal_number,
                source.is_transferred, source.mos_score, source.proxy_target_id, source.state, source.target_email,
                source.target_id, source.target_name, source.target_phone, source.target_type, source.total_duration, source.was_recorded);
    """

    # Prepare the data for bulk insert.  This involves converting each item
    # into a tuple of values that matches the order of columns in the INSERT statement.
    values_list = []
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
            date_connected = None
            if "date_rang" in item:
                date_connected = convert_milliseconds_to_datetime(float(item["date_rang"]))

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
                None,  # proxy_target_id
                item.get("state"),
                target_data.get("email"),
                target_data.get("id"),
                target_data.get("name"),
                target_data.get("phone"),
                target_data.get("type"),
                item.get("total_duration"),
                item.get("was_recorded"),
            )
            values_list.append(values)  # Append the tuple to the list

        except Exception as e:
            print(f"Error processing record for call_id: {item.get('call_id')}.  Skipping. Details: {e}")
            continue  # Skip the current record and continue to the next.

    try:
        # Execute the bulk insert using executemany().
        cursor.executemany(insert_statement, values_list)
        conn.commit()
        print(f"Successfully inserted {len(values_list)} records into {table_name}")

    except pyodbc.Error as e:
        print(f"Error performing bulk insert. Details: {e}")
        conn.rollback()

    finally:
        # Close the database connection.  Important to free up resources.
        cursor.close()
        conn.close()
        print("Successfully closed the database connection.")
        
def dialpad_api_request(api_start_time=None, api_end_time=None):
    # Load environment variables
    # api_endpoint = os.getenv('API_ENDPOINT')
    # api_token = os.getenv('API_TOKEN')
    # storage_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    # container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
    next_cursor = None
    request_count = 0
    start_time = time.time()

    api_start_time = api_start_time if api_start_time is not None else time.time()
    # Get current time in seconds since epoch
    # Subtract 2 hours (2 * 3600 seconds)
    two_hours_ago = api_start_time - (2 * 3600)
    # Convert to milliseconds
    two_hours_ago_millis = int(two_hours_ago * 1000)
    started_after_timestamp = two_hours_ago_millis
    # Initialize BlobServiceClient outside the loop
    try:
        blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    except Exception as e:
        logging.error(f'Error creating BlobServiceClient: {e}')
        return  # Exit if BlobServiceClient cannot be created
    
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

        if api_end_time is not None:
            params['started_before'] = api_end_time*1000

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


def get_and_update_transcripts(call_ids, connection_string, api_token):
    """
    Downloads transcripts for a list of call_ids and updates the Azure SQL database.

    Args:
        call_ids (list): A list of call_ids to fetch transcripts for.
        connection_string (str): The connection string for the Azure SQL database.
        api_token (str): The Dialpad API token for authentication.
    """
    transcript_api_endpoint = 'https://dialpad.com/api/v2/transcripts/'
    headers = {'Authorization': f'Bearer {api_token}'}

    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        update_count = 0
        for call_id in call_ids:
            try:
                transcript_url = f"{transcript_api_endpoint}{call_id}"
                response = requests.get(transcript_url, headers=headers)
                response.raise_for_status()

                transcript_data = response.json()
                if 'lines' in transcript_data:
                    # Filter for 'transcript' type lines and join their content
                    transcript_lines = [line['content'] for line in transcript_data['lines'] if line.get('type') == 'transcript']
                    full_transcript = "\n".join(transcript_lines)
                    
                    # Update the database
                    update_statement = """
                    UPDATE DialpadCalls
                    SET transcript = ?
                    WHERE call_id = ?
                    """
                    cursor.execute(update_statement, full_transcript, call_id)
                    update_count += 1
                else:
                    logging.warning(f"No 'lines' found in transcript data for call_id: {call_id}")

            except requests.exceptions.RequestException as e:
                logging.error(f'Failed to get transcript for call_id {call_id}: {e}')
                continue
            except json.JSONDecodeError:
                logging.error(f'Failed to decode JSON response for transcript for call_id {call_id}.')
                continue
            
            # Add a small delay to avoid hitting rate limits on the transcripts API
            time.sleep(MIN_DELAY_SECONDS)
        
        conn.commit()
        logging.info(f"Successfully updated {update_count} call transcripts.")
        
    except pyodbc.Error as e:
        logging.error(f"Database error while updating transcripts: {e}")
        conn.rollback()
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()
            
def get_remaining_transcripts_in_batches():
    batch_size = 100   
    try:
        logging.info("Connecting to the database to retrieve remaining call IDs.")
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        query = """
        SELECT
        call_id
        FROM DialpadCalls
        WHERE
        date_started >= DATEADD(minute, -20, GETDATE())
        AND
        (transcript IS NULL OR trim(transcript) = '')        
        """
        cursor.execute(query)
        call_ids_to_process = [row.call_id for row in cursor.fetchall()]
        
        if not call_ids_to_process:
            logging.info("No new calls found  needing a transcript.")
            return

        logging.info(f"Found {len(call_ids_to_process)} remaining calls to process.")

        # Process call IDs in batches
        for i in range(0, len(call_ids_to_process), batch_size):
            batch = call_ids_to_process[i:i + batch_size]
            logging.info(f"Processing batch {i // batch_size + 1} of size {len(batch)}.")
            get_and_update_transcripts(batch, connection_string, api_token)
            
    except pyodbc.Error as e:
        logging.error(f"Database error in get_remaining_transcripts_in_batches: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()
        logging.info("Finished processing  call transcripts.")
        
                    
#if __name__ == "__main__":
    # Define Eastern Time Zone
    # eastern = pytz.timezone('America/New_York')
    # dt = eastern.localize(datetime.datetime(2025, 5, 5, 0, 0))
    # epoch_time = int(dt.timestamp())
    # print(epoch_time)
    # api_end_time = int((eastern.localize(datetime.datetime(2025, 5, 9, 0, 0))).timestamp())
    # print(api_end_time)
    # dialpad_api_request(api_start_time=epoch_time, api_end_time=api_end_time)
    
    #get_remaining_transcripts_in_batches()
