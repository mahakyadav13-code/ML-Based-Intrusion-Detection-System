# ML-Based Intrusion Detection System (IDS)

## Autonomous Development Prompt for Kiro

> **Project:** ML-Based Intrusion Detection System\
> **GitHub repository:**
> https://github.com/mahakyadav13-code/ML-Based-Intrusion-Detection-System\
> **Internship:** CodeC Technologies\
> **Target environment:** Windows\
> **Primary stack:** Python, Pandas, NumPy, Scikit-learn, Streamlit,
> Plotly, Joblib, Pytest

------------------------------------------------------------------------

## Role and objective

Act as a senior cybersecurity engineer, machine-learning engineer, data
scientist, and Python full-stack developer.

Independently plan, implement, test, and document a complete, functional
**Machine Learning-Based Intrusion Detection System**. This is an
internship project intended to demonstrate practical skills in
cybersecurity, machine learning, network traffic analysis, and Python
development.

Do not create only a frontend, mockup, or basic demonstration. Build a
working application with a reproducible machine-learning pipeline and a
usable dashboard.

## Working rules

1.  First inspect the current workspace, existing files, Git status,
    configured remotes, Python version, and available dependencies.
2.  Preserve existing work. Do not overwrite or delete files without
    inspecting them first.
3.  Work systematically through the phases below. Do not stop after
    producing a plan.
4.  Make reasonable engineering decisions independently. Ask questions
    only when a decision, permission, dataset, or external dependency is
    genuinely essential.
5.  Before destructive operations, system-level changes, or publishing
    to GitHub, explain the action and obtain my approval.
6.  Never fabricate datasets, metrics, screenshots, test results, or
    completed features.
7.  If a feature cannot be completed, document the limitation clearly
    rather than pretending it works.
8.  Keep the application compatible with Windows and provide exact
    PowerShell commands.
9.  Use safe defaults and defensive cybersecurity practices.

------------------------------------------------------------------------

## Phase 1 --- Inspect and initialize the project

Inspect the current repository and workspace before making changes.

-   Confirm whether this folder is already a Git repository.
-   Check the current branch and Git working tree.
-   Check whether the GitHub remote is already configured.
-   Do not add a duplicate remote.
-   Do not force-push or overwrite remote history.
-   Check the installed Python version.

Use or adapt this structure as appropriate:

``` text
ML-Based-Intrusion-Detection-System/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── AGENTS.md
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
├── models/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── feature_engineering.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── predict.py
│   └── utils.py
├── dashboard/
│   ├── __init__.py
│   ├── overview.py
│   ├── traffic_analysis.py
│   └── model_performance.py
├── tests/
│   ├── test_preprocessing.py
│   ├── test_prediction.py
│   └── test_model.py
├── reports/
│   └── .gitkeep
└── assets/
    └── .gitkeep
```

Improve the structure if there is a clear technical reason, and explain
the change.

## Phase 2 --- Dataset integration and preprocessing

Use a genuine, publicly available network intrusion dataset.

Preferred options:

1.  **CIC-IDS2017**
2.  **UNSW-NB15**

Document the exact dataset source, download instructions, applicable
licence or terms, selected files, target labels, and feature columns.

Implement:

-   CSV loading with Pandas.
-   Column-name normalization where appropriate.
-   Missing-value handling.
-   Duplicate handling, with a documented rationale.
-   Infinite-value handling.
-   Categorical feature encoding when required.
-   Feature scaling when required by the selected algorithm.
-   Class-distribution analysis.
-   Appropriate class-imbalance handling.
-   Reproducible train/test splitting.
-   Leakage prevention.
-   A consistent preprocessing pipeline for both training and inference.

Keep raw datasets out of Git unless they are small, legally
redistributable, and explicitly appropriate to commit. Add suitable data
directories to `.gitignore` and provide download instructions.

If the real dataset is not available, create only clearly labelled
synthetic sample data for a smoke test. Do not describe synthetic data
as real network traffic or use it to claim real-world model performance.

## Phase 3 --- Machine-learning implementation

Implement and compare:

1.  Logistic Regression
2.  Decision Tree Classifier
3.  Random Forest Classifier

Requirements:

-   Build reproducible training scripts.
-   Use a proper preprocessing and model pipeline.
-   Avoid data leakage, including leakage from preprocessing and feature
    selection.
-   Use stratified splitting when appropriate.
-   Consider class imbalance and document the selected strategy.
-   Compare models using suitable metrics.
-   Select a model using a reasoned criterion, not accuracy alone.
-   Save the fitted pipeline using Joblib.
-   Save model metadata, feature names, label mapping, and training
    configuration.
-   Implement reusable prediction functions.
-   Include feature-importance analysis where supported.

Evaluate with:

-   Accuracy
-   Precision
-   Recall
-   F1-score
-   Confusion matrix
-   Classification report
-   ROC-AUC where appropriate and mathematically valid
-   False-positive and false-negative counts

Because missed attacks are important in intrusion detection, discuss
recall and false negatives alongside precision and false positives.
State whether each metric is macro, micro, weighted, or class-specific.

Report actual results from executed experiments only. Include the
dataset split, class distribution, and relevant experimental settings so
results can be interpreted.

## Phase 4 --- Professional Streamlit dashboard

Build a polished, responsive Streamlit cybersecurity dashboard with a
consistent visual design, clear navigation, useful charts, and readable
tables.

Include these sections:

1.  Overview
2.  Network Traffic Analysis
3.  Intrusion Detection
4.  Attack Classification
5.  Model Performance
6.  Feature Importance
7.  Prediction History
8.  About the Project

Display, where supported by actual data:

-   Total records analyzed
-   Benign and malicious counts
-   Attack-category distribution
-   Detection summaries
-   Model metrics
-   Confusion matrix
-   Feature-importance chart
-   Prediction results and timestamps

Do not display fabricated or hardcoded metrics as if they were real
model results. Clearly distinguish sample/demo data from actual model
output.

## Phase 5 --- Detection functionality

Implement the following modes.

### A. CSV-based traffic analysis --- required

-   Allow users to upload a network-flow CSV.
-   Validate file type, size, columns, and input values.
-   Explain which feature schema is expected.
-   Apply the exact preprocessing pipeline used during training.
-   Reject incompatible files with actionable error messages.
-   Predict benign or malicious traffic.
-   Show attack categories only if the trained model supports them.
-   Display appropriately interpreted confidence or probability values.
-   Allow users to download prediction results as CSV.
-   Do not execute uploaded files or treat their contents as trusted.

This is the primary required detection workflow and must work without
live packet capture.

### B. Optional live network monitoring

If feasible, implement an opt-in packet-monitoring module using Scapy.

Safety and correctness requirements:

-   Disabled by default.
-   Require explicit user action and appropriate permission.
-   Capture only on an interface and network the user is authorized to
    monitor.
-   Do not capture, store, or display passwords or sensitive payload
    contents.
-   Prefer metadata and flow-level features.
-   Explain that raw packet fields may not match CIC-IDS2017 or
    UNSW-NB15 flow features.
-   Do not claim that live traffic is being classified by the trained ML
    model unless a compatible, tested feature-extraction pipeline
    exists.
-   If compatibility cannot be implemented reliably, provide packet
    statistics as a separate experimental feature and label it clearly.

Do not implement offensive actions, exploitation, credential collection,
or unauthorized monitoring.

## Phase 6 --- Security and code quality

Implement:

-   Input validation and defensive error handling.
-   Safe CSV parsing and file-size limits.
-   Clear logging without recording sensitive payloads.
-   Modular, maintainable code.
-   Reusable functions and type hints where useful.
-   Configuration separated from business logic.
-   No hardcoded credentials, tokens, or API keys.
-   Dependency versions that are compatible with the selected Python
    version.
-   Clear user-facing error messages.

Document security limitations and ethical-use boundaries.

## Phase 7 --- Automated testing

Create unit tests for:

-   Missing and infinite values.
-   Preprocessing behavior.
-   Feature ordering and schema validation.
-   Model loading.
-   Prediction output.
-   Invalid or malformed CSV files.
-   Empty inputs.
-   Dashboard data-processing functions.

Run the tests and fix failures. Include a reproducible command such as:

``` powershell
python -m pytest -q
```

Also run basic application and training smoke tests when data is
available.

## Phase 8 --- Documentation

Create a professional `README.md` containing:

1.  Project title and overview
2.  Problem statement
3.  Objectives
4.  Features
5.  Technology stack
6.  System architecture
7.  Dataset sources and download instructions
8.  Data preprocessing methodology
9.  Machine-learning algorithms
10. Evaluation methodology and actual results
11. Dashboard screenshots section
12. Installation instructions for Windows
13. Training instructions
14. Application execution instructions
15. Testing instructions
16. Project structure
17. Limitations
18. Ethical considerations
19. Future enhancements
20. Author and repository information

Include a Mermaid architecture diagram showing the flow from dataset
ingestion through preprocessing, model training/evaluation, saved model,
prediction service, and Streamlit dashboard.

Create `requirements.txt`, `.gitignore`, and an appropriate open-source
`LICENSE`. Do not invent author details or licence permissions. If the
intended licence is unclear, ask me or explain the available choices
before selecting one.

## Phase 9 --- Windows setup and execution

Provide exact PowerShell commands for a clean setup, for example:

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Provide the actual commands required by the implemented project to:

-   Download or prepare the dataset.
-   Preprocess data.
-   Train models.
-   Evaluate models.
-   Run tests.
-   Launch Streamlit.

Ensure commands match the files and entry points that actually exist. Do
not provide placeholder commands.

## Phase 10 --- GitHub readiness

Prepare the local project for:

https://github.com/mahakyadav13-code/ML-Based-Intrusion-Detection-System

Requirements:

-   Keep the existing repository history.
-   Confirm the configured remote before changing it.
-   Use the `main` branch unless the existing repository requires
    otherwise.
-   Exclude virtual environments, Python caches, temporary files, large
    raw datasets, and local secrets.
-   Include useful sample files only when safe and clearly labelled.
-   Check for accidental secrets and unnecessary large files.
-   Review `git status` and the staged diff before committing.
-   Do not push without my explicit confirmation.

Provide the exact Git commands needed to commit and publish the reviewed
work.

------------------------------------------------------------------------

## Final quality gate

Before reporting completion:

1.  Confirm all expected source files exist.
2.  Install the declared dependencies in the project environment.
3.  Run preprocessing on available data.
4.  Train and evaluate models when the genuine dataset is available.
5.  Verify that the saved pipeline can be loaded for inference.
6.  Run unit tests.
7.  Launch the Streamlit application.
8.  Test the major dashboard and CSV prediction workflows.
9.  Fix errors that can be fixed in the current environment.
10. Verify that README instructions match the implementation.
11. Review Git status and ensure no secrets or inappropriate datasets
    are staged.

If the real dataset is unavailable, report which steps were tested with
synthetic data and which real-data experiments remain pending.

## Final completion report

At the end, provide:

-   Implemented features
-   Project folder and key files
-   Dataset used and its source
-   Models trained
-   Actual evaluation metrics and test conditions
-   Unit-test results
-   Application launch status
-   Exact Windows commands to run the project
-   Known limitations and remaining tasks
-   GitHub publication instructions

**Definition of done:** The project is not complete merely because files
were generated. It is complete only to the extent that the implemented
workflows have been executed and verified. Clearly distinguish
completed, tested, partially tested, and pending work.
