"""
ML-Based Intrusion Detection System - Main Streamlit Application
"""
import streamlit as st
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

import config
from src.utils import setup_logging


# Page configuration
st.set_page_config(
    page_title=config.DASHBOARD_TITLE,
    page_icon=config.DASHBOARD_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize logging
setup_logging()

# Custom CSS for cybersecurity theme
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #00d4ff;
        --secondary-color: #8b5cf6;
        --success-color: #00ff41;
        --danger-color: #ff0000;
        --background-dark: #0a0e27;
    }
    
    /* Title styling */
    .main-title {
        color: #00d4ff;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 0 0 10px #00d4ff;
        padding: 20px;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #00d4ff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 212, 255, 0.1);
    }
    
    /* Alert box */
    .alert-box {
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid;
    }
    
    .alert-success {
        background-color: rgba(0, 255, 65, 0.1);
        border-color: #00ff41;
        color: #00ff41;
    }
    
    .alert-danger {
        background-color: rgba(255, 0, 0, 0.1);
        border-color: #ff0000;
        color: #ff0000;
    }
    
    .alert-info {
        background-color: rgba(0, 212, 255, 0.1);
        border-color: #00d4ff;
        color: #00d4ff;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e27 0%, #1e293b 100%);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #00d4ff 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function"""
    
    # Header
    st.markdown(
        f'<h1 class="main-title">{config.DASHBOARD_ICON} {config.DASHBOARD_TITLE}</h1>',
        unsafe_allow_html=True
    )
    
    # Sidebar navigation
    st.sidebar.title("🔐 Navigation")
    
    page = st.sidebar.radio(
        "Select Module",
        [
            "🏠 Overview",
            "📊 Network Traffic Analysis",
            "🛡️ Intrusion Detection",
            "⚔️ Attack Classification",
            "📈 Model Performance",
            "🔍 Feature Importance",
            "📜 Prediction History",
            "ℹ️ About"
        ]
    )
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.info(
        """
        **ML-Based IDS v1.0**
        
        Detects network intrusions using
        machine learning algorithms.
        
        📚 Dataset: CIC-IDS2017
        🤖 Models: LR, DT, RF
        """
    )
    
    # Main content area
    if page == "🏠 Overview":
        show_overview()
    elif page == "📊 Network Traffic Analysis":
        show_traffic_analysis()
    elif page == "🛡️ Intrusion Detection":
        show_intrusion_detection()
    elif page == "⚔️ Attack Classification":
        show_attack_classification()
    elif page == "📈 Model Performance":
        show_model_performance()
    elif page == "🔍 Feature Importance":
        show_feature_importance()
    elif page == "📜 Prediction History":
        show_prediction_history()
    elif page == "ℹ️ About":
        show_about()


def show_overview():
    """Display overview page"""
    from dashboard import overview
    overview.show()


def show_traffic_analysis():
    """Display network traffic analysis page"""
    from dashboard import traffic_analysis
    traffic_analysis.show()


def show_intrusion_detection():
    """Display intrusion detection page"""
    from dashboard import intrusion_detection
    intrusion_detection.show()


def show_attack_classification():
    """Display attack classification page"""
    st.header("⚔️ Attack Classification")
    st.info("""
    ### Multi-class Attack Classification
    
    This feature will classify specific attack types:
    - DoS Hulk
    - PortScan
    - DDoS
    - FTP-Patator
    - SSH-Patator
    - And more...
    
    **Status**: Binary classification (Benign/Malicious) is currently active.
    
    To enable multi-class classification:
    1. Retrain models with `binary_classification=False`
    2. Update label encoder for multiple classes
    3. Update dashboard to display specific attack types
    """)


def show_model_performance():
    """Display model performance page"""
    from dashboard import model_performance
    model_performance.show()


def show_feature_importance():
    """Display feature importance page"""
    st.header("🔍 Feature Importance")
    
    # Check for feature importance data
    importance_file = config.REPORTS_DIR / 'feature_importance.csv'
    
    if importance_file.exists():
        import pandas as pd
        import plotly.express as px
        
        importance_df = pd.read_csv(importance_file)
        
        st.subheader("Top 20 Most Important Features")
        
        top_features = importance_df.head(20)
        
        fig = px.bar(
            top_features,
            x='importance',
            y='feature',
            orientation='h',
            title='Feature Importance (Random Forest)',
            labels={'importance': 'Importance Score', 'feature': 'Feature'},
            color='importance',
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(height=600, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Show full table
        with st.expander("📋 View All Features"):
            st.dataframe(importance_df, use_container_width=True)
    else:
        st.info("""
        ### Feature Importance Analysis
        
        Feature importance helps understand which network traffic characteristics
        are most indicative of malicious activity.
        
        **To generate feature importance:**
        ```powershell
        python src/feature_engineering.py
        ```
        
        This will analyze features using Random Forest and save the results.
        """)


def show_prediction_history():
    """Display prediction history page"""
    st.header("� Prediction History")
    
    if 'last_results' in st.session_state:
        st.subheader("Recent Predictions")
        st.caption(f"Last prediction: {st.session_state.last_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        results_df = st.session_state.last_results
        
        # Summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Analyzed", f"{len(results_df):,}")
        with col2:
            benign = (results_df['Predicted_Class'] == 0).sum()
            st.metric("Benign", f"{benign:,}")
        with col3:
            malicious = (results_df['Predicted_Class'] == 1).sum()
            st.metric("Malicious", f"{malicious:,}")
        
        # Recent predictions
        st.subheader("Recent Predictions (Last 50)")
        display_cols = ['Predicted_Label', 'Confidence', 'Prediction_Timestamp']
        st.dataframe(results_df[display_cols].tail(50), use_container_width=True)
    else:
        st.info("""
        ### Prediction History
        
        No predictions have been made yet.
        
        **To start:**
        1. Navigate to **Intrusion Detection** page
        2. Upload network traffic CSV
        3. Click **Detect Intrusions**
        
        Your prediction history will appear here automatically.
        """)




def show_about():
    """Display about page"""
    st.header("ℹ️ About This Project")
    
    st.markdown("""
    ### 🛡️ ML-Based Intrusion Detection System
    
    **Version**: 1.0.0  
    **Author**: Mahak Yadav  
    **Organization**: CodeC Technologies (Internship Project)
    
    ---
    
    #### 📋 Project Description
    
    This is a machine learning-based network intrusion detection system designed to identify
    malicious network traffic patterns and classify different types of cyber attacks.
    
    #### 🎯 Key Features
    
    - **Real-time Detection**: Analyze network traffic for intrusions
    - **Multiple ML Models**: Compare Logistic Regression, Decision Tree, and Random Forest
    - **Attack Classification**: Identify specific attack types (DoS, DDoS, Port Scan, etc.)
    - **Interactive Dashboard**: User-friendly Streamlit interface
    - **Comprehensive Metrics**: Accuracy, Precision, Recall, F1-Score, ROC-AUC
    
    #### 🔧 Technology Stack
    
    - **Python 3.14**: Core programming language
    - **Scikit-learn**: Machine learning algorithms
    - **Pandas & NumPy**: Data processing
    - **Streamlit**: Web dashboard
    - **Plotly**: Interactive visualizations
    - **CIC-IDS2017**: Training dataset
    
    #### 📊 Dataset
    
    **CIC-IDS2017** - Canadian Institute for Cybersecurity IDS Dataset
    - Contains realistic network traffic data
    - Multiple attack categories
    - Over 2.8 million network flows
    
    #### ⚖️ License
    
    This project is for educational and research purposes.
    
    #### 🔗 Links
    
    - **GitHub**: [ML-Based-Intrusion-Detection-System](https://github.com/mahakyadav13-code/ML-Based-Intrusion-Detection-System)
    - **Dataset**: [CIC-IDS2017](https://www.unb.ca/cic/datasets/ids-2017.html)
    
    ---
    
    #### ⚠️ Ethical Considerations
    
    This system is intended for:
    - Educational purposes
    - Authorized network monitoring only
    - Cybersecurity research
    
    **Do NOT use for**:
    - Unauthorized network access
    - Malicious activities
    - Privacy violations
    
    ---
    
    *Built with ❤️ for cybersecurity*
    """)


if __name__ == "__main__":
    main()
