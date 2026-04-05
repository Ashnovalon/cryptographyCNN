"""
Training Module for Fraud Detection CNN
Handles model training with class weights for imbalanced data
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow import keras
from typing import Tuple
from src.config import (
    TEST_SIZE,
    VALIDATION_SIZE,
    RANDOM_STATE,
    BATCH_SIZE,
    EPOCHS,
    FRAUD_WEIGHT,
    MODEL_PATH
)
from src.data_preprocessing import SMOTEHandler, reshape_for_cnn
from src.cnn_model import create_fraud_detection_model, ModelCallbacks


class ModelTrainer:
    """Handles training of fraud detection model"""
    
    def __init__(self):
        self.model = None
        self.history = None
        self.class_weights = None
    
    def calculate_class_weights(self, y: np.ndarray) -> dict:
        """
        Calculate class weights to handle imbalanced fraud data
        Gives more weight to rare fraud cases
        """
        print("\n→ Calculating class weights for imbalanced data...")
        
        fraud_count = np.sum(y == 1)
        legitimate_count = np.sum(y == 0)
        total = len(y)
        
        # Weight inversely proportional to class frequency
        weight_legitimate = (1 / legitimate_count) * (total / 2.0)
        weight_fraud = (1 / fraud_count) * (total / 2.0)
        
        # Scale fraud weight
        weight_fraud *= FRAUD_WEIGHT
        
        self.class_weights = {0: weight_legitimate, 1: weight_fraud}
        
        print(f"✓ Class weights calculated:")
        print(f"  Legitimate (Class 0): {weight_legitimate:.4f}")
        print(f"  Fraud (Class 1): {weight_fraud:.4f}")
        print(f"  Weight ratio (Fraud/Legitimate): {weight_fraud / weight_legitimate:.2f}x")
        
        return self.class_weights
    
    def split_data(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Split data into train, validation, and test sets
        
        Split strategy:
        - 20% test set
        - Of remaining 80%, 20% validation
        - Remaining ~64% training
        """
        print("\n→ Splitting data into train/validation/test sets...")
        
        # First split: 80% train+val, 20% test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=y
        )
        
        # Second split: 20% validation, 80% training
        val_size_adjusted = VALIDATION_SIZE / (1 - TEST_SIZE)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp,
            test_size=val_size_adjusted,
            random_state=RANDOM_STATE,
            stratify=y_temp
        )
        
        print(f"✓ Data split complete:")
        print(f"  Train: {len(X_train)} samples ({len(X_train)/len(X)*100:.1f}%)")
        print(f"  Validation: {len(X_val)} samples ({len(X_val)/len(X)*100:.1f}%)")
        print(f"  Test: {len(X_test)} samples ({len(X_test)/len(X)*100:.1f}%)")
        print(f"\n  Train fraud rate: {np.sum(y_train==1)/len(y_train)*100:.2f}%")
        print(f"  Val fraud rate: {np.sum(y_val==1)/len(y_val)*100:.2f}%")
        print(f"  Test fraud rate: {np.sum(y_test==1)/len(y_test)*100:.2f}%")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def apply_smote_to_training(self, X_train: np.ndarray, y_train: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply SMOTE only to training data
        Never apply to validation/test to maintain realistic distribution
        """
        print("\n" + "="*60)
        print("STEP: HANDLING CLASS IMBALANCE WITH SMOTE")
        print("="*60)
        
        smote_handler = SMOTEHandler()
        X_train_smoted, y_train_smoted = smote_handler.apply_smote(X_train, y_train)
        
        print("\n" + "="*60)
        print("✓ SMOTE APPLIED")
        print("="*60)
        
        return X_train_smoted, y_train_smoted
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray,
              X_val: np.ndarray, y_val: np.ndarray) -> keras.callbacks.History:
        """
        Train the CNN model
        
        Args:
            X_train: Training features (already reshaped for CNN)
            y_train: Training labels
            X_val: Validation features
            y_val: Validation labels
        
        Returns:
            Training history object
        """
        print("\n" + "="*60)
        print("STEP: MODEL TRAINING")
        print("="*60)
        
        if self.model is None:
            # Input shape is (num_features, channels)
            input_shape = (X_train.shape[1], X_train.shape[2])
            print(f"\n→ Creating model with input shape: {input_shape}")
            self.model = create_fraud_detection_model(input_shape)
        
        # Calculate class weights
        self.calculate_class_weights(y_train)
        
        # Get callbacks
        callbacks = ModelCallbacks.get_callbacks(str(MODEL_PATH))
        
        # Train the model
        print(f"\n→ Training model for {EPOCHS} epochs...")
        print(f"  Batch size: {BATCH_SIZE}")
        print(f"  Learning rate: 0.001 (with decay)")
        print(f"  Using class weights to handle imbalance")
        
        self.history = self.model.fit(
            X_train.astype('float32'), y_train.astype('float32'),
            validation_data=(X_val.astype('float32'), y_val.astype('float32')),
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            class_weight=self.class_weights,
            callbacks=callbacks,
            verbose=1
        )
        
        print("\n" + "="*60)
        print("✓ MODEL TRAINING COMPLETE")
        print("="*60)
        
        return self.history
    
    def plot_training_history(self, save_path: str = None) -> None:
        """
        Plot training history
        """
        if self.history is None:
            raise ValueError("No training history. Train the model first.")
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Loss
        axes[0, 0].plot(self.history.history['loss'], label='Train Loss')
        axes[0, 0].plot(self.history.history['val_loss'], label='Val Loss')
        axes[0, 0].set_title('Model Loss')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Accuracy
        axes[0, 1].plot(self.history.history['accuracy'], label='Train Accuracy')
        axes[0, 1].plot(self.history.history['val_accuracy'], label='Val Accuracy')
        axes[0, 1].set_title('Model Accuracy')
        axes[0, 1].set_ylabel('Accuracy')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # AUC
        axes[1, 0].plot(self.history.history['auc'], label='Train AUC')
        axes[1, 0].plot(self.history.history['val_auc'], label='Val AUC')
        axes[1, 0].set_title('Model AUC')
        axes[1, 0].set_ylabel('AUC')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Precision & Recall
        axes[1, 1].plot(self.history.history['precision'], label='Train Precision')
        axes[1, 1].plot(self.history.history['val_precision'], label='Val Precision')
        axes[1, 1].plot(self.history.history['recall'], label='Train Recall')
        axes[1, 1].plot(self.history.history['val_recall'], label='Val Recall')
        axes[1, 1].set_title('Precision & Recall')
        axes[1, 1].set_ylabel('Score')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Training history plot saved to {save_path}")
        else:
            plt.show()
    
    def save_model(self, save_path: str = None) -> None:
        """
        Save the trained model
        """
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
        
        save_path = save_path or str(MODEL_PATH)
        self.model.save(save_path)
        print(f"✓ Model saved to {save_path}")
    
    def load_model(self, model_path: str) -> keras.Model:
        """
        Load a trained model
        """
        self.model = keras.models.load_model(model_path)
        print(f"✓ Model loaded from {model_path}")
        return self.model
