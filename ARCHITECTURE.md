# 🏗️ Project Architecture & Technical Design

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   INPUT: PaySim Dataset                     │
│            (6.3M transactions, 11 features)                 │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────▼─────────────┐
        │  DATA EXPLORATION        │
        │ - Load CSV (Pandas)      │
        │ - Analyze statistics     │
        │ - Check missing values   │
        │ - Fraud distribution     │
        └────────────┬─────────────┘
                     │
      ┌──────────────▼──────────────┐
      │  SECURITY LAYER 🔐          │
      ├──────────────────────────────┤
      │ 1. TOKENIZATION            │
      │    nameOrig → UUID token   │
      │    nameDest → UUID token   │
      │                            │
      │ 2. ENCRYPTION (Fernet)     │
      │    Encrypt mapping dict    │
      │    Save to .bin file       │
      │                            │
      │ 3. SECURE STORAGE          │
      │    SQLite database         │
      │    Keep encryption_key.key │
      └──────────────┬──────────────┘
                     │
      ┌──────────────▼──────────────────┐
      │  PREPROCESSING PIPELINE         │
      ├──────────────────────────────────┤
      │ 1. CATEGORICAL ENCODING         │
      │    type: [CASH_IN, CASH_OUT...] │
      │    → One-hot encoding           │
      │                                 │
      │ 2. FEATURE SCALING              │
      │    amount, balance cols         │
      │    → MinMaxScaler [0, 1]        │
      │                                 │
      │ 3. DERIVED FEATURES             │
      │    (optional)                   │
      └──────────────┬──────────────────┘
                     │
      ┌──────────────▼──────────────────┐
      │  TRAIN/VAL/TEST SPLIT           │
      └──────────────┬──────────────────┘
                     │
      ┌──────────────▼──────────────────┐
      │  CLASS IMBALANCE HANDLING       │
      │  (SMOTE on training only)       │
      │  99.8% → 0.2% to 50% → 50%    │
      └──────────────┬──────────────────┘
                     │
      ┌──────────────▼──────────────────┐
      │  RESHAPE FOR 1D CNN             │
      │  (N, features) → (N, feat, 1)  │
      └──────────────┬──────────────────┘
                     │
      ┌──────────────▼──────────────────┐
      │    1D CNN ARCHITECTURE 🧠       │
      ├──────────────────────────────────┤
      │ Conv1D(32) → ReLU → BatchNorm   │
      │ MaxPool → Conv1D(64) → ReLU     │
      │ Flatten → Dense(128/64/32)      │
      │ Output: Sigmoid [0, 1]          │
      └──────────────┬──────────────────┘
                     │
      ┌──────────────▼──────────────────┐
      │    MODEL TRAINING 📈             │
      ├──────────────────────────────────┤
      │ Loss: binary_crossentropy       │
      │ Optimizer: Adam (lr decay)      │
      │ Class weights: [1, 500]         │
      │ Early stopping: patience=5      │
      │ LR reduction: factor=0.5        │
      └──────────────┬──────────────────┘
                     │
      ┌──────────────▼──────────────────┐
      │    EVALUATION & METRICS 📊      │
      ├──────────────────────────────────┤
      │ • Confusion Matrix              │
      │ • ROC Curve & AUC               │
      │ • Precision-Recall Curve        │
      │ • Classification Report         │
      │ • Fraud Detection Summary       │
      └──────────────┬──────────────────┘
                     │
        ┌────────────▼────────────┐
        │  OUTPUT: Trained Model  │
        │  - fraud_detection_cnn  │
        │  - preprocessor.pkl     │
        │  - Evaluation plots (5) │
        │  - Metrics report       │
        └─────────────────────────┘
```

## Data Flow Diagram

```
CSV Input
   ↓
DataFrame (Pandas)
   ├─ Original IDs (nameOrig, nameDest)
   ├─ Transaction type (type)
   ├─ Amount, balance info
   └─ Fraud label (isFraud)
   ↓
[TOKENIZATION]
   ├─ Generate UUIDs
   ├─ Create mapping
   └─ Replace original IDs
   ↓
Tokenized DataFrame
   ├─ UUID tokens
   ├─ Transaction features
   └─ Fraud labels
   ↓
[ENCRYPTION]
   ├─ Serialize mapping
   ├─ Encrypt with Fernet
   └─ Store in DB
   ↓
[PREPROCESSING]
   ├─ One-hot encode
   ├─ Scale features
   └─ Handle missing
   ↓
Processed Features (X) & Labels (y)
   ├─ X: (N, features)
   └─ y: (N,) or (N, 1)
   ↓
[RESHAPE FOR CNN]
   ├─ X: (N, features, 1)
   └─ y: (N,) binary labels
   ↓
[SPLIT DATA]
   ├─ Train: 64% (512K samples)
   ├─ Val: 16% (128K samples)
   └─ Test: 20% (160K samples)
   ↓
[APPLY SMOTE]
   ├─ X_train: 512K → 1M (synthetic fraud added)
   └─ y_train: 0.2% fraud → 50% fraud
   ↓
[TRAIN CNN]
   ├─ 50 epochs
   ├─ Batch size 32
   ├─ Class weights
   └─ Early stopping
   ↓
Trained Model
   ├─ Weights learned
   ├─ Fraud patterns detected
   └─ Ready for inference
   ↓
[EVALUATE]
   ├─ Predict on test set
   ├─ Generate metrics
   ├─ Create visualizations
   └─ Generate reports
   ↓
Results & Insights
```

## Module Dependencies

```
src/
├── main.py (entry point)
│   ├─ config.py (constants)
│   ├─ data_preprocessing.py
│   │   ├─ config.py
│   │   ├─ pandas, numpy, sklearn
│   │   └─ imblearn (SMOTE)
│   │
│   ├─ encryption.py
│   │   ├─ config.py
│   │   ├─ cryptography (Fernet)
│   │   └─ sqlite3
│   │
│   ├─ train.py
│   │   ├─ config.py
│   │   ├─ data_preprocessing.py
│   │   ├─ cnn_model.py
│   │   └─ tensorflow/keras
│   │
│   ├─ cnn_model.py
│   │   ├─ config.py
│   │   └─ tensorflow/keras
│   │
│   └─ evaluate.py
│       ├─ config.py
│       ├─ sklearn (metrics)
│       ├─ matplotlib, seaborn
│       └─ tensorflow/keras
│
└─ Supporting:
   ├─ utils.py (helpers)
   └─ __init__.py (package)
```

## 1D CNN Architecture Details

### Why 1D Convolution for Tabular Data?

Traditional fully connected networks:
- Treat each feature independently
- No spatial/sequential relationship
- Prone to overfitting on small datasets

1D CNN advantages:
- Learns local feature combinations
- Hierarchical feature extraction
- Fewer parameters (regularization)
- Better generalization

### Layer-by-Layer Breakdown

```
INPUT: (batch, 10 features, 1 channel)
   ↓
CONV1D: 32 filters, kernel=3
   - 10 features → 32 different patterns learned
   - Kernel slides across 3 adjacent features
   - Output: (batch, 10, 32)
   ↓
RELU ACTIVATION
   - Non-linearity for complex patterns
   ↓
BATCH NORMALIZATION
   - Normalize activations
   - Stabilize training
   - Allows higher learning rates
   ↓
MAXPOOL1D: pool_size=2
   - Takes max of each 2-element window
   - Reduces dimension: (batch, 5, 32)
   - Preserves important features
   ↓
CONV1D: 64 filters, kernel=3
   - 32 channels → 64 different patterns
   - Another level of feature combination
   - Output: (batch, 5, 64)
   ↓
RELU + BATCH NORM + MAXPOOL
   ↓
FLATTEN
   - (batch, 5, 64) → (batch, 320)
   ↓
DENSE: 128 units
   - Fully connected layer
   - Interprets learned features
   - Output: (batch, 128)
   ↓
DROPOUT: 0.3
   - Randomly drop 30% of activations
   - Prevent overfitting
   ↓
DENSE: 64 units
   - Further feature combination
   - Output: (batch, 64)
   ↓
DROPOUT: 0.3
   ↓
DENSE: 32 units
   - Final feature extraction
   - Output: (batch, 32)
   ↓
DROPOUT: 0.3
   ↓
DENSE: 1 unit with SIGMOID
   - Binary classification output
   - Output: (batch, 1) with value in [0, 1]
   - 0 = Legitimate, 1 = Fraud
```

### Activation Functions

- **ReLU** (Rectified Linear Unit): max(0, x)
  - Introduces non-linearity
  - Computationally efficient
  - Helps learn complex patterns

- **Sigmoid**: 1 / (1 + e^(-x))
  - Output range [0, 1]
  - Probability interpretation
  - Standard for binary classification

## Training Strategy

### Class Weights
```
Class 0 (Legitimate): weight = 1.0
Class 1 (Fraud):      weight = 500.0

Impact:
- Fraud misclassification costs 500x more
- Model pays attention to rare fraud
- Prevents learning "always predict legitimate"
```

### Early Stopping
```
patience = 5
- Monitor: validation loss
- If no improvement for 5 epochs → stop
- Restore best weights
- Prevent overfitting
```

### Learning Rate Schedule
```
Initial: 0.001
Reduction trigger: val_loss plateaus for 3 epochs
Factor: 0.5
Min LR: 1e-7

Adaptive learning rate:
- Fast initial learning
- Refinement in later stages
- Convergence in local minima
```

## Security Architecture

### Encryption Flow

```
Original ID: C123456789
   ↓
[UUID.uuid4()]
   ↓
Token: 550e8400-e29b-41d4-a716-446655440000
   ↓
Store in mapping:
{"C123456789": "550e8400-e29b-41d4-a716-446655440000"}
   ↓
[json.dumps() → bytes]
   ↓
[Fernet.generate_key()]
   ↓
encryption_key: gAAAAAB...
   ↓
[cipher.encrypt(mapping_bytes)]
   ↓
encrypted_mapping: gAAAAAB9V... (binary blob)
   ↓
[sqlite3] Store encrypted_mapping
   ↓
Encrypted Database
```

### Key Management
```
Generate: Fernet.generate_key()
Save to: data/encryption_key.key
Use: Store in secure vault/environment variable
Protect: Keep offline backup
Recover: Impossible without key (by design)
```

## Performance Considerations

### Memory Usage
```
Input size: 6.3M transactions × 10 features × 32-bit = 2.5GB
After SMOTE: 1M samples (training) = reasonable
Batch size 32: Process 32 samples at a time
GPU memory: ~2GB (manageable)
```

### Computation Time
```
Preprocessing: ~5 minutes (pandas operations)
SMOTE synthesis: ~2 minutes
Training 50 epochs: ~20 minutes (GPU), ~2 hours (CPU)
Evaluation: ~2 minutes
Total: 30 minutes to 2.5 hours (hardware dependent)
```

### Scaling Strategies
```
For larger datasets:
- Increase batch size (32 → 64)
- Reduce SMOTE ratio
- Use data generators
- Distributed training (multi-GPU)
- Cloud infrastructure (TPU)
```

## Evaluation Metrics Rationale

### Why Multiple Metrics?

```
Dataset: 99.8% legitimate, 0.2% fraud

Bad metric: Accuracy
- "Always predict legitimate" → 99.8% accuracy ✓ but useless ✗

Good metrics:
- Precision: TP / (TP + FP)
  "Of frauds we detect, how many are real?"
  
- Recall: TP / (TP + FN)
  "Of real frauds, how many do we catch?"
  
- F1-Score: 2 * (Precision × Recall) / (Precision + Recall)
  "Harmonic mean balances precision/recall"
  
- AUC: Area under ROC curve
  "Threshold-independent performance"
  
- PR-AUC: Precision-Recall curve
  "Better for imbalanced data"
```

### Decision Thresholds

Standard threshold: 0.5
```
if prediction > 0.5: fraud
else: legitimate
```

Adjustable thresholds:
```
Conservative (threshold=0.8): Fewer false alarms, more misses
Aggressive (threshold=0.2): More detections, more false alarms
```

---

## Summary

This architecture combines:
1. **Security**: Tokenization + Fernet encryption
2. **ML**: 1D CNN optimized for tabular fraud data
3. **Handling Imbalance**: SMOTE + class weights
4. **Evaluation**: Multiple metrics for imbalanced classification
5. **Production Ready**: Error handling, logging, documentation
