# Legacy code for uploading logs to Azure Monitor using HTTP Data Collector API
# Refer step by step instructions, refer:
#     https://learn.microsoft.com/en-us/previous-versions/azure/azure-monitor/logs/data-collector-api?tabs=python
# Additional sample Function App Python code template:
#     https://github.com/Azure/Azure-Sentinel/blob/master/DataConnectors/Templates/Connector_REST_API_AzureFunctionApp_template/Template_REST_API_AzureFunction_App_Code/Template_REST_API_Function_App_Python/Template_REST_API_Function_App_Python.py
# Reference to the legacy HTTP Data Collector API 
#     https://learn.microsoft.com/en-us/rest/api/loganalytics/create-request
endpoint_uri = 'https://<Your-Workspace-ID>.ods.opinsights.azure.com/api/logs?api-version=2016-04-01' # this is HTTP endpoint for legacy Log Analytics workspace ingestion
log_type = '<Your-Custom-Table-Name>'  # name of the custom table
workspace_id = '<Your-Workspace-ID>' # Your Log Analytics workspace ID
shared_key = '<Your-Shared-Key>' # Your Log Analytics workspace primary key

import azure.functions as func
from azure.core.exceptions import HttpResponseError
import json
import requests
import hashlib
import hmac
import base64
from datetime import datetime
import logging

app = func.FunctionApp()

@app.timer_trigger(schedule="*/10 * * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    timestamp = datetime.datetime.now()
    logging.info(f'[TIMER] Python timer trigger function begin at {timestamp}')

    if myTimer.past_due:
        logging.info('[TIMER] The timer is past due!')

    # Sample data to send to the Log Analytics
    log_data = [
        {
            "Time": "2023-03-12T15:04:48.423211Z",
            "Computer": "Computer1",
            "AdditionalContext": {
                "InstanceName": "user1",
                "TimeZone": "Pacific Time",
                "Level": 4,
                "CounterName": "AppMetric2",
                "CounterValue": 35.3    
            }
        },
        {
            "Time": "2023-03-12T15:04:48.794972Z",
            "Computer": "Computer2",
            "AdditionalContext": {
                "InstanceName": "user2",
                "TimeZone": "Central Time",
                "Level": 3,
                "CounterName": "AppMetric2",
                "CounterValue": 43.5     
            }
        }
    ]

    try:       
        # Convert log data to JSON
        body = json.dumps(log_data)

        # Post the data
        post_data(workspace_id, shared_key, log_type, body)
    except HttpResponseError as e:
        logging.info(f"Upload failed: {e}")

        
    timestamp = datetime.datetime.now()
    logging.info(f'[TIMER] Python timer trigger function end at {timestamp}')



# **Build the signature**
def build_signature(workspace_id, shared_key, date, content_length, method, content_type, resource):
    x_headers = f'x-ms-date:{date}'
    string_to_hash = f"{method}\n{content_length}\n{content_type}\n{x_headers}\n{resource}"
    bytes_to_hash = bytes(string_to_hash, encoding="utf-8")
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
    return f"SharedKey {workspace_id}:{encoded_hash}"

# **Send data to Azure Monitor**
def post_data(workspace_id, shared_key, log_type, body):
    method = 'POST'
    content_type = 'application/json'
    resource = f'/api/logs'
    rfc1123date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(body)
    signature = build_signature(workspace_id, shared_key, rfc1123date, content_length, method, content_type, resource)
    uri = f'https://{workspace_id}.ods.opinsights.azure.com{resource}?api-version=2016-04-01'

    headers = {
        'Content-Type': content_type,
        'Authorization': signature,
        'Log-Type': log_type,
        'x-ms-date': rfc1123date
    }

    response = requests.post(uri, data=body, headers=headers)
    if response.status_code >= 200 and response.status_code <= 299:
        logging.info('Data posted successfully!')
    else:
        logging.info(f'Failed to post data: {response.status_code}, {response.text}')


