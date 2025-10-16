# information needed to send data to the DCR endpoint
#TODO: Update DCE DCR and table details
endpoint_uri = "https://<your-dce-name>.ingest.monitor.azure.com" # logs ingestion endpoint of the DCR
dcr_immutableid = "dcr-00000000000000000000000000000000" # immutableId property of the Data Collection Rule
stream_name = "Custom-<your-customtablename>" #name of the stream in the DCR that represents the destination table

import azure.functions as func
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.core.exceptions import HttpResponseError
import datetime
import json
import logging

app = func.FunctionApp()

@app.timer_trigger(schedule="*/5 * * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    timestamp = datetime.datetime.now()
    logging.info(f'[TIMER] Python timer trigger function begin at {timestamp}')

    if myTimer.past_due:
        logging.info('[TIMER] The timer is past due!')

    # Sample data to send to the DCR
    body = [
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
        # authenticate and create client
        credential = DefaultAzureCredential() # use this line to authenticate if the environment variable AZURE_CLIENT_ID is set
        logging.info('[TIMER] DefaultAzureCredential initialized')
        client = LogsIngestionClient(endpoint=endpoint_uri, credential=credential, logging_enable=True)

        # upload data to the DCR
        logging.info(f'[TIMER] Uploading {len(body)} records to DCR {dcr_immutableid} at {endpoint_uri}')
        client.upload(rule_id=dcr_immutableid, stream_name=stream_name, logs=body)
    except HttpResponseError as e:
        logging.info(f"Upload failed: {e}")

    timestamp = datetime.datetime.now()
    logging.info(f'[TIMER] Python timer trigger function end at {timestamp}')