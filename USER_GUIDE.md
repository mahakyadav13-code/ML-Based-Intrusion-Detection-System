# 📖 User Guide - ML-Based Intrusion Detection System

Complete guide for using the IDS Flask Dashboard and API.

---

## 📋 Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Using the Detection System](#using-the-detection-system)
4. [Understanding Results](#understanding-results)
5. [API Usage](#api-usage)
6. [Troubleshooting](#troubleshooting)
7. [Best Practices](#best-practices)

---

## 🚀 Getting Started

### Accessing the Dashboard

1. **Open your web browser**
2. **Navigate to**: http://localhost:5000
3. **Wait for the page to load** (usually 2-3 seconds)

### First Time Setup

If this is your first time using the system:

1. **Verify Models are Trained**
   - Look for "3 Trained Models" on the Overview page
   - If models are missing, run: `python src\train_model.py`

2. **Check System Status**
   - Green "Operational" badge in top right = System ready
   - Red/Yellow badge = Check logs or retrain models

---

## 🎯 Dashboard Overview

### Navigation Bar

Located at the top of the page:

- **🏠 Overview** - System dashboard and statistics
- **🖥️ Models** - Model performance and details
- **🔍 Detection** - Upload files for intrusion detection
- **📊 Analytics** - Charts and visualizations
- **🟢 Status Badge** - Real-time system health

### Overview Page

#### Key Metrics Cards

**Trained Models**
- Shows total number of ML models ready for use
- Typical value: 3 (Logistic Regression, Decision Tree, Random Forest)

**Average Accuracy**
- Combined accuracy across all models
- Higher is better (90%+ is excellent)

**Features**
- Number of network traffic features analyzed
- Standard: 63 features from CIC-IDS2017 dataset

**Training Samples**
- Number of records used to train models
- More samples = better model performance

#### System Health Panel

Shows real-time status:
- **Detector Status**: Model loading state
- **Last Updated**: Timestamp of last status check
- **API Status**: Backend availability

---

## 🔍 Using the Detection System

### Step-by-Step: Analyze Network Traffic

#### 1. Navigate to Detection Page

Click **"Detection"** in the navigation bar.

#### 2. Prepare Your Data

**File Format Requirements:**
- **Type**: CSV (Comma-Separated Values)
- **Size**: Maximum 100MB
- **Features**: Must include all 63 required features
- **Encoding**: UTF-8

**Sample Data Location:**
```
data/sample/test_upload_SYNTHETIC.csv
```

**Required Features** (excerpt):
- Flow_Duration
- Total_Fwd_Packets
- Total_Backward_Packets
- Flow_Bytes/s
- Flow_Packets/s
- Protocol
- ...and 57 more

#### 3. Upload File

1. **Click "Select CSV File"** button
2. **Choose your CSV file** from file browser
3. **Click "Analyze Traffic"** button
4. **Wait for processing** (progress bar will show)

#### 4. View Results

Results appear below the upload form:

**Summary Statistics:**
- **Total Records**: Number of traffic flows analyzed
- **Benign Traffic**: Normal, safe connections
- **Attacks Detected**: Malicious traffic identified
- **High Risk**: Attacks with >80% confidence

**Detailed Predictions Table:**
- **#**: Record number
- **Prediction**: BENIGN or ATTACK
- **Confidence**: Model's certainty (0-100%)
- **Risk Level**: HIGH/MEDIUM/LOW
- **Status**: Processing confirmation

---

## 📊 Understanding Results

### Prediction Labels

**🟢 BENIGN**
- Normal network traffic
- No threat detected
- Safe to allow

**🔴 ATTACK**
- Malicious traffic detected
- Potential security threat
- Requires investigation

### Confidence Scores

**90-100% (Excellent)**
- Very high certainty
- Highly reliable prediction
- Trust this result

**70-89% (Good)**
- Good confidence
- Generally reliable
- Minor uncertainty

**50-69% (Moderate)**
- Moderate confidence
- May need human review
- Some uncertainty

**Below 50% (Low)**
- Low confidence
- Definitely needs review
- Model unsure

### Risk Levels

**🔴 HIGH RISK**
- Attack detected with >80% confidence
- Immediate action recommended
- Block traffic or investigate urgently

**🟡 MEDIUM RISK**
- Attack detected with 60-80% confidence
- Monitor closely
- Consider additional analysis

**🟢 LOW RISK**
- Benign traffic or low-confidence attack
- Normal monitoring sufficient
- Likely safe

---

## 🔧 Model Performance

### Available Models

#### 1. Logistic Regression
**Type**: Linear classification  
**Strengths**: Fast, interpretable  
**Best For**: Binary classification, quick predictions  
**Accuracy**: ~95-99%

#### 2. Decision Tree
**Type**: Tree-based classification  
**Strengths**: Easy to understand, visual  
**Best For**: Finding decision rules  
**Accuracy**: ~98-100%

#### 3. Random Forest
**Type**: Ensemble of decision trees  
**Strengths**: High accuracy, robust  
**Best For**: Production use, complex patterns  
**Accuracy**: ~99-100%

### How Models Are Selected

The system automatically uses the **best performing model** based on:
1. F1-Score (primary metric)
2. Accuracy
3. Training time

Currently: **Decision Tree** is selected (F1=1.0000)

---

## 🌐 API Usage

### Authentication

Currently, the API is **open** (no authentication required).

**Production Recommendation**: Add API keys or JWT tokens.

### Base URL

```
http://localhost:5000/api
```

### Endpoints

#### Get System Status

```bash
GET /api/status
```

**Response:**
```json
{
  "status": "operational",
  "models": [
    {
      "name": "Decision Tree",
      "accuracy": 1.0,
      "training_time": 0.18
    }
  ],
  "detector_loaded": true,
  "dataset_info": {
    "features": 63,
    "training_samples": 4900
  }
}
```

#### Get Model Information

```bash
GET /api/models
```

**Response:**
```json
{
  "models": [
    {
      "name": "Decision Tree",
      "test_accuracy": "1.0000",
      "precision": "1.0000",
      "f1_score": "1.0000"
    }
  ]
}
```

#### Predict (Batch)

```bash
POST /api/predict
Content-Type: multipart/form-data

file: <CSV file>
```

**Response:**
```json
{
  "total_records": 700,
  "benign_count": 500,
  "attack_count": 200,
  "predictions": [
    {
      "record_id": 1,
      "prediction": "BENIGN",
      "confidence": 0.95
    }
  ]
}
```

#### Single Prediction

```bash
POST /api/predict/single
Content-Type: application/json

{
  "Flow_Duration": 120000,
  "Total_Fwd_Packets": 10,
  ...
}
```

**Response:**
```json
{
  "prediction": "BENIGN",
  "confidence": 0.98,
  "timestamp": "2026-11-21T01:30:00"
}
```

### Example: Python API Client

```python
import requests

# Get system status
response = requests.get('http://localhost:5000/api/status')
status = response.json()
print(f"System: {status['status']}")

# Upload file for prediction
files = {'file': open('traffic.csv', 'rb')}
response = requests.post('http://localhost:5000/api/predict', files=files)
results = response.json()
print(f"Attacks detected: {results['attack_count']}")
```

### Example: JavaScript/Fetch

```javascript
// Get system status
fetch('http://localhost:5000/api/status')
  .then(response => response.json())
  .then(data => console.log('Status:', data.status));

// Upload file
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/api/predict', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => console.log('Results:', data));
```

---

## 🔧 Troubleshooting

### Common Issues

#### "Model not loaded" Error

**Cause**: Models haven't been trained  
**Solution**:
```powershell
python src\train_model.py
```

#### File Upload Fails

**Possible Causes**:
- File too large (>100MB)
- Wrong format (not CSV)
- Missing required features
- Corrupted file

**Solution**:
1. Check file size
2. Verify CSV format
3. Use sample data to test
4. Check browser console for errors

#### Slow Performance

**Causes**:
- Large file (>50,000 records)
- Insufficient RAM
- CPU bottleneck

**Solutions**:
- Split large files into smaller batches
- Close other applications
- Use more powerful hardware
- Consider cloud deployment

#### Charts Not Displaying

**Cause**: Missing evaluation reports  
**Solution**:
```powershell
python src\evaluate_model.py
```

---

## ✅ Best Practices

### Data Preparation

1. **Clean Your Data**
   - Remove duplicates
   - Handle missing values
   - Normalize features

2. **Use Correct Format**
   - CSV with proper headers
   - UTF-8 encoding
   - Consistent feature names

3. **Test with Samples First**
   - Use provided sample data
   - Verify format is correct
   - Check for errors

### Security

1. **Don't Upload Sensitive Data**
   - Remove PII (Personally Identifiable Information)
   - Anonymize IP addresses if needed
   - Follow data protection regulations

2. **Use HTTPS in Production**
   - Never send data over plain HTTP
   - Configure SSL/TLS certificates
   - Use secure authentication

3. **Regular Updates**
   - Keep models retrained with new data
   - Update dependencies
   - Monitor for security patches

### Performance

1. **Batch Processing**
   - Group small files together
   - Split very large files
   - Process during off-peak hours

2. **Monitor Resources**
   - Check CPU/RAM usage
   - Monitor disk space
   - Review logs regularly

3. **Cache Results**
   - Save predictions for analysis
   - Export reports regularly
   - Keep audit trails

---

## 📞 Getting Help

### Resources

- **README.md** - Project overview
- **DEPLOYMENT.md** - Deployment instructions
- **API_DOCUMENTATION.md** - Full API reference
- **GitHub Issues** - Report bugs

### Log Files

Check logs for detailed error information:
```
logs/app.log
```

### Support Channels

1. Check documentation first
2. Review log files
3. Test with sample data
4. Contact development team

---

## 📚 Additional Information

### Dataset Information

**CIC-IDS2017**
- Source: Canadian Institute for Cybersecurity
- Size: 2.8 million flows
- Attack Types: 15 categories
- Download: https://www.unb.ca/cic/datasets/ids-2017.html

### Attack Types Detected

The system can identify:
- **DoS/DDoS** - Denial of Service attacks
- **Port Scanning** - Network reconnaissance
- **Brute Force** - Password attacks
- **Web Attacks** - SQL injection, XSS
- **Infiltration** - System penetration
- **Botnet** - Malware networks

### Model Retraining

Retrain models regularly with new data:

```powershell
# Full pipeline
python src\data_preprocessing.py
python src\train_model.py
python src\evaluate_model.py
```

Recommended frequency:
- **Development**: Weekly
- **Production**: Monthly or when accuracy drops

---

## 🎓 Learning Resources

- **Machine Learning**: scikit-learn.org
- **Network Security**: SANS Institute
- **Flask Framework**: flask.palletsprojects.com
- **Docker**: docs.docker.com

---

**Version**: 1.0.0  
**Last Updated**: November 21, 2026  
**Maintained By**: CodeC Technologies Internship Team
