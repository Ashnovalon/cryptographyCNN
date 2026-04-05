# 📋 Project File Structure & Documentation Summary

Complete Crypto Fraud Detection Project - All Files Explained

## 📂 Directory Structure

```
cryptoProject/
├── README.md                      # Main project documentation
├── QUICK_START.md                # 5-minute setup guide
├── ARCHITECTURE.md               # Technical design & system architecture
├── CONFIGURATION.md              # Advanced configuration guide
│
├── data/                         # Dataset and encrypted files
│   ├── PS_20174392719_1491204840871_log.csv  # PaySim dataset (download required)
│   ├── encrypted_mapping.bin     # Encrypted ID tokenization mapping
│   ├── encryption_key.key        # 🔐 Keep safe! Encryption key
│   ├── secure_db.sqlite          # SQLite database with encrypted data
│   ├── tokenization_mapping.json # Reference mapping (non-secure)
│   └── processed_data.pkl        # Preprocessed features (if caching enabled)
│
├── models/                       # Trained models and evaluation artifacts
│   ├── fraud_detection_cnn.h5    # ✓ Trained deep learning model
│   ├── preprocessor.pkl          # Feature scaler (StandardScaler/MinMaxScaler)
│   ├── training_history.png      # 📊 Training curves (loss, accuracy, AUC)
│   ├── confusion_matrix.png      # Confusion matrix heatmap
│   ├── roc_curve.png             # ROC curve analysis
│   ├── precision_recall_curve.png # Precision-Recall curve
│   ├── prediction_distribution.png # Histogram of prediction probabilities
│   └── classification_report.txt  # Detailed evaluation metrics
│
├── src/                          # Python source code modules
│   ├── __init__.py               # Package initialization
│   │
│   ├── config.py                 # 📍 Configuration constants
│   │   ├── Path definitions (DATA_DIR, MODELS_DIR)
│   │   ├── Data parameters (TEST_SIZE, VALIDATION_SIZE)
│   │   ├── Preprocessing (SCALING_METHOD, CATEGORICAL_FEATURES)
│   │   ├── Training (EPOCHS, BATCH_SIZE, LEARNING_RATE)
│   │   ├── Model architecture (NUM_FILTERS, KERNEL_SIZE, DROPOUT_RATE)
│   │   └── Class weights for imbalance (FRAUD_WEIGHT)
│   │
│   ├── encryption.py             # 🔐 Tokenization & Encryption
│   │   ├── TokenizationManager: Generate tokens, map IDs
│   │   ├── EncryptionManager: Fernet encryption/decryption
│   │   ├── SecureDatabase: SQLite storage for encrypted data
│   │   └── secure_tokenize_and_encrypt_dataset(): Main pipeline
│   │
│   ├── data_preprocessing.py    # 📊 Data Loading & Preprocessing
│   │   ├── DataPreprocessor: Core preprocessing functions
│   │   │   ├── load_data(): Load CSV with Pandas
│   │   │   ├── explore_data(): Display statistics
│   │   │   ├── handle_missing_values(): NaN handling
│   │   │   ├── encode_categorical_features(): One-hot encoding
│   │   │   ├── scale_features(): MinMax/Standard scaling
│   │   │   └── preprocess_pipeline(): Full workflow
│   │   │
│   │   ├── SMOTEHandler: Synthetic oversampling
│   │   │   └── apply_smote(): Handle class imbalance
│   │   │
│   │   ├── prepare_training_data(): Extract X, y from dataframe
│   │   └── reshape_for_cnn(): (N, features) → (N, features, 1)
│   │
│   ├── cnn_model.py              # 🧠 1D CNN Architecture
│   │   ├── FraudDetectionCNN: Model class
│   │   │   ├── build_model(): Create 1D CNN layers
│   │   │   ├── compile_model(): Set optimizer, loss, metrics
│   │   │   └── summary(): Print architecture
│   │   │
│   │   ├── ModelCallbacks: Training callbacks
│   │   │   └── get_callbacks(): Early stopping, checkpointing
│   │   │
│   │   └── create_fraud_detection_model(): Factory function
│   │
│   ├── train.py                  # 📈 Training Pipeline
│   │   ├── ModelTrainer: Main training class
│   │   │   ├── calculate_class_weights(): Weight imbalanced data
│   │   │   ├── split_data(): Train/val/test split
│   │   │   ├── apply_smote_to_training(): Synthetic samples
│   │   │   ├── train(): Execute training loop
│   │   │   ├── plot_training_history(): Visualize learning curves
│   │   │   ├── save_model(): Export trained model
│   │   │   └── load_model(): Import saved model
│   │
│   ├── evaluate.py               # 📊 Model Evaluation
│   │   ├── ModelEvaluator: Evaluation class
│   │   │   ├── evaluate_on_test_set(): Calculate metrics
│   │   │   ├── generate_confusion_matrix(): TP/TN/FP/FN
│   │   │   ├── plot_confusion_matrix(): Heatmap visualization
│   │   │   ├── generate_classification_report(): Precision/Recall/F1
│   │   │   ├── plot_roc_curve(): ROC curve
│   │   │   ├── plot_precision_recall_curve(): For imbalanced data
│   │   │   ├── plot_prediction_distribution(): Probability histogram
│   │   │   └── print_fraud_detection_summary(): Key metrics
│   │
│   ├── utils.py                  # 🛠️ Utility Functions
│   │   ├── load_json() / save_json()
│   │   ├── print_section() / print_success()
│   │   └── print_error() / print_info()
│   │
│   └── main.py                   # 🚀 Main Pipeline Orchestrator
│       ├── Step 1: Load data
│       ├── Step 2: Tokenization & encryption
│       ├── Step 3: Preprocessing
│       ├── Step 4: Train/val/test split
│       ├── Step 5: SMOTE for training data
│       ├── Step 6: Reshape for 1D CNN
│       ├── Step 7: Model training
│       ├── Step 8: Evaluation
│       └── Step 9: Report generation
│
├── notebooks/                    # Jupyter notebooks (for exploration)
│   └── [future: Add exploratory notebooks]
│
├── requirements.txt              # 📦 Python dependencies
│   ├── Data: pandas, numpy, scipy
│   ├── ML: scikit-learn, imbalanced-learn
│   ├── DL: tensorflow, keras
│   ├── Security: cryptography
│   ├── Viz: matplotlib, seaborn
│   └── Dev: jupyter, pytest
│
├── .gitignore                    # Git ignore rules
│   ├── __pycache__/
│   ├── *.pyc
│   ├── data/*.csv (large files)
│   ├── models/*.h5 (large files)
│   └── venv/ (virtual env)
│
└── [Root files]                  # Config in workspace root
    ├── index.html
    ├── index2.html
    ├── upper.html
    ├── lower.html
    └── LICENSE (if applicable)
```

## 📖 Documentation Files

### README.md (Project Overview)
- **Purpose**: Complete project introduction
- **Contains**:
  - Project overview and features
  - Prerequisites and installation
  - Dataset setup instructions
  - Running the pipeline
  - Expected results
  - Security features explanation
  - Model architecture description
  - Troubleshooting guide
  - Next steps

### QUICK_START.md (Fast Onboarding)
- **Purpose**: Get running in 5 minutes
- **Contains**:
  - 3-step setup
  - Expected output example
  - Security files explanation
  - Model loading example
  - Optional customization
  - Troubleshooting shortcuts

### ARCHITECTURE.md (Technical Design)
- **Purpose**: Understand how everything works
- **Contains**:
  - System architecture diagram
  - Data flow visualization
  - Module dependencies
  - 1D CNN detailed architecture
  - Training strategy explanation
  - Security architecture
  - Performance considerations
  - Evaluation metrics rationale

### CONFIGURATION.md (Customization)
- **Purpose**: Tune model and training parameters
- **Contains**:
  - Detailed parameter explanations
  - Tuning recommendations
  - Experiment templates
  - Configuration examples
  - Hyperparameter strategy
  - Comparison tables

## 🐍 Python Modules Explained

### config.py (Configuration Hub)
**What it does**: Centralized configuration constants
**Use for**: Customizing training, model, and data parameters
**Key variables**:
```python
# Paths
RAW_DATA_PATH, PROCESSED_DATA_PATH, MODEL_PATH, etc.

# Data split
TEST_SIZE = 0.2
VALIDATION_SIZE = 0.2
RANDOM_STATE = 42

# Training
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001

# Model
NUM_FILTERS_1 = 32
NUM_FILTERS_2 = 64
KERNEL_SIZE = 3
DROPOUT_RATE = 0.3

# Class imbalance
FRAUD_WEIGHT = 500
```

### encryption.py (Security Layer)
**What it does**: Tokenization and encryption of sensitive data
**Main classes**:
- `TokenizationManager`: Creates UUID tokens from original IDs
- `EncryptionManager`: Fernet encryption/decryption
- `SecureDatabase`: SQLite storage for encrypted mappings
**Usage**: Called from main.py automatically

### data_preprocessing.py (Data Pipeline)
**What it does**: Load, clean, and prepare data for ML
**Main classes**:
- `DataPreprocessor`: Handles all preprocessing steps
- `SMOTEHandler`: Generates synthetic fraud samples
**Key functions**:
- `prepare_training_data()`: Extract features and labels
- `reshape_for_cnn()`: Transform to CNN input shape

### cnn_model.py (Model Architecture)
**What it does**: Define 1D CNN architecture
**Main class**:
- `FraudDetectionCNN`: Build and compile model
**Key functions**:
- `build_model()`: Create layer stack
- `compile_model()`: Set optimizer and metrics

### train.py (Training Engine)
**What it does**: Train the model with callbacks
**Main class**:
- `ModelTrainer`: Orchestrate training
**Key functions**:
- `split_data()`: Train/val/test split
- `train()`: Execute training loop
- `calculate_class_weights()`: Handle imbalance

### evaluate.py (Evaluation Suite)
**What it does**: Comprehensive model evaluation
**Main class**:
- `ModelEvaluator`: Generate metrics and plots
**Key functions**:
- `evaluate_on_test_set()`: Calculate all metrics
- `plot_confusion_matrix()`: Visualization
- `plot_roc_curve()`: ROC analysis

### main.py (Orchestrator)
**What it does**: Execute complete pipeline
**Workflow**:
1. Load data
2. Tokenize & encrypt
3. Preprocess
4. Split data
5. Apply SMOTE
6. Reshape for CNN
7. Train model
8. Evaluate
9. Generate reports

## 📊 Output Files Generated

### During Execution

```
data/
├── encrypted_mapping.bin    ← Encrypted tokenization
├── encryption_key.key       ← 🔐 Keep safe!
├── secure_db.sqlite        ← Encrypted database
└── tokenization_mapping.json ← Reference (non-secure)

models/
├── fraud_detection_cnn.h5           ← Trained model (50MB+)
├── preprocessor.pkl                 ← Feature scaler (KB)
├── training_history.png             ← Loss/acc curves
├── confusion_matrix.png             ← TP/TN/FP/FN heatmap
├── roc_curve.png                    ← ROC analysis
├── precision_recall_curve.png       ← PR curve
├── prediction_distribution.png      ← Probability histogram
└── classification_report.txt        ← Metrics summary
```

### What Each Output Means

| File | Purpose | Read With |
|------|---------|-----------|
| fraud_detection_cnn.h5 | Trained weights | TensorFlow |
| training_history.png | Learning curves | Image viewer |
| confusion_matrix.png | TP/TN/FP/FN breakdown | Image viewer |
| roc_curve.png | AUC visualization | Image viewer |
| classification_report.txt | Precision/Recall/F1 | Text editor |

## 🔄 Workflow Summary

### Data Journey
```
CSV File
  ↓
[config.py] Load with paths
  ↓
[data_preprocessing.py] Load & explore
  ↓
[encryption.py] Tokenize sensitive IDs
  ↓
[encryption.py] Encrypt mappings
  ↓
[data_preprocessing.py] Encode & scale
  ↓
[train.py] Split train/val/test
  ↓
[data_preprocessing.py] SMOTE training set
  ↓
[data_preprocessing.py] Reshape for CNN
  ↓
[cnn_model.py] Build architecture
  ↓
[train.py] Train with callbacks
  ↓
[evaluate.py] Test and visualize
  ↓
[main.py] Generate reports
```

## 💾 File Dependencies

### Import Graph
```
main.py
├── config.py
├── data_preprocessing.py
│   └── config.py
├── encryption.py
│   └── config.py
├── train.py
│   ├── config.py
│   ├── data_preprocessing.py
│   └── cnn_model.py
├── cnn_model.py
│   └── config.py
└── evaluate.py
    ├── config.py
    └── (imports visualization libraries)
```

## 🎯 Using Each Module

### To experiment with encryption:
→ Edit and run `encryption.py` directly

### To test preprocessing:
→ Run data_preprocessing functions in Jupyter

### To try different architectures:
→ Modify `cnn_model.py` build_model()

### To adjust training:
→ Edit hyperparameters in `config.py` and re-run `main.py`

### To create custom metrics:
→ Extend `evaluate.py` with new methods

---

## 📚 Reading Order

**New to the project?**
1. Start: README.md
2. Setup: QUICK_START.md
3. Deep dive: ARCHITECTURE.md
4. Customize: CONFIGURATION.md

**Want to understand security?**
1. ARCHITECTURE.md → Security Architecture section
2. Check: encryption.py code

**Want to improve accuracy?**
1. CONFIGURATION.md → Hyperparameter tuning
2. Check: train.py weights calculation

**Want to add new metrics?**
1. ARCHITECTURE.md → Evaluation metrics rationale
2. Edit: evaluate.py

---

## ✅ File Checklist

Verify all these files exist:

```
✓ README.md
✓ QUICK_START.md
✓ ARCHITECTURE.md
✓ CONFIGURATION.md
✓ requirements.txt
✓ .gitignore

✓ src/
  ✓ __init__.py
  ✓ config.py
  ✓ encryption.py
  ✓ data_preprocessing.py
  ✓ cnn_model.py
  ✓ train.py
  ✓ evaluate.py
  ✓ utils.py
  ✓ main.py

✓ data/ (empty initially)
✓ models/ (empty initially)
✓ notebooks/ (empty)
```

---

All set! Start with README.md or QUICK_START.md. 🚀
