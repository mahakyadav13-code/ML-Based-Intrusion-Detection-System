# 🔌 API Documentation - ML-Based Intrusion Detection System

Complete REST API reference for developers.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
4. [Request/Response Formats](#requestresponse-formats)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Code Examples](#code-examples)

---

## 🌐 Overview

### Base URL

```
http://localhost:5000/api
```

**Production**: Replace with your deployed URL

### Protocol

- **HTTP Methods**: GET, POST
- **Data Format**: JSON, multipart/form-data
- **Response Format**: JSON
- **Encoding**: UTF-8

### API Version

**Current Version**: 1.0.0  
**Release Date**: November 21, 2026

---

## 🔐 Authentication

### Current Implementation

**Type**: None (Open API)  
**Status**: Development mode

### Production Recommendations

#### API Key Authentication

```python
headers = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}
```

#### JWT Token Authentication

```python
headers = {
    'Authorization': 'JWT your.token.here'
}
```

---

## 📡 Endpoints

### 1. System Status

Get current system status and health information.

**Endpoint**: `GET /api/status`

**Parameters**: None

**Response**:
```json
{
  "status": "operational",
  "models": [
    {
      "name": "Decision Tree",
      "accuracy": 1.0,
      "training_time": 0.18,
      "trained_date": "2026-11-21T00:52:49"
    },
    {
      "name": "Logistic Regression",
      "accuracy": 1.0,
      "training_time": 0.18,
      "trained_date": "2026-11-21T00:52:41"
    },
    {
      "name": "Random Forest",
      "accuracy": 1.0,
      "training_time": 0.44,
      "trained_date": "2026-11-21T00:52:47"
    }
  ],
  "detector_loaded": true,
  "dataset_info": {
    "features": 63,
    "training_samples": 4900,
    "test_samples": 2100
  },
  "timestamp": "2026-11-21T01:30:15.123456"
}
```

**Status Codes**:
- `200` - Success
- `500` - Internal server error

**Example**:
```bash
curl http://localhost:5000/api/status
```

---

### 2. Model Information

Get detailed information about all trained models.

**Endpoint**: `GET /api/models`

**Parameters**: None

**Response**:
```json
{
  "models": [
    {
      "name": "Decision Tree",
      "key": "decision_tree",
      "file_size": "15.23 KB",
      "training_time": "0.18s",
      "cv_accuracy": "0.9998",
      "test_accuracy": "1.0000",
      "precision": "1.0000",
      "recall": "1.0000",
      "f1_score": "1.0000",
      "roc_auc": "1.0000",
      "trained_at": "2026-11-21 00:52:44"
    }
  ],
  "total_models": 3
}
```

**Status Codes**:
- `200` - Success
- `500` - Internal server error

**Example**:
```bash
curl http://localhost:5000/api/models
```

---

### 3. Batch Prediction

Upload CSV file for batch intrusion detection.

**Endpoint**: `POST /api/predict`

**Content-Type**: `multipart/form-data`

**Parameters**:
- `file` (required) - CSV file containing network traffic data

**File Requirements**:
- **Format**: CSV
- **Max Size**: 100MB
- **Encoding**: UTF-8
- **Features**: All 63 required features must be present

**Response**:
```json
{
  "total_records": 700,
  "benign_count": 500,
  "attack_count": 200,
  "predictions": [
    {
      "record_id": 1,
      "prediction": "BENIGN",
      "prediction_class": 0,
      "confidence": 0.9876,
      "timestamp": "2026-11-21T01:30:15.123456"
    },
    {
      "record_id": 2,
      "prediction": "ATTACK",
      "prediction_class": 1,
      "confidence": 0.9543,
      "timestamp": "2026-11-21T01:30:15.234567"
    }
  ],
  "summary": {
    "avg_confidence": 0.9712,
    "high_risk_count": 150
  }
}
```

**Note**: Only first 100 predictions are returned. Full results are processed.

**Status Codes**:
- `200` - Success
- `400` - Bad request (no file, invalid format)
- `413` - File too large
- `500` - Internal server error

**Example**:
```bash
curl -X POST \
  -F "file=@traffic.csv" \
  http://localhost:5000/api/predict
```

**Python Example**:
```python
import requests

files = {'file': open('traffic.csv', 'rb')}
response = requests.post(
    'http://localhost:5000/api/predict',
    files=files
)
results = response.json()
print(f"Total: {results['total_records']}")
print(f"Attacks: {results['attack_count']}")
```

---

### 4. Single Prediction

Make prediction on a single network traffic record.

**Endpoint**: `POST /api/predict/single`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "Flow_Duration": 120000,
  "Total_Fwd_Packets": 10,
  "Total_Backward_Packets": 8,
  "Total_Length_of_Fwd_Packets": 5000,
  "Total_Length_of_Bwd_Packets": 3200,
  "Fwd_Packet_Length_Max": 1500,
  "Fwd_Packet_Length_Min": 60,
  "Fwd_Packet_Length_Mean": 500.0,
  "Fwd_Packet_Length_Std": 150.5,
  ...
}
```

**Response**:
```json
{
  "record_id": 1,
  "prediction": "BENIGN",
  "prediction_class": 0,
  "confidence": 0.9876,
  "timestamp": "2026-11-21T01:30:15.123456"
}
```

**Status Codes**:
- `200` - Success
- `400` - Bad request (missing features)
- `500` - Internal server error

**Example**:
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"Flow_Duration": 120000, ...}' \
  http://localhost:5000/api/predict/single
```

---

### 5. Statistics

Get system-wide statistics.

**Endpoint**: `GET /api/statistics`

**Parameters**: None

**Response**:
```json
{
  "models": {
    "total_trained": 3,
    "available_algorithms": [
      "Logistic Regression",
      "Decision Tree",
      "Random Forest",
      "XGBoost"
    ]
  },
  "data": {
    "processed_files": 2,
    "sample_files": 2
  },
  "reports": {
    "evaluation_reports": 1,
    "visualizations": 9
  }
}
```

**Status Codes**:
- `200` - Success
- `500` - Internal server error

---

### 6. Get Report

Retrieve specific evaluation report.

**Endpoint**: `GET /api/reports/{report_name}`

**Parameters**:
- `report_name` - Name of the report (without extension)

**Available Reports**:
- `evaluation_report`
- `model_comparison`

**Response**: JSON object with report data

**Status Codes**:
- `200` - Success
- `404` - Report not found
- `500` - Internal server error

**Example**:
```bash
curl http://localhost:5000/api/reports/evaluation_report
```

---

### 7. Get Chart

Retrieve chart image (confusion matrix, ROC curve, etc.).

**Endpoint**: `GET /api/charts/{chart_name}`

**Parameters**:
- `chart_name` - Name of the chart (without extension)

**Available Charts**:
- `{model}_confusion_matrix`
- `{model}_roc_curve`
- `{model}_pr_curve`

**Models**: `logistic_regression`, `decision_tree`, `random_forest`

**Response**: PNG image

**Status Codes**:
- `200` - Success
- `404` - Chart not found
- `500` - Internal server error

**Example**:
```bash
curl http://localhost:5000/api/charts/decision_tree_model_confusion_matrix \
  --output confusion_matrix.png
```

---

## 📝 Request/Response Formats

### Standard Response Format

All API responses follow this structure:

**Success Response**:
```json
{
  "data": { ... },
  "metadata": {
    "timestamp": "2026-11-21T01:30:15",
    "version": "1.0.0"
  }
}
```

**Error Response**:
```json
{
  "error": "Error message description",
  "code": "ERROR_CODE",
  "timestamp": "2026-11-21T01:30:15"
}
```

### Data Types

| Type | Description | Example |
|------|-------------|---------|
| `string` | Text data | `"BENIGN"` |
| `integer` | Whole number | `42` |
| `float` | Decimal number | `0.9876` |
| `boolean` | True/False | `true` |
| `array` | List of items | `[1, 2, 3]` |
| `object` | Key-value pairs | `{"key": "value"}` |
| `datetime` | ISO 8601 timestamp | `"2026-11-21T01:30:15"` |

---

## ⚠️ Error Handling

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| `200` | OK | Request successful |
| `201` | Created | Resource created |
| `400` | Bad Request | Invalid request format |
| `404` | Not Found | Resource not found |
| `413` | Payload Too Large | File exceeds 100MB |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Server error |
| `503` | Service Unavailable | Service temporarily down |

### Error Response Examples

**400 Bad Request**:
```json
{
  "error": "No file provided",
  "code": "MISSING_FILE",
  "timestamp": "2026-11-21T01:30:15"
}
```

**404 Not Found**:
```json
{
  "error": "Report not found",
  "code": "RESOURCE_NOT_FOUND",
  "timestamp": "2026-11-21T01:30:15"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Model not loaded",
  "code": "MODEL_ERROR",
  "timestamp": "2026-11-21T01:30:15"
}
```

### Error Handling Best Practices

```python
import requests

try:
    response = requests.post(url, files=files)
    response.raise_for_status()  # Raise exception for bad status
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.exceptions.ConnectionError:
    print("Connection failed")
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

---

## 🚦 Rate Limiting

### Current Limits

**Default**: No rate limiting (development mode)

### Recommended Production Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/api/status` | 60 req | 1 minute |
| `/api/models` | 30 req | 1 minute |
| `/api/predict` | 10 req | 1 minute |
| `/api/predict/single` | 100 req | 1 minute |

### Rate Limit Headers

When implemented:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1700567815
```

---

## 💻 Code Examples

### Python Client Library

```python
import requests
from pathlib import Path

class IDSClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_status(self):
        """Get system status"""
        response = self.session.get(f'{self.base_url}/api/status')
        response.raise_for_status()
        return response.json()
    
    def predict_file(self, filepath):
        """Predict on CSV file"""
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = self.session.post(
                f'{self.base_url}/api/predict',
                files=files
            )
        response.raise_for_status()
        return response.json()
    
    def predict_single(self, features):
        """Predict single record"""
        response = self.session.post(
            f'{self.base_url}/api/predict/single',
            json=features
        )
        response.raise_for_status()
        return response.json()

# Usage
client = IDSClient()
status = client.get_status()
print(f"System: {status['status']}")

results = client.predict_file('traffic.csv')
print(f"Attacks: {results['attack_count']}")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

class IDSClient {
    constructor(baseURL = 'http://localhost:5000') {
        this.baseURL = baseURL;
        this.client = axios.create({ baseURL });
    }

    async getStatus() {
        const response = await this.client.get('/api/status');
        return response.data;
    }

    async predictFile(filepath) {
        const form = new FormData();
        form.append('file', fs.createReadStream(filepath));
        
        const response = await this.client.post('/api/predict', form, {
            headers: form.getHeaders()
        });
        return response.data;
    }

    async predictSingle(features) {
        const response = await this.client.post('/api/predict/single', features);
        return response.data;
    }
}

// Usage
(async () => {
    const client = new IDSClient();
    const status = await client.getStatus();
    console.log('System:', status.status);
    
    const results = await client.predictFile('traffic.csv');
    console.log('Attacks:', results.attack_count);
})();
```

### cURL Examples

**Get Status**:
```bash
curl -X GET http://localhost:5000/api/status
```

**Upload File**:
```bash
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "file=@traffic.csv" \
  http://localhost:5000/api/predict
```

**Single Prediction**:
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d @sample_record.json \
  http://localhost:5000/api/predict/single
```

**Save Chart**:
```bash
curl http://localhost:5000/api/charts/decision_tree_model_confusion_matrix \
  -o confusion_matrix.png
```

---

## 📚 Additional Resources

- **OpenAPI Specification**: Coming soon
- **Postman Collection**: Available in `/docs/postman/`
- **SDK Libraries**: Python, JavaScript
- **API Changelog**: Track updates

---

## 🔄 Versioning

API follows **Semantic Versioning** (SemVer):

```
MAJOR.MINOR.PATCH
  1  .  0  .  0
```

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

---

**Version**: 1.0.0  
**Last Updated**: November 21, 2026  
**Maintained By**: CodeC Technologies
