"""
Configuration file for ML-Based Intrusion Detection System
"""
import os
from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).parent.absolute()

# Directory Paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"

MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
LOGS_DIR = PROJECT_ROOT / "logs"
CONFIGS_DIR = PROJECT_ROOT / "configs"

# Ensure directories exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, SAMPLE_DATA_DIR, 
                  MODELS_DIR, REPORTS_DIR, LOGS_DIR, CONFIGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Data Configuration
RANDOM_STATE = 42
TEST_SIZE = 0.3
VALIDATION_SIZE = 0.15

# File Upload Limits
MAX_FILE_SIZE_MB = 100
ALLOWED_EXTENSIONS = ['.csv']

# Model Configuration
MODELS = {
    'logistic_regression': {
        'name': 'Logistic Regression',
        'enabled': True,
        'max_iter': 1000,
        'random_state': RANDOM_STATE
    },
    'decision_tree': {
        'name': 'Decision Tree',
        'enabled': True,
        'max_depth': 20,
        'random_state': RANDOM_STATE
    },
    'random_forest': {
        'name': 'Random Forest',
        'enabled': True,
        'n_estimators': 100,
        'max_depth': 20,
        'random_state': RANDOM_STATE
    },
    'xgboost': {
        'name': 'XGBoost',
        'enabled': False,  # Optional enhancement
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': RANDOM_STATE
    }
}

# Class Imbalance Strategy
IMBALANCE_STRATEGY = 'smote'  # Options: 'smote', 'undersample', 'class_weights', 'combined'
SMOTE_SAMPLING_STRATEGY = 'auto'

# Feature Engineering
SCALE_FEATURES = True
SCALER_TYPE = 'standard'  # Options: 'standard', 'minmax', 'robust'

# Evaluation Metrics
METRICS = [
    'accuracy',
    'precision',
    'recall',
    'f1_score',
    'roc_auc',
    'confusion_matrix',
    'classification_report'
]

# Dashboard Configuration
DASHBOARD_TITLE = "ML-Based Intrusion Detection System"
DASHBOARD_ICON = "🛡️"
THEME = "dark"

# Colors for Visualization
COLORS = {
    'benign': '#00ff41',      # Matrix green
    'malicious': '#ff0000',    # Red
    'primary': '#00d4ff',      # Cyan
    'secondary': '#8b5cf6',    # Purple
    'background': '#0a0e27',   # Dark blue
    'text': '#e2e8f0'          # Light gray
}

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"

# Dataset Configuration (CIC-IDS2017)
DATASET_INFO = {
    'name': 'CIC-IDS2017',
    'url': 'https://www.unb.ca/cic/datasets/ids-2017.html',
    'description': 'Canadian Institute for Cybersecurity Intrusion Detection System Dataset 2017',
    'target_column': 'Label',
    'features': []  # Will be populated after data loading
}

# Attack Categories for CIC-IDS2017
ATTACK_CATEGORIES = [
    'BENIGN',
    'DoS Hulk',
    'PortScan',
    'DDoS',
    'DoS GoldenEye',
    'FTP-Patator',
    'SSH-Patator',
    'DoS slowloris',
    'DoS Slowhttptest',
    'Bot',
    'Web Attack – Brute Force',
    'Web Attack – XSS',
    'Infiltration',
    'Web Attack – Sql Injection',
    'Heartbleed'
]

# Binary Classification Mapping
BINARY_MAPPING = {
    'BENIGN': 0,
    'default': 1  # All attack types map to 1
}

# Network Monitoring Configuration (Optional)
NETWORK_MONITORING = {
    'enabled': False,  # Disabled by default for safety
    'interface': 'auto',  # Will be selected by user
    'packet_count': 100,
    'timeout': 30
}

# Security Configuration
SECURITY = {
    'max_csv_rows': 1000000,  # Maximum rows to process
    'validate_input': True,
    'sanitize_output': True
}

# Model Persistence
MODEL_FILENAME = 'ids_model.joblib'
METADATA_FILENAME = 'model_metadata.json'
FEATURE_NAMES_FILENAME = 'feature_names.json'
SCALER_FILENAME = 'scaler.joblib'
ENCODER_FILENAME = 'label_encoder.joblib'
