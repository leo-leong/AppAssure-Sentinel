# AppAssure-Sentinel

Sample code repository designed to accelerate development of Microsoft Sentinel integration solutions. This repository contains Azure Function applications and Codeless Connector Framework (CCF) solutions demonstrating different approaches to data ingestion and processing for Sentinel workflows.

## Repository Structure

This repository contains four sample implementations organized into Azure Functions and CCF Connector solutions that serve as templates and learning examples for Sentinel integration development:

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
3. **Explore Sample3-CCF-New**: Understand pull-based CCF connectors with API polling
4. **Study Sample4-CCFPush-New**: Learn push-based CCF connectors with agent implementation
5. **Switch to Legacy-HttpDataCollectorApi branch**: Review the legacy code ingesting data with HTTP Data Collector API and compare that to the modern Log Ingestion API

---

## CCF Connector Solutions

### Sample3-CCF-New - Pull-Based Data Connector

**Purpose**: Demonstrates a **CCF Pull Connector** (RestApiPoller) that actively polls an external API endpoint to retrieve logs and ingest them into Microsoft Sentinel.

**Key Features**:
- RestApiPoller connector that polls external APIs on schedule
- JWT token-based authentication with OAuth2 endpoint
- Offset-based pagination support
- Configurable rate limiting and retry logic
- KQL-based data transformation
- Automated deployment via ARM templates

**Technical Details**:
- **Connector Type**: Customizable CCF Connector (RestApiPoller)
- **Authentication**: JWT Token from OAuth2 endpoint
- **API Configuration**:
  - Query Window: 5 minutes
  - Rate Limit: 5 QPS (queries per second)
  - Retry Count: 3 attempts
  - Timeout: 20 seconds
  - Pagination: Offset-based with 50 items per page
- **Target Table**: `AppAssure-SampleIngestFuncLogs_CL`

**Architecture Components**:
1. **Connector Definition**: UI configuration with identity provider and token authentication
2. **Poller Configuration**: API endpoint settings, authentication, and pagination rules
3. **Data Collection Rule (DCR)**: Schema definition and KQL transformation
4. **Log Analytics Table**: Custom table with TimeGenerated, Time, Computer, and AdditionalContext fields

**Data Schema**:
```json
{
    "Time": "datetime",
    "Computer": "string",
    "AdditionalContext": {
        // Dynamic JSON object
    }
}
```

**Data Flow**:
1. Connector polls external API every 5 minutes
2. Authenticates using JWT token from OAuth2 endpoint
3. Retrieves events with offset-based pagination
4. Data flows through Data Collection Endpoint → DCR → Log Analytics Workspace
5. KQL transformation applied before storage

**Configuration Required**:
- Identity Provider URL (OAuth2 token endpoint)
- Identity Provider Token (API credentials)
- App Assure Service Endpoint URL
- Data Collection Endpoint (DCE)
- Data Collection Rule with appropriate schema

**Use Cases**:
- Polling external SaaS APIs for security events
- Scheduled data collection from third-party services
- Integration with systems that expose REST APIs
- Centralized log aggregation from multiple sources

---

### Sample4-CCFPush-New - Push-Based Data Connector

**Purpose**: Demonstrates a **CCF Push Connector** where external systems/agents push logs directly to Microsoft Sentinel using the Logs Ingestion API.

**Key Features**:
- Push connector allowing agents to send data in real-time
- Automated ARM resource deployment (tables, DCR, DCE, Entra app)
- Service Principal authentication with managed identity
- C# .NET sample agent application included
- One-click deployment with automated RBAC assignment
- Secure secret management

**Technical Details**:
- **Connector Type**: Customizable CCF Push Connector
- **Authentication**: Service Principal (Microsoft Entra App)
- **Stream Name**: `Custom-appassurealerts`
- **Target Table**: `appassurealerts_CL`
- **Retry**: 1 attempt
- **Response Processing**: Extracts data from `$.messages` JSON path

**Architecture Components**:
1. **Connector Definition**: Automated deployment configuration with DeployPushConnectorButton
2. **Data Connector**: Push-based configuration with service principal auth
3. **Data Collection Rule (DCR)**: Schema with caid, certid, input fields
4. **Log Analytics Table**: Custom table for alerts
5. **Sample Agent**: C# .NET application demonstrating log push

**Data Schema**:
```json
{
    "TimeGenerated": "datetime",
    "caid": "string",
    "certid": "string",
    "input": {
        // Dynamic JSON object
    }
}
```

**Sample Agent Application** (`Program.cs`):
- **Language**: C# .NET 9.0
- **Libraries**: 
  - `Azure.Identity` - DefaultAzureCredential for authentication
  - `Azure.Monitor.Ingestion` - LogsIngestionClient for data upload
- **Features**:
  - Asynchronous log upload
  - JSON serialization using BinaryData
  - Support for compressed/uncompressed data
  - Comprehensive error handling

**Data Flow**:
1. Deploy connector button creates all Azure resources automatically
2. Entra app is registered with Monitoring Metrics Publisher role
3. External agent/application uses credentials to authenticate
4. Agent pushes logs via Logs Ingestion API to DCE
5. DCR processes and transforms data
6. Logs stored in Log Analytics custom table

**Automated Deployment Provides**:
- Tenant ID (Directory ID)
- Application ID (Client ID)
- Application Secret (Client Secret)
- Data Collection Endpoint URI
- Data Collection Rule Immutable ID
- Stream Name for ingestion

**Configuration Required**:
- Permissions to create Entra app registration
- Azure RBAC Owner or User Access Administrator role (for role assignment)
- Read/Write/Delete permissions on Log Analytics Workspace
- Outbound connectivity from agent to Azure

**Use Cases**:
- On-premises agents pushing security events
- Custom applications sending telemetry
- Real-time event streaming from distributed systems
- IoT devices or edge computing scenarios
- Legacy systems integration via custom agents

**Sample Agent Implementation**:
```csharp
// Initialize
var endpoint = new Uri("https://my-dce.monitor.azure.com");
var ruleId = "dcr-xxxxx";
var streamName = "Custom-appassurealerts";

var credential = new DefaultAzureCredential();
LogsIngestionClient client = new LogsIngestionClient(endpoint, credential);

// Prepare data
BinaryData data = BinaryData.FromObjectAsJson(new[] {
    new {
        Time = DateTime.UtcNow,
        Computer = "Computer1",
        AdditionalContext = new { /* ... */ }
    }
});

// Upload
var response = await client.UploadAsync(ruleId, streamName, RequestContent.Create(data));
```

---

## CCF Connector Comparison: Pull vs Push

| Feature | Sample3 (Pull) | Sample4 (Push) |
|---------|----------------|----------------|
| **Connector Type** | RestApiPoller | Push |
| **Data Flow** | Sentinel polls external API | Agent pushes to Sentinel |
| **Authentication** | JWT from OAuth2 endpoint | Service Principal (Entra App) |
| **Setup Complexity** | Manual credential configuration | Automated ARM deployment |
| **Use Case** | External APIs you can poll | On-premises agents, custom apps |
| **Frequency** | Polling interval (configurable) | Real-time as events occur |
| **Sample Code** | Configuration only | C# .NET agent included |
| **Scalability** | Limited by polling rate | Scales with multiple agents |
| **Latency** | Depends on polling interval | Near real-time |
| **Network** | Outbound from Azure | Outbound from agent |

---

## Common CCF Elements

Both Sample3 and Sample4 utilize:
- **Codeless Connector Framework (CCF)** - Microsoft Sentinel's framework for custom data ingestion
- **Data Collection Rules (DCR)** - Define data transformation and routing
- **Data Collection Endpoints (DCE)** - Ingestion endpoints for secure data transfer
- **Custom Log Analytics Tables** - Store ingested data with `_CL` suffix
- **KQL Transformations** - Process and enrich data before storage
- **Dynamic Schema Support** - Both use `dynamic` type for flexible JSON data
- **ARM Template Deployment** - Infrastructure as Code for reproducible deployments

---

## Security Best Practices

### For All Solutions:
- Store secrets in Azure Key Vault (not in configuration files)
- Use Managed Identities where possible
- Apply principle of least privilege for RBAC roles
- Rotate secrets regularly
- Monitor connector health and connectivity
- Review DCR transformation logic for data sanitization

### For Azure Functions (Sample1, Sample2):
- Enable Application Insights for monitoring
- Use system-assigned managed identity
- Configure network security with VNet integration if needed
- Implement proper error handling and retry logic

### For CCF Connectors (Sample3, Sample4):
- Monitor Data Collection Rule metrics
- Review connector connectivity status in Sentinel
- Validate data ingestion rates against quotas
- Test failover scenarios for high availability
- Implement logging in custom agents (Sample4)

 

## References

### Azure Functions
- [Azure Functions Python Developer Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Azure Monitor Logs Ingestion API](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/logs-ingestion-api-overview)
- [Azure Identity Library for Python](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme)
- [Azure Monitor Ingestion Client Library](https://learn.microsoft.com/en-us/python/api/overview/azure/monitor-ingestion-readme)

### CCF Connectors
- [Codeless Connector Platform (CCP) Overview](https://learn.microsoft.com/en-us/azure/sentinel/create-codeless-connector)
- [Data Collection Rules in Azure Monitor](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/data-collection-rule-overview)
- [Data Collection Endpoints](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/data-collection-endpoint-overview)
- [Custom Logs Ingestion API Tutorial](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/tutorial-logs-ingestion-code)

### Microsoft Sentinel
- [Azure Sentinel Data Connectors](https://github.com/Azure/Azure-Sentinel/tree/master/DataConnectors)
- [Azure Sentinel Solutions](https://learn.microsoft.com/en-us/azure/sentinel/sentinel-solutions)
- [Create Custom Connectors](https://learn.microsoft.com/en-us/azure/sentinel/create-custom-connector)

### Agent Development
- [Azure Monitor Ingestion .NET Client](https://learn.microsoft.com/en-us/dotnet/api/overview/azure/monitor.ingestion-readme)
- [DefaultAzureCredential Class](https://learn.microsoft.com/en-us/dotnet/api/azure.identity.defaultazurecredential)
