# AppAssure-Sentinel

Sample code repository designed to accelerate development of Microsoft Sentinel integration solutions. This repository contains Azure Function applications demonstrating different approaches to data ingestion and processing for Sentinel workflows.

## Repository Structure

This repository contains two sample Azure Function applications that serve as templates and learning examples for Sentinel integration development:

### Sample1-SkeletonFunc - Basic Timer-Triggered Function

**Purpose**: A minimal Azure Function template demonstrating the basic structure and timer-based execution pattern.

**Key Features**:
- Timer-triggered Azure Function with 5-second intervals
- Basic logging implementation
- Minimal dependencies (azure-functions only)
- Runs on startup for immediate testing
- Foundation template for building custom Sentinel integrations

**Technical Details**:
- **Runtime**: Python 3.11+ with Azure Functions Runtime v4
- **Trigger**: Timer (CRON: `*/5 * * * * *` - every 5 seconds)
- **Dependencies**: `azure-functions`
- **Logging**: Basic logging with past-due timer detection

**Use Cases**:
- Starting template for new Sentinel integration functions
- Learning basic Azure Function structure and timer triggers
- Foundation for scheduled data collection tasks

### Sample2-IngestFunc - Modern Logs Ingestion API Implementation

**Purpose**: Demonstrates modern data ingestion into Azure Monitor using the Logs Ingestion API with Data Collection Rules (DCR) and managed identity authentication.

**Key Features**:
- Timer-triggered function (10-second intervals) for automated data submission
- Modern Logs Ingestion API implementation using Data Collection Rules
- Azure managed identity authentication (DefaultAzureCredential)
- Sample data structure with nested JSON objects
- Comprehensive error handling and logging
- Production-ready implementation following current best practices

**Technical Details**:
- **Runtime**: Python 3.x with Azure Functions Runtime v4
- **Trigger**: Timer (CRON: `*/10 * * * * *` - every 10 seconds)
- **API**: Azure Monitor Logs Ingestion API (Modern)
- **Authentication**: Azure managed identity with DefaultAzureCredential
- **Dependencies**: 
  - `azure-functions` - Core Azure Functions runtime
  - `azure-identity` - Azure authentication libraries  
  - `azure-monitor-ingestion` - Modern logs ingestion client

**Data Flow**:
1. Timer triggers function execution every 10 seconds
2. Sample log data is prepared with timestamp, computer, and additional context
3. DefaultAzureCredential authenticates using managed identity or environment variables
4. LogsIngestionClient uploads data to specified Data Collection Rule and stream
5. Response status and errors are logged for monitoring

**Configuration Required**:
- `endpoint_uri`: Data Collection Endpoint (DCE) ingestion URL  
  - Format: `https://<your-dce-name>.ingest.monitor.azure.com`
- `dcr_immutableid`: Data Collection Rule immutable ID
  - Format: `dcr-00000000000000000000000000000000`
- `stream_name`: Stream name in the DCR targeting destination table
  - Format: `Custom-<your-customtablename>`
- **Azure Managed Identity**: Function app must have appropriate permissions to the DCR

**Sample Data Structure**:
```json
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
}
```

**Security & Best Practices**:
- Uses **Modern Logs Ingestion API** (recommended approach)
- Leverages Azure managed identity for secure, credential-less authentication
- Supports Data Collection Rules for schema validation and transformation
- Includes detailed logging with timestamps for troubleshooting

**Setup Requirements**:
1. Create Data Collection Endpoint (DCE) in Azure
2. Create Data Collection Rule (DCR) with appropriate schema and destination table
3. Configure Function App managed identity with DCR permissions
4. Update configuration variables in function code

## Getting Started

1. **Prerequisites**:
   - Azure subscription with Log Analytics workspace (for Sample2)
   - Azure Functions Core Tools v4
   - Python 3.11+ runtime
   - Visual Studio Code with Azure Functions extension (recommended)

2. **Local Development**:
   ```bash
   # Navigate to desired sample
   cd Sample1-SkeletonFunc  # or Sample2-IngestFunc
   
   # Install dependencies
   py -m venv .venv
   .venv\Scripts\activate
   .venv\Scripts\python -m pip install -r requirements.txt
   
   # Run locally
   func start
   ```

3. **Deployment**:
   - Deploy using Azure Functions Core Tools, VS Code, or Azure Portal
   - Configure application settings for production credentials
   - Monitor function execution through Azure Portal or Application Insights

## Learning Path

1. **Start with Sample1-SkeletonFunc**: Understand basic Azure Function structure and timer triggers
2. **Progress to Sample2-IngestFunc**: Learn data ingestion patterns and Azure Monitor integration
3. **Switch to Legacy-HttpDataCollectorApi brnach**: Review the legacy code ingesting data with HTTP Data Collector API and compare that to the modern Log Ingestion API 

## References

- [Azure Functions Python Developer Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Azure Monitor Logs Ingestion API](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/logs-ingestion-api-overview)
- [Data Collection Rules in Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/data-collection-rule-overview)
- [Azure Identity Library for Python](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme)
- [Azure Sentinel Data Connectors](https://github.com/Azure/Azure-Sentinel/tree/master/DataConnectors)
- [Azure Monitor Ingestion Client Library](https://learn.microsoft.com/en-us/python/api/overview/azure/monitor-ingestion-readme)
