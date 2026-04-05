# 🔧 Advanced Configuration Guide

## Customizing Model & Training Parameters

Edit `src/config.py` to customize your experiment. This guide explains each parameter.

## Data Parameters

### `TEST_SIZE = 0.2`
- Fraction of data reserved for final testing
- Range: 0.1 - 0.3
- Default: 0.2 (20% test set)
- ⚠️ Too small: Test metrics unreliable
- ⚠️ Too large: Less training data

### `VALIDATION_SIZE = 0.2`
- Fraction of remaining (80%) data for validation
- Actual val set = 0.2 * 0.8 = 16%
- Range: 0.1 - 0.3
- Used to monitor overfitting during training

### `RANDOM_STATE = 42`
- Seed for reproducibility
- Change for different splits
- Use 42, 123, 456 for experiments

## Preprocessing Parameters

### `SCALING_METHOD = "minmax"`
Options:
- `"minmax"`: Scale to [0, 1] (recommended for neural networks)
- `"standard"`: Zero mean, unit variance (for tree models)

### `FEATURES_TO_SCALE`
```python
["amount", "oldbalanceOrig", "newbalanceOrig", 
 "oldbalanceDest", "newbalanceDest"]
```
- Which numerical columns to normalize
- Categorical columns already encoded
- Add/remove features as needed

### `CATEGORICAL_FEATURES = ["type"]`
- Columns to one-hot encode
- "type" has 5 values: CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER
- Add more if dataset has other categoricals

## Training Parameters

### `BATCH_SIZE = 32`
- Samples processed before weight update
- Smaller batch (16): Noisier gradients, more updates/epoch, slower convergence
- Larger batch (128): Smoother gradients, fewer updates/epoch, faster computation
- Memory: ~32MB per batch (GPU dependent)

**Tuning tips:**
```
Out of memory?        → Reduce to 16
Want faster learning? → Increase to 64
Very small dataset?   → Reduce to 8
Large GPU memory?     → Use 128
```

### `EPOCHS = 50`
- Number of times model sees full training data
- Larger = longer training, risk of overfitting
- Smaller = underfitting, poor performance

**Recommendations:**
```
Quick test:     20 epochs
Production:     50-100 epochs
Long training:  100-200 epochs
With early stop: Doesn't matter, will stop when ready
```

### `LEARNING_RATE = 0.001`
- Step size for weight updates
- Too high (0.1): Jumps over optima, fails to converge
- Too low (0.00001): Converges slowly, gets stuck
- Default (0.001): Good for Adam optimizer

**Learning rate schedule in code:**
```python
optimizer = keras.optimizers.Adam(learning_rate=0.001)
# Further reduced by ReduceLROnPlateau callback
```

## Model Architecture Parameters

### `NUM_FILTERS_1 = 32`
- Number of filters in first convolutional layer
- More filters = more pattern detection = more parameters
- Larger networks need more data

**Memory impact**: 32 → 64 filters ≈ 2x memory, 2x computation

### `NUM_FILTERS_2 = 64`
- Filters in second convolutional layer
- Usually larger than first layer
- Typically: NUM_FILTERS_1 * 2

### `KERNEL_SIZE = 3`
- Size of convolutional filter
- 3 = look at 3 adjacent features
- Larger (5, 7) = broader context, slower
- Smaller (2) = narrower patterns, faster

**Explanation:**
```
Kernel size 3:
[Feature1, Feature2, Feature3] → 1 output
[Feature2, Feature3, Feature4] → 1 output
etc.

Captures relationships between nearby features
```

### `POOL_SIZE = 2`
- Size of pooling window
- Takes max of each 2-element window
- Reduces spatial dimension by half
- Larger (4) = more aggressive reduction

## Dropout and Regularization

### `DROPOUT_RATE = 0.3`
- Fraction of neurons randomly disabled during training
- 0.3 = drop 30% of connections
- Prevents co-adaptation, improves generalization

**Tuning:**
```
Underfitting (train acc ≈ val acc)?  → Reduce to 0.1-0.2
Overfitting (train >> val acc)?      → Increase to 0.4-0.5
Well-balanced?                        → Keep at 0.3
```

## Class Imbalance Handling

### `FRAUD_WEIGHT = 500`
- How much more important fraud cases are
- Range: 10 - 1000
- Formula: weight_fraud = base_weight * FRAUD_WEIGHT

**Impact:**
```
FRAUD_WEIGHT = 100:  Miss more frauds, fewer false alarms
FRAUD_WEIGHT = 500:  Balanced detection/alarms
FRAUD_WEIGHT = 1000: Catch more frauds, more false alarms
```

## Model Paths

### `RAW_DATA_PATH = DATA_DIR / "PS_20174392719_1491204840871_log.csv"`
- Location of downloaded PaySim CSV
- You must place the dataset here

### `MODEL_PATH = MODELS_DIR / "fraud_detection_cnn.h5"`
- Where trained model is saved

### `PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.pkl"`
- Where feature scaler is saved

## Security Paths

### `ENCRYPTION_KEY_PATH = DATA_DIR / "encryption_key.key"`
- Encryption key location
- ⚠️ Keep this safe!
- Without it, mappings can't be decrypted

### `ENCRYPTED_MAPPING_PATH = DATA_DIR / "encrypted_mapping.bin"`
- Encrypted tokenization mapping

## Experiment Templates

### 🧪 Template 1: Quick Prototype (1-2 minutes)
```python
# src/config.py

# Smaller data
TEST_SIZE = 0.5  # Use less data
VALIDATION_SIZE = 0.5

# Faster training
EPOCHS = 10
BATCH_SIZE = 128

# Smaller model
NUM_FILTERS_1 = 16
NUM_FILTERS_2 = 32
DROPOUT_RATE = 0.2
```

### 🎯 Template 2: Production Model (20-30 minutes)
```python
# Default settings in config.py
# Already optimized for PaySim dataset
# Leave as is!
```

### 🔍 Template 3: Experiment with Hyperparameters (1 hour)
```python
# Try different learning rates
LEARNING_RATE = 0.0001  # Slower, more careful

# Larger model for better patterns
NUM_FILTERS_1 = 64
NUM_FILTERS_2 = 128

# More regularization
DROPOUT_RATE = 0.4

# More training
EPOCHS = 100
```

### 🚀 Template 4: Maximum Performance (2+ hours)
```python
# Everything bigger and better
EPOCHS = 200
BATCH_SIZE = 16  # Slower but better gradients

NUM_FILTERS_1 = 64
NUM_FILTERS_2 = 128

DROPOUT_RATE = 0.3
FRAUD_WEIGHT = 1000

# More careful learning
LEARNING_RATE = 0.0001

# More validation
VALIDATION_SIZE = 0.3
```

## Advanced Tuning Strategy

### Step 1: Baseline
Run with default config, record metrics.

### Step 2: Fix Underfitting
If train_loss ≈ val_loss ≈ high:
```python
# Increase model capacity
NUM_FILTERS_1 = 64
NUM_FILTERS_2 = 128

# More training
EPOCHS = 100

# Less regularization
DROPOUT_RATE = 0.2
```

### Step 3: Fix Overfitting
If train_loss << val_loss:
```python
# More regularization
DROPOUT_RATE = 0.5

# Smaller model
NUM_FILTERS_1 = 16
NUM_FILTERS_2 = 32

# Larger batch
BATCH_SIZE = 64

# More data
VALIDATION_SIZE = 0.1  # More training data
```

### Step 4: Optimize Fraud Detection
If recall (fraud detection rate) < 95%:
```python
# Emphasize fraud more
FRAUD_WEIGHT = 1000

# Larger model
NUM_FILTERS_1 = 64
NUM_FILTERS_2 = 128

# More training
EPOCHS = 100
```

## Monitoring During Training

Watch for:
```
✓ Loss decreasing: Good
✓ Val loss decreasing with train loss: Good
✓ AUC increasing: Good
✓ Train loss << val loss: Overfitting (increase dropout)
✓ Train loss ≈ val loss ≈ high: Underfitting (increase model)
✓ AUC plateaus early: Early stopping triggered (increase patience)
```

## Configuration Examples

### Fraud-Detection Focused (High Recall)
```python
FRAUD_WEIGHT = 1000  # Catch every fraud
NUM_FILTERS_1 = 64   # Larger model
EPOCHS = 100         # More training
DROPOUT_RATE = 0.2   # Less regularization
```

### Precision-Focused (Few False Alarms)
```python
FRAUD_WEIGHT = 100   # Be selective
NUM_FILTERS_1 = 16   # Smaller, simpler
EPOCHS = 30          # Quick training
DROPOUT_RATE = 0.5   # More regularization
```

### Balanced (Default)
```python
# Current settings - good for general use
FRAUD_WEIGHT = 500
NUM_FILTERS_1 = 32
EPOCHS = 50
DROPOUT_RATE = 0.3
```

---

## Summary Table

| Parameter | Small | Default | Large |
|-----------|-------|---------|-------|
| BATCH_SIZE | 16 | 32 | 128 |
| EPOCHS | 20 | 50 | 100 |
| NUM_FILTERS_1 | 16 | 32 | 64 |
| NUM_FILTERS_2 | 32 | 64 | 128 |
| DROPOUT_RATE | 0.1 | 0.3 | 0.5 |
| FRAUD_WEIGHT | 100 | 500 | 1000 |
| LEARNING_RATE | 0.0001 | 0.001 | 0.01 |

---

Happy tuning! 🎯
