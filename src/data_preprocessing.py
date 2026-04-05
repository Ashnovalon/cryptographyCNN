"""
Data Preprocessing Module for PaySim Fraud Detection
Handles loading, cleaning, feature engineering, and scaling
"""
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from imblearn.over_sampling import SMOTE
from typing import Tuple
from src.config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    PREPROCESSOR_PATH,
    TEST_SIZE,
    VALIDATION_SIZE,
    RANDOM_STATE,
    CATEGORICAL_FEATURES,
    FEATURES_TO_SCALE,
    TARGET_COLUMN,
    SCALING_METHOD
)


class DataPreprocessor:
    """Handles data loading, cleaning, and preprocessing"""
    
    def __init__(self):
        self.scaler = None
        self.original_columns = None
        self.features_to_scale = FEATURES_TO_SCALE
        self.scaled_features = None
    
    def load_data(self, csv_path: str) -> pd.DataFrame:
        """Load PaySim dataset from CSV"""
        print(f"\n→ Loading data from {csv_path}...")
        df = pd.read_csv(csv_path)
        print(f"✓ Loaded {len(df)} rows and {len(df.columns)} columns")
        print(f"✓ Columns: {list(df.columns)}")
        return df
    
    def explore_data(self, df: pd.DataFrame) -> None:
        """Print data exploration statistics"""
        print("\n" + "="*60)
        print("DATA EXPLORATION")
        print("="*60)
        print(f"\nDataset shape: {df.shape}")
        print(f"\nFirst few rows:\n{df.head()}")
        print(f"\nData types:\n{df.dtypes}")
        print(f"\nMissing values:\n{df.isnull().sum()}")
        
        if TARGET_COLUMN in df.columns:
            fraud_dist = df[TARGET_COLUMN].value_counts()
            print(f"\nFraud distribution:\n{fraud_dist}")
            print(f"Fraud rate: {df[TARGET_COLUMN].mean() * 100:.2f}%")
        
        print(f"\nBasic statistics:\n{df.describe()}")
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values"""
        print("\n→ Handling missing values...")
        
        missing_count = df.isnull().sum().sum()
        if missing_count > 0:
            print(f"  Found {missing_count} missing values")
            # Forward fill for time-series data, then backfill
            df = df.fillna(method='ffill').fillna(method='bfill')
            print(f"✓ Missing values handled")
        else:
            print("✓ No missing values found")
        
        return df
    
    def encode_categorical_features(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """Encode categorical features using one-hot encoding"""
        print("\n→ Encoding categorical features...")
        
        df_encoded = df.copy()
        
        for col in CATEGORICAL_FEATURES:
            if col in df_encoded.columns:
                print(f"  One-hot encoding '{col}': {df_encoded[col].unique()}")
                encoded = pd.get_dummies(df_encoded[col], prefix=col, drop_first=False)
                df_encoded = pd.concat([df_encoded.drop(col, axis=1), encoded], axis=1)
        
        print(f"✓ Categorical features encoded. New shape: {df_encoded.shape}")
        return df_encoded
    
    def scale_features(self, df: pd.DataFrame, fit: bool = True) -> Tuple[pd.DataFrame, object]:
        """Scale numerical features"""
        print("\n→ Scaling features...")
        
        # Identify features to scale (those that exist in the dataframe)
        features_to_scale = [f for f in self.features_to_scale if f in df.columns]
        
        if not features_to_scale:
            print("✓ No features to scale found")
            return df, None
        
        df_scaled = df.copy()
        
        # Create or use existing scaler
        if fit or self.scaler is None:
            if SCALING_METHOD == "standard":
                self.scaler = StandardScaler()
            else:
                self.scaler = MinMaxScaler()
            
            scaled_values = self.scaler.fit_transform(df_scaled[features_to_scale])
        else:
            scaled_values = self.scaler.transform(df_scaled[features_to_scale])
        
        df_scaled[features_to_scale] = scaled_values
        
        print(f"✓ Scaled {len(features_to_scale)} features using {SCALING_METHOD} scaling")
        print(f"  Scaled features: {features_to_scale}")
        
        return df_scaled, self.scaler
    
    def save_preprocessor(self) -> None:
        """Save scaler and preprocessing configuration"""
        if self.scaler is not None:
            with open(PREPROCESSOR_PATH, 'wb') as f:
                pickle.dump(self.scaler, f)
            print(f"✓ Preprocessor saved to {PREPROCESSOR_PATH}")
    
    def load_preprocessor(self) -> None:
        """Load scaler from saved file"""
        if PREPROCESSOR_PATH.exists():
            with open(PREPROCESSOR_PATH, 'rb') as f:
                self.scaler = pickle.load(f)
            print(f"✓ Preprocessor loaded from {PREPROCESSOR_PATH}")
    
    def preprocess_pipeline(self, df: pd.DataFrame) -> pd.DataFrame:
        """Full preprocessing pipeline"""
        print("\n" + "="*60)
        print("STEP: DATA PREPROCESSING")
        print("="*60)
        
        # Store original columns
        self.original_columns = df.columns.tolist()
        
        # Step 1: Data exploration
        self.explore_data(df)
        
        # Step 2: Handle missing values
        df = self.handle_missing_values(df)
        
        # Step 3: Encode categorical features
        df = self.encode_categorical_features(df, fit=True)
        
        # Step 4: Scale features
        df, self.scaler = self.scale_features(df, fit=True)
        
        # Step 5: Save preprocessor
        self.save_preprocessor()
        
        print("\n" + "="*60)
        print("✓ PREPROCESSING COMPLETE")
        print("="*60)
        
        return df


class SMOTEHandler:
    """Handles synthetic oversampling for imbalanced fraud data"""
    
    def __init__(self, random_state: int = RANDOM_STATE):
        self.random_state = random_state
        self.smote = SMOTE(random_state=random_state)
    
    def apply_smote(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Apply SMOTE to handle class imbalance"""
        print("\n→ Applying SMOTE for class imbalance handling...")
        
        initial_fraud_count = np.sum(y == 1)
        X_smoted, y_smoted = self.smote.fit_resample(X, y)
        
        # Ensure correct data types for TensorFlow compatibility
        X_smoted = X_smoted.astype('float32')
        y_smoted = y_smoted.astype('float32')
        
        final_fraud_count = np.sum(y_smoted == 1)
        
        print(f"✓ SMOTE Applied:")
        print(f"  Original fraud cases: {initial_fraud_count}")
        print(f"  After SMOTE fraud cases: {final_fraud_count}")
        print(f"  Total samples after SMOTE: {len(X_smoted)}")
        print(f"  New fraud rate: {final_fraud_count / len(X_smoted) * 100:.2f}%")
        
        return X_smoted, y_smoted


def prepare_training_data(df_preprocessed: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """
    Prepare training data from preprocessed dataframe
    
    Returns:
        X: Features array
        y: Target array
    """
    print("\n→ Preparing training tensors...")
    
    # Separate features and target
    if TARGET_COLUMN not in df_preprocessed.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found in dataframe")
    
    y = df_preprocessed[TARGET_COLUMN].values
    
    # Drop target column and ID columns (nameOrig, nameDest)
    X_df = df_preprocessed.drop(TARGET_COLUMN, axis=1)
    X_df = X_df.drop(['nameOrig', 'nameDest'], axis=1, errors='ignore')
    X = X_df.values.astype('float32')
    y = y.astype('float32')
    
    print(f"✓ Features shape: {X.shape}")
    print(f"✓ Target shape: {y.shape}")
    print(f"✓ Fraud ratio: {np.sum(y == 1) / len(y) * 100:.2f}%")
    
    return X, y


def reshape_for_cnn(X: np.ndarray) -> np.ndarray:
    """
    Reshape tabular data for 1D CNN
    From (samples, features) to (samples, features, 1)
    """
    print("\n→ Reshaping data for 1D CNN...")
    
    # Ensure float32 dtype and reshape
    X = X.astype('float32') if X.dtype != np.float32 else X
    X_reshaped = np.reshape(X, (X.shape[0], X.shape[1], 1))
    
    print(f"✓ Original shape: {X.shape}")
    print(f"✓ Reshaped for CNN: {X_reshaped.shape}")
    print(f"  (samples={X_reshaped.shape[0]}, features={X_reshaped.shape[1]}, channels={X_reshaped.shape[2]})")
    
    return X_reshaped
