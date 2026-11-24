"""
Professional Flask Application for ML-Based Intrusion Detection System
Modern REST API with comprehensive security and error handling
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
from loguru import logger

import config
from src.predict import IntrusionDetector
from src.utils import setup_logging, load_metadata

# Initialize Flask app
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = config.DATA_DIR / 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Enable CORS
CORS(app)

# Setup logging
setup_logging()

# Create upload folder
app.config['UPLOAD_FOLDER'].mkdir(parents=True, exist_ok=True)

# Global detector instance
detector = None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.before_request
def initialize_detector():
    """Initialize detector on first request"""
    global detector
    if detector is None:
        try:
            detector = IntrusionDetector()
            detector.load_best_model()
            logger.info("Intrusion detector initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize detector: {e}")


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/status')
def api_status():
    """Get system status"""
    try:
        # Load model metadata
        models_dir = config.MODELS_DIR
        trained_models = []
        
        for model_file in models_dir.glob('*_model.joblib'):
            model_name = model_file.stem.replace('_model', '').replace('_', ' ').title()
            metadata_file = models_dir / f"{model_file.stem.replace('_model', '')}_metadata.json"
            
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                trained_models.append({
                    'name': model_name,
                    'accuracy': metadata.get('cv_accuracy_mean', 0),
                    'training_time': metadata.get('training_time', 0),
                    'trained_date': metadata.get('trained_at', 'N/A')
                })
        
        # Get dataset info
        preprocessing_metadata = load_metadata(models_dir / 'preprocessing_metadata.json')
        
        return jsonify({
            'status': 'operational',
            'models': trained_models,
            'detector_loaded': detector is not None and detector.model is not None,
            'dataset_info': {
                'features': preprocessing_metadata.get('num_features', 0),
                'training_samples': preprocessing_metadata.get('training_samples', 0),
                'test_samples': preprocessing_metadata.get('test_samples', 0)
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/models')
def api_models():
    """Get detailed model information"""
    try:
        models_dir = config.MODELS_DIR
        models_info = []
        
        # Load evaluation report
        eval_report_path = config.REPORTS_DIR / 'evaluation_report.json'
        eval_data = {}
        if eval_report_path.exists():
            with open(eval_report_path, 'r') as f:
                eval_data = json.load(f)
        
        for model_file in models_dir.glob('*_model.joblib'):
            model_key = model_file.stem.replace('_model', '')
            model_name = model_key.replace('_', ' ').title()
            
            metadata_file = models_dir / f"{model_key}_metadata.json"
            
            model_info = {
                'name': model_name,
                'key': model_key,
                'file_size': f"{model_file.stat().st_size / 1024:.2f} KB"
            }
            
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                model_info.update({
                    'training_time': f"{metadata.get('training_time', 0):.2f}s",
                    'cv_accuracy': f"{metadata.get('cv_accuracy_mean', 0):.4f}",
                    'trained_at': metadata.get('trained_at', 'N/A')
                })
            
            # Add evaluation metrics if available
            if model_key in eval_data.get('models', {}):
                eval_metrics = eval_data['models'][model_key]
                model_info.update({
                    'test_accuracy': f"{eval_metrics.get('accuracy', 0):.4f}",
                    'precision': f"{eval_metrics.get('precision', 0):.4f}",
                    'recall': f"{eval_metrics.get('recall', 0):.4f}",
                    'f1_score': f"{eval_metrics.get('f1_score', 0):.4f}",
                    'roc_auc': f"{eval_metrics.get('roc_auc', 0):.4f}"
                })
            
            models_info.append(model_info)
        
        return jsonify({
            'models': models_info,
            'total_models': len(models_info)
        })
    except Exception as e:
        logger.error(f"Error getting models info: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """Predict on uploaded CSV file"""
    try:
        if detector is None or detector.model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only CSV files are allowed'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = app.config['UPLOAD_FOLDER'] / filename
        file.save(filepath)
        
        try:
            # Read CSV
            df = pd.read_csv(filepath)
            logger.info(f"Loaded CSV: {len(df)} records, {len(df.columns)} columns")
            
            # Make predictions
            predictions = detector.predict_batch(df)
            
            # Prepare response
            results = {
                'total_records': len(predictions),
                'benign_count': int(sum(1 for p in predictions if p['prediction'] == 'BENIGN')),
                'attack_count': int(sum(1 for p in predictions if p['prediction'] == 'ATTACK')),
                'predictions': predictions[:100],  # Return first 100 for display
                'summary': {
                    'avg_confidence': float(np.mean([p['confidence'] for p in predictions])),
                    'high_risk_count': int(sum(1 for p in predictions if p['confidence'] > 0.8 and p['prediction'] == 'ATTACK'))
                }
            }
            
            return jsonify(results)
            
        finally:
            # Clean up uploaded file
            if filepath.exists():
                filepath.unlink()
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict/single', methods=['POST'])
def api_predict_single():
    """Predict on single record"""
    try:
        if detector is None or detector.model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Convert to DataFrame
        df = pd.DataFrame([data])
        
        # Make prediction
        predictions = detector.predict_batch(df)
        
        if predictions:
            return jsonify(predictions[0])
        else:
            return jsonify({'error': 'Prediction failed'}), 500
            
    except Exception as e:
        logger.error(f"Single prediction error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics')
def api_statistics():
    """Get system statistics"""
    try:
        stats = {
            'models': {
                'total_trained': len(list(config.MODELS_DIR.glob('*_model.joblib'))),
                'available_algorithms': ['Logistic Regression', 'Decision Tree', 'Random Forest', 'XGBoost']
            },
            'data': {
                'processed_files': len(list(config.PROCESSED_DATA_DIR.glob('*.csv'))),
                'sample_files': len(list(config.SAMPLE_DATA_DIR.glob('*.csv')))
            },
            'reports': {
                'evaluation_reports': len(list(config.REPORTS_DIR.glob('*.json'))),
                'visualizations': len(list(config.REPORTS_DIR.glob('*.png')))
            }
        }
        
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Statistics error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/<report_name>')
def api_report(report_name):
    """Get specific report"""
    try:
        report_path = config.REPORTS_DIR / f"{report_name}.json"
        
        if not report_path.exists():
            return jsonify({'error': 'Report not found'}), 404
        
        with open(report_path, 'r') as f:
            report_data = json.load(f)
        
        return jsonify(report_data)
        
    except Exception as e:
        logger.error(f"Report error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/charts/<chart_name>')
def api_chart(chart_name):
    """Serve chart images"""
    try:
        chart_path = config.REPORTS_DIR / f"{chart_name}.png"
        
        if not chart_path.exists():
            return jsonify({'error': 'Chart not found'}), 404
        
        return send_file(chart_path, mimetype='image/png')
        
    except Exception as e:
        logger.error(f"Chart error: {e}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large errors"""
    return jsonify({'error': 'File too large. Maximum size is 100MB'}), 413


if __name__ == '__main__':
    logger.info("Starting Flask application...")
    logger.info(f"Dashboard will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
