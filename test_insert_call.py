import json
import pyodbc
from datetime import datetime
import pytz

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
    utc_time = datetime.utcfromtimestamp(seconds)
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


if __name__ == "__main__":
    #  Replace with your actual Azure SQL connection string.
    connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:lendz.database.windows.net,1433;Database=Lexi_DEV;Uid=lexi;Pwd=H3n4y*_D@;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    #  Replace with your JSON data.  For testing, you can use the sample data
    #  provided in the problem description, or load it from a file.
    json_data = """
    {
        "cursor": "76172bbc9c14e876fcc93f9345d08ce0-_-0",
        "items": [
            {
                "call_id": "4756071778664448",
                "contact": {
                    "email": "",
                    "id": "6648290999582720",
                    "name": "Newtonville MA",
                    "phone": "+18572321711",
                    "type": "local"
                },
                "date_ended": "1739834613505",
                "date_started": "1739834608997",
                "direction": "inbound",
                "duration": 0,
                "entry_point_target": {},
                "event_timestamp": "1747322231916",
                "external_number": "+18572321711",
                "group_id": "Office:5231288289411072",
                "internal_number": "+13059010714",
                "is_transferred": false,
                "mos_score": 4.41,
                "proxy_target": {},
                "state": "hangup",
                "target": {
                    "email": "",
                    "id": "5231288289411072",
                    "name": "Lendz Financial",
                    "phone": "+13059010714",
                    "type": "office"
                },
                "total_duration": 4508.166,
                "was_recorded": false
            },
            {
                "call_id": "5786930812076032",
                "contact": {
                    "email": "",
                    "id": "6585648819290112",
                    "name": "(305) 609-8131",
                    "phone": "+13056098131",
                    "type": "local"
                },
                "date_ended": "1739828590144",
                "date_started": "1739828580235",
                "direction": "inbound",
                "duration": 0,
                "entry_point_target": {},
                "event_timestamp": "1747322232234",
                "external_number": "+13056098131",
                "group_id": "Office:5231288289411072",
                "internal_number": "+13059010714",
                "is_transferred": true,
                "mos_score": 4.41,
                "proxy_target": {},
                "state": "hangup",
                "target": {
                    "email": "",
                    "id": "5231288289411072",
                    "name": "Lendz Financial",
                    "phone": "+13059010714",
                    "type": "office"
                },
                "total_duration": 9908.737000000001,
                "was_recorded": false
            },
            {
                "call_id": "6401638543966208",
                "contact": {
                    "email": "",
                    "id": "5720699479572480",
                    "name": "Nadia Casales",
                    "phone": "+13058338579",
                    "type": "local"
                },
                "date_ended": "1739824055505",
                "date_rang": "1739824025896",
                "date_started": "1739824025058",
                "direction": "inbound",
                "duration": 0,
                "entry_point_call_id": "6443115512905728",
                "entry_point_target": {
                    "email": "",
                    "id": "5231288289411072",
                    "name": "Lendz Financial",
                    "phone": "+13059010714",
                    "type": "office"
                },
                "event_timestamp": "1747322232509",
                "external_number": "+13058338579",
                "group_id": "Office:5231288289411072",
                "internal_number": "+13052398796",
                "is_transferred": false,
                "mos_score": 4.5,
                "proxy_target": {},
                "state": "hangup",
                "target": {
                    "email": "nicolas.friedmann@lendzfinancial.com",
                    "id": "5821975242293248",
                    "name": "Nicolas Friedmann",
                    "phone": "+13052398796",
                    "type": "user"
                },
                "total_duration": 30447.371,
                "was_recorded": false
            },
            {
                "call_id": "4714734773649408",
                "contact": {
                    "email": "",
                    "id": "5720699479572480",
                    "name": "Nadia Casales",
                    "phone": "+13058338579",
                    "type": "local"
                },
                "date_ended": "1739824030862",
                "date_rang": "1739824025732",
                "date_started": "1739824024915",
                "direction": "inbound",
                "duration": 0,
                "entry_point_call_id": "6443115512905728",
                "entry_point_target": {
                    "email": "",
                    "id": "5231288289411072",
                    "name": "Lendz Financial",
                    "phone": "+13059010714",
                    "type": "office"
                },
                "event_timestamp": "1747322232803",
                "external_number": "+13058338579",
                "group_id": "Office:5231288289411072",
                "internal_number": "+13053597909",
                "is_transferred": false,
                "mos_score": 4.5,
                "proxy_target": {},
                "state": "hangup",
                "target": {
                    "email": "traci.levine@lendzfinancial.com",
                    "id": "6037819886878720",
                    "name": "Traci Levine",
                    "phone": "+13053597909",
                    "type": "user"
                },
                "total_duration": 5946.995,
                "was_recorded": false
            }
        ]
    }
    """
    write_dialpad_data_to_azure_sql(json_data, connection_string)
