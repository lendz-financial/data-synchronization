# import logging
# import azure.functions as func

# app = func.FunctionApp()

# @app.timer_trigger(schedule="0 5 * * * *", arg_name="myTimer", run_on_startup=False,
#               use_monitor=False) 
# def get_dialpad_calls(myTimer: func.TimerRequest) -> None:
#     if myTimer.past_due:
#         logging.info('The timer is past due!')

#     logging.info('Python timer trigger function executed.')

# https://lendzdialpadscripts.blob.core.windows.net/calls/?sv=2022-11-02&ss=b&srt=co&se=2025-05-17T21%3A55%3A18Z&sp=rwl&sig=bWZlUqB2uXUKEmixW41x6PU%2FHTWagyqet4vn47cFVnk%3D


import datetime
import logging
import os
import requests
import time
import pytz
import json
from azure.storage.blob import BlobServiceClient
import azure.functions as func

storage_connection_string = 'DefaultEndpointsProtocol=https;AccountName=lendzdialpadscripts;AccountKey=XLwTu4FtAwh9r2mYUpkPdMOj16uD4RVbR5ivU3/XGDC3rINroLNkqQul2U216kFhhy6zJJ2U2FFP+AStGRx1WA==;EndpointSuffix=core.windows.net'
container_name = 'calls'
api_endpoint = 'https://dialpad.com/api/v2/call'
api_token = 'JzEWbTUAQ7Msvd2Qha58hk2dmthVdFVmrgmTGVXg2RbyTBU4BAzsBDk6x8EKc6YxC7XrLxMbvjNY37pWhtDC8mLRkuUFyaU7YjGD'
MAX_REQUESTS_PER_MINUTE = 1000  # Setting a slightly lower limit for safety
MIN_DELAY_SECONDS = 60.0 / MAX_REQUESTS_PER_MINUTE

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

    # Define the target date and time in Eastern Time
    eastern_tz = pytz.timezone('America/New_York')
    may_first_et = eastern_tz.localize(datetime.datetime(2025, 5, 1, 0, 0, 0))

    # Convert the Eastern Time to UTC timestamp (seconds)
    #started_after_timestamp = int(may_first_et.astimezone(pytz.utc).timestamp())
    started_after_timestamp = 1746057600000

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


