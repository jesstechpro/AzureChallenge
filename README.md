# Azure Cloud Resume Challenge

A modern, serverless resume website built on Azure, featuring a real-time visitor counter powered by Azure Functions and Cosmos DB.

## 🌐 Live Demo

**[View Live Site →](https://azurefrontend.z13.web.core.windows.net/)**

## 🏗️ Architecture

This project demonstrates a complete serverless web application using Azure cloud services:

```
[Frontend] → [Azure Storage Static Website] → [Azure Functions API] → [Cosmos DB]
    ↓              ↓                           ↓                      ↓
HTML/CSS/JS    Static Hosting              Serverless Backend     NoSQL Database
```

### Components

- **Frontend**: Static website (HTML, CSS, JavaScript) hosted on Azure Storage
- **Backend**: Python Azure Functions for API endpoints
- **Database**: Azure Cosmos DB for visitor counter persistence
- **CI/CD**: GitHub Actions for automated deployment
- **Monitoring**: Built-in Azure Functions logging and telemetry

## 🚀 Features

- **Responsive Design**: Modern, mobile-first resume layout
- **Real-time Visitor Counter**: Tracks site visits using serverless architecture
- **CORS-Enabled API**: Secure cross-origin requests between frontend and backend
- **Automated Deployment**: GitHub Actions workflow for continuous deployment
- **Cost-Effective**: Serverless architecture with pay-per-use pricing

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Semantic markup and accessibility
- **CSS3** - Modern styling with flexbox/grid layouts
- **Vanilla JavaScript** - Fetch API for backend communication

### Backend
- **Python 3.11** - Azure Functions runtime
- **Azure Functions** - Serverless compute platform
- **Azure Cosmos DB** - NoSQL database with SQL API
- **CORS** - Cross-origin resource sharing configuration

### Infrastructure
- **Azure Storage** - Static website hosting
- **Azure Functions App** - Serverless backend hosting
- **Azure Cosmos DB** - Managed NoSQL database
- **GitHub Actions** - CI/CD pipeline

## 📁 Project Structure

```
AzureChallenge/
├── frontend/                 # Static website files
│   ├── index.html           # Main resume page
│   ├── style.css            # Styling and responsive design
│   ├── script.js            # Visitor counter JavaScript
│   └── robots.txt           # Search engine directives
├── backend/                 # Azure Functions backend
│   ├── function_app.py      # Main Functions application
│   ├── requirements.txt     # Python dependencies
│   ├── host.json           # Functions host configuration
│   └── local.settings.json  # Local development settings
├── .github/workflows/       # CI/CD configuration
│   └── deploy-function-app.yml
├── AZURE_STORAGE_MIGRATION_PLAN.md
├── VISITOR_COUNTER_PLAN.md
└── README.md
```

## 🔧 API Endpoints

### Visitor Counter API

**Base URL**: `https://getwebcounter.azurewebsites.net/api`

#### Get Current Count
```http
GET /counter
```
**Response**:
```json
{
  "count": 1234
}
```

#### Increment Counter
```http
POST /counter
```
**Response**:
```json
{
  "count": 1235
}
```

## 🚀 Deployment

### Prerequisites
- Azure subscription
- GitHub account
- Azure CLI (for local development)

### Backend Deployment
The backend is automatically deployed via GitHub Actions when changes are pushed to the `backend/` directory:

1. **GitHub Secrets Required**:
   - `AZURE_FUNCTIONAPP_NAME`
   - `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`

2. **Deployment Trigger**: Push to `main` branch with changes in `backend/` path

### Frontend Deployment
The frontend is hosted on Azure Storage Static Website:

1. **Storage Account**: `stresumejesswood`
2. **Container**: `$web`
3. **Endpoint**: `https://azurefrontend.z13.web.core.windows.net/`

## 🔒 Security Features

- **CORS Configuration**: Properly configured cross-origin requests
- **Anonymous Access**: Public API endpoints for visitor counter
- **Environment Variables**: Secure configuration management
- **Connection String Security**: Database credentials stored in Azure App Settings

## 📊 Database Schema

### Cosmos DB Container: `Counters`
```json
{
  "id": "1",
  "count": 1234,
  "_partitionKey": "1"
}
```

- **Database**: `VisitorCounterDb`
- **Container**: `Counters`
- **Partition Key**: `/_partitionKey`

## 🔄 Development Workflow

### Local Development
1. **Backend**:
   ```bash
   cd backend
   func start
   ```
   
2. **Frontend**:
   - Serve `frontend/` directory with any static server
   - Update `script.js` to use `localApiUrl` for development

### Production Deployment
- **Backend**: Automatic via GitHub Actions
- **Frontend**: Manual upload to Azure Storage `$web` container

## 📈 Monitoring & Logging

- **Azure Functions Logs**: Built-in logging and telemetry
- **Application Insights**: Optional monitoring (commented in requirements.txt)
- **Cosmos DB Metrics**: Database performance monitoring through Azure Portal

## 💰 Cost Optimization

This serverless architecture is designed for cost efficiency:

- **Azure Functions**: Pay-per-execution model
- **Cosmos DB**: Provisioned throughput with autoscale
- **Azure Storage**: Low-cost static website hosting
- **Estimated Monthly Cost**: $2-5 for low-traffic scenarios

## 🎯 Cloud Resume Challenge

This project was built as part of the [Cloud Resume Challenge](https://cloudresumechallenge.dev/), demonstrating:

- ✅ Static website hosting
- ✅ HTTPS and custom DNS (planned)
- ✅ Serverless API backend
- ✅ Database integration
- ✅ Infrastructure as Code concepts
- ✅ CI/CD pipeline
- ✅ Monitoring and logging

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 About

**Jess Wood** - Sales Engineer specializing in endpoint security, IAM, and compliance solutions.

- 📧 [10jwood@gmail.com](mailto:10jwood@gmail.com)
- 📱 [(910) 442-6537](tel:+19104426537)
- 💼 [LinkedIn](https://www.linkedin.com/in/jess-wood-consults)

---

*Built with ❤️ using Azure serverless technologies*
