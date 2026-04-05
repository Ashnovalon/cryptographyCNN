"""
Configuration settings for the Crypto Fraud Detection Project
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# Dataset paths
RAW_DATA_PATH = DATA_DIR / "PS_20174392719_1491204439457_log.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed_data.pkl"
TOKENIZATION_MAPPING_PATH = DATA_DIR / "tokenization_mapping.json"
ENCRYPTED_MAPPING_PATH = DATA_DIR / "encrypted_mapping.bin"
ENCRYPTION_KEY_PATH = DATA_DIR / "encryption_key.key"

# Model paths
MODEL_PATH = MODELS_DIR / "fraud_detection_cnn.h5"
PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.pkl"

# Data preprocessing parameters
TEST_SIZE = 0.2
VALIDATION_SIZE = 0.2
RANDOM_STATE = 42

# Training parameters
BATCH_SIZE = 32
EPOCHS = 30
LEARNING_RATE = 0.001
DROPOUT_RATE = 0.2

# Model architecture parameters
NUM_FILTERS_1 = 64
NUM_FILTERS_2 = 128
KERNEL_SIZE = 3
POOL_SIZE = 2

# Feature scaling
SCALING_METHOD = "minmax"  # "minmax" or "standard"
FEATURES_TO_SCALE = ["amount", "oldbalanceOrig", "newbalanceOrig", "oldbalanceDest", "newbalanceDest"]

# Categorical features
CATEGORICAL_FEATURES = ["type"]

# Target variable
TARGET_COLUMN = "isFraud"

# ID columns to tokenize
ID_COLUMNS = ["nameOrig", "nameDest"]

# Class weight for imbalanced data
FRAUD_WEIGHT = 500  # Give more weight to fraud cases

# Evaluation metrics
CONFUSION_MATRIX_PATH = MODELS_DIR / "confusion_matrix.png"
CLASSIFICATION_REPORT_PATH = MODELS_DIR / "classification_report.txt"
