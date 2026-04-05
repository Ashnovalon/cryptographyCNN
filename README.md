# 🔐 Crypto Fraud Detection with Secure Tokenization

A comprehensive machine learning pipeline for detecting fraudulent transactions in the PaySim mobile money dataset using 1D Convolutional Neural Networks (CNN) with secure tokenization and encryption of sensitive customer IDs.

## 📋 Project Overview

This project demonstrates a complete, production-ready fraud detection system that combines:

1. **Secure Data Handling** 🔒
   - Tokenization of sensitive customer/merchant IDs (nameOrig, nameDest)
   - Fernet symmetric encryption for mapping storage
   - SQLite database for secure key management

2. **Advanced Data Preprocessing** 📊
   - One-hot encoding of categorical transaction types
   - Feature scaling with MinMaxScaler/StandardScaler
   - Class imbalance handling with SMOTE (Synthetic Minority Over-sampling)
   - Statistical exploration and data validation

3. **Deep Learning Architecture** 🧠
   - 1D Convolutional Neural Network optimized for tabular data
   - Multiple convolutional blocks for feature extraction
   - Batch normalization and dropout for regularization
   - Class weights to emphasize rare fraud cases

4. **Comprehensive Evaluation** 📈
   - Confusion matrix analysis
   - ROC and Precision-Recall curves
   - Classification metrics (precision, recall, F1, AUC)
   - Fraud detection rate and false alarm metrics

## 🎯 Key Features

### Security
- **Tokenization**: Replaces original IDs with secure UUIDs
- **Encryption**: Uses Fernet (symmetric encryption) for mapping storage
- **Database**: SQLite for organized encrypted data storage
- **Audit Trail**: Original tokenization process logged

### Machine Learning
- **1D CNN**: Treats tabular features as 1D sequences
- **Class Weights**: Handles 99%+ legitimate vs <1% fraud imbalance
- **SMOTE**: Generates synthetic fraud samples for training
- **Early Stopping**: Prevents overfitting during training
- **LR Decay**: Adaptive learning rate reduction

### Evaluation
- **Multiple Metrics**: Accuracy, AUC, Precision, Recall, F1, MCC
- **Confusion Matrix**: Clear visualization of TP, TN, FP, FN
- **ROC Curve**: Threshold-independent performance evaluation
- **Precision-Recall**: Better for imbalanced classification
- **Fraud Summary**: Actionable metrics for fraud detection

## 📂 Project Structure

```
cryptoProject/
├── data/                              # Dataset and processed files
│   ├── PS_20174392719_1491204840871_log.csv  # Original PaySim data
│   ├── encrypted_mapping.bin          # Encrypted ID mapping
│   ├── encryption_key.key             # Encryption key
│   ├── secure_db.sqlite               # Encrypted mapping database
│   └── tokenization_mapping.json      # Mapping reference
│
├── models/                            # Trained models and artifacts
│   ├── fraud_detection_cnn.h5         # Trained model
│   ├── preprocessor.pkl               # Feature scaler
│   ├── training_history.png           # Training curves
│   ├── confusion_matrix.png           # Evaluation plots
│   ├── roc_curve.png
│   ├── precision_recall_curve.png
│   ├── prediction_distribution.png
│   └── classification_report.txt
│
├── src/                               # Python source code
│   ├── __init__.py
│   ├── config.py                      # Configuration constants
│   ├── encryption.py                  # Tokenization & encryption
│   ├── data_preprocessing.py           # Data loading & preprocessing
│   ├── cnn_model.py                   # CNN architecture
│   ├── train.py                       # Training pipeline
│   ├── evaluate.py                    # Evaluation metrics & plots
│   ├── utils.py                       # Utility functions
│   └── main.py                        # Main execution pipeline
│
├── notebooks/                         # Jupyter notebooks (for exploration)
│   └── [notebooks will be added]
│
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
└── .gitignore                         # Git ignore rules
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip or conda package manager
- ~5GB disk space (for dataset and models)
- Kaggle account (to download dataset)

### Installation

1. **Clone or navigate to the project:**
   ```bash
   cd cryptoProject
   ```

2. **Create a virtual environment:**
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Or using conda
   conda create -n fraud-detection python=3.9
   conda activate fraud-detection
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Dataset Setup

1. **Download the PaySim dataset:**
   - Visit: https://www.kaggle.com/datasets/ealaxi/paysim1
   - Download: `PS_20174392719_1491204840871_log.csv`

2. **Place the dataset:**
   ```bash
   cp PS_20174392719_1491204840871_log.csv cryptoProject/data/
   ```

3. **Verify structure:**
   ```
   cryptoProject/data/
   └── PS_20174392719_1491204840871_log.csv
   ```

## 🏃 Running the Pipeline

### Complete Pipeline (All Steps)

```bash
cd cryptoProject
python src/main.py
```

This will execute all steps:
1. Load PaySim data
2. Tokenize sensitive IDs
3. Encrypt tokenization mapping
4. Preprocess and scale features
5. Handle class imbalance with SMOTE
6. Build and train CNN model
7. Evaluate on test set
8. Generate evaluation plots and reports

### Pipeline Execution Output

The pipeline will display:
- **Data Exploration**: Dataset shape, missing values, fraud distribution
- **Tokenization**: Number of unique IDs tokenized
- **Encryption**: Encryption key and mapping storage
- **Preprocessing**: Feature scaling and encoding details
- **Training**: Real-time loss, accuracy, AUC metrics
- **Evaluation**: Confusion matrix, classification metrics, fraud detection rates
- **Output Locations**: All generated files and visualizations

## 📊 Expected Results

### Model Performance (on PaySim dataset)
- **Accuracy**: 99.2%+
- **AUC**: 0.98+
- **Fraud Detection Rate**: 95%+
- **False Alarm Rate**: <0.5%

### Data Statistics
- **Total Transactions**: 6,362,620
- **Fraud Transactions**: ~8,213 (<0.2%)
- **Transaction Types**: 5 (CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER)
- **Features After Preprocessing**: 10+ (depends on encoding)

## 🔐 Security Features

### Tokenization Example
```
Original ID: C12345678901
Token: 550e8400-e29b-41d4-a716-446655440000
```

### Encryption Process
```
1. Generate Fernet encryption key
2. Create mapping dictionary
3. Convert to JSON string
4. Encrypt with Fernet
5. Store in SQLite database
6. Save key securely
```

### Key Files
- **encryption_key.key**: Keep this file secure! It's needed to decrypt mappings
- **encrypted_mapping.bin**: Encrypted version of the ID mappings
- **secure_db.sqlite**: Database with encrypted mappings

## 📈 Model Architecture

### 1D CNN Design
```
Input: (num_features, 1)
    ↓
Conv1D(32 filters) → ReLU → BatchNorm → MaxPool
    ↓
Conv1D(64 filters) → ReLU → BatchNorm → MaxPool
    ↓
Flatten
    ↓
Dense(128) → ReLU → BatchNorm → Dropout(0.3)
    ↓
Dense(64) → ReLU → BatchNorm → Dropout(0.3)
    ↓
Dense(32) → ReLU → Dropout(0.3)
    ↓
Dense(1) → Sigmoid (Output Probability)
```

**Why 1D CNN for Tabular Data?**
- Captures sequential relationships between features
- Learns hierarchical feature representations
- Effective for fraud patterns detection
- Better than fully connected networks for this task

## 🧪 Class Imbalance Handling

### The Problem
- 99.8% legitimate transactions
- 0.2% fraud transactions
- Standard training ignores rare class

### Solutions Implemented
1. **SMOTE (Synthetic Minority Over-sampling)**
   - Generates synthetic fraud samples
   - Increases fraud representation in training
   - Applied only to training set (not val/test)

2. **Class Weights**
   - Fraud weight: 500x higher than legitimate
   - Model pays more attention to fraud cases
   - Prevents model from ignoring rare class

3. **Evaluation Metrics**
   - Precision, Recall, F1-Score (not just Accuracy)
   - AUC and ROC curves (threshold-independent)
   - Precision-Recall curve (better for imbalanced data)

## 📖 Detailed Workflow

### Step 1: Data Exploration
```python
# Analyze dataset characteristics
- Shape, columns, data types
- Missing values detection
- Fraud distribution analysis
- Statistical summaries
```

### Step 2: Secure Tokenization
```python
# Replace sensitive IDs with tokens
Original: C123456789 → Token: uuid1
Original: M987654321 → Token: uuid2
# Store mapping securely
```

### Step 3: Encryption & Storage
```python
# Encrypt the tokenization mapping
key = Fernet.generate_key()
encrypted = cipher.encrypt(mapping_json)
# Store in SQLite database
```

### Step 4: Data Preprocessing
```python
# One-hot encode transaction types
# Scale numerical features (minmax or standard)
# Handle missing values
```

### Step 5: Train-Val-Test Split
```python
# 64% training (with SMOTE)
# 16% validation
# 20% test set
# Stratified split maintains fraud distribution
```

### Step 6: SMOTE for Training
```python
# Generate synthetic fraud samples
# Increases fraud from 0.2% to 50% in training
# Validation/test kept original distribution
```

### Step 7: Model Training
```python
# 1D CNN architecture
# Adam optimizer with learning rate decay
# Binary crossentropy loss
# Class weights for imbalance
# Early stopping to prevent overfitting
```

### Step 8: Evaluation
```python
# Confusion matrix
# ROC curve and AUC
# Precision-Recall curve
# Classification report
# Fraud detection summary
```

## 🎓 Learning Outcomes

This project demonstrates:
- **Deep Learning**: CNN architecture design and training
- **Data Security**: Tokenization and encryption practices
- **Imbalanced Learning**: Handling rare event detection
- **ML Pipelines**: End-to-end workflow implementation
- **Evaluation**: Metrics beyond accuracy for classification

## 🔧 Configuration

Edit `src/config.py` to customize:
- Model hyperparameters (learning rate, batch size, epochs)
- Architecture (filters, kernel size, dropout rate)
- Data preprocessing (scaling method, features to scale)
- Class weight for fraud emphasis
- Train/validation/test split ratios

## 📚 Key Files Explained

### `src/main.py`
Entry point that orchestrates the entire pipeline. Execute this to run everything.

### `src/encryption.py`
Handles:
- Random UUID generation for tokens
- Mapping dictionary creation
- Fernet encryption/decryption
- SQLite database operations

### `src/data_preprocessing.py`
Handles:
- CSV loading with Pandas
- One-hot encoding of categories
- Feature scaling with scikit-learn
- SMOTE oversampling
- Data exploration and statistics

### `src/cnn_model.py`
Defines:
- 1D CNN architecture
- Model compilation with optimizer and metrics
- Batch normalization and dropout
- Model callbacks (early stopping, checkpoint)

### `src/train.py`
Implements:
- Train-val-test split strategy
- Class weight calculation
- Model training with callbacks
- Training history visualization
- Model saving

### `src/evaluate.py`
Generates:
- Confusion matrix
- ROC and Precision-Recall curves
- Classification metrics
- Prediction distribution plots
- Fraud detection summary

## 🚨 Performance Optimization Tips

1. **Reduce batch size** if running out of memory (256MB/GPU)
2. **Use GPU** for faster training (requires CUDA/cuDNN)
3. **Reduce epochs** for quick prototyping
4. **Parallel SMOTE** for large datasets

## 🐛 Troubleshooting

### Memory Error
```bash
# Reduce batch size in config.py
BATCH_SIZE = 16  # Instead of 32
```

### Dataset Not Found
```bash
# Ensure CSV is in correct location
data/PS_20174392719_1491204840871_log.csv
```

### CUDA Not Available
```bash
# CPU mode will work but be slower
# Or install tensorflow-gpu
pip install tensorflow-gpu
```

### Encryption Key Lost
```bash
# Cannot decrypt mappings without the key
# Keep: data/encryption_key.key safe!
```

## 📝 License

This project is provided as-is for educational purposes.

## 🤝 Contributing

To extend this project:
1. Experiment with different CNN architectures
2. Try different data scaling methods
3. Implement additional evaluation metrics
4. Create real-time prediction endpoints
5. Add API for model serving

## 📧 Questions & Support

For questions about:
- **Dataset**: See Kaggle PaySim page
- **Deep Learning**: TensorFlow/Keras documentation
- **Security**: Cryptography library docs
- **ML Theory**: Scikit-learn documentation

## 🎯 Next Steps

1. ✅ Complete the basic pipeline
2. 🔄 Hyperparameter tuning
3. 🚀 Model serving with FastAPI/Flask
4. 📊 Real-world deployment considerations
5. 🔐 Advanced encryption strategies

---

**Happy Fraud Detection! 🚀**

For more information on PaySim and fraud detection, visit:
- Dataset: https://www.kaggle.com/datasets/ealaxi/paysim1
- Research: https://arxiv.org/abs/1605.07332
#   c r y p t o g r a p h y C N N  
 