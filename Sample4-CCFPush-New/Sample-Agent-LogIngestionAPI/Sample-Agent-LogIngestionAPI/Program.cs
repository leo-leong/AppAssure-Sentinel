/*
 * Sample code for uploading custom logs to Azure Monitor using the Logs Ingestion API.
 * Refer to the documentation for more details: https://learn.microsoft.com/en-us/azure/azure-monitor/logs/tutorial-logs-ingestion-code?tabs=net
 */

using Azure.Core;
using Azure.Identity;
using Azure.Monitor.Ingestion;

// Initialize variables
var endpoint = new Uri("https://my-url.monitor.azure.com");
var ruleId = "dcr-00000000000000000000000000000000";
var streamName = "Custom-MyTableRawData";

// Create credential and client
var credential = new DefaultAzureCredential();
LogsIngestionClient client = new LogsIngestionClient(endpoint, credential);

DateTime currentTime = DateTime.UtcNow;

// Use BinaryData to serialize instances of an anonymous type into JSON
BinaryData data = BinaryData.FromObjectAsJson(
   new[] {
    new
    {
       Time = currentTime,
       Computer = "Computer1",
       AdditionalContext = new
       {
         InstanceName = "user1",
        TimeZone = "Pacific Time",
        Level = 4,
        CounterName = "AppMetric1",
        CounterValue = 15.3
       }
    },
    new
    {
       Time = currentTime,
       Computer = "Computer2",
       AdditionalContext = new
       {
        InstanceName = "user2",
        TimeZone = "Central Time",
        Level = 3,
        CounterName = "AppMetric1",
        CounterValue = 23.5
       }
    },
   }
);

// Upload logs
try
{
    //** ===== START: Use this block of code to upload uncompressed data.
    var response = await client.UploadAsync(ruleId, streamName, RequestContent.Create(data)).ConfigureAwait(false);
    if (response.IsError)
    {
        throw new Exception(response.ToString());
    }
    //** ===== End: code block to upload uncompressed data.

}
catch (Exception ex)
{
    Console.WriteLine("Upload failed with Exception: " + ex.Message);
}
