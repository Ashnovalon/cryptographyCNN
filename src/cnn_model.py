"""
CNN Model Architecture for Fraud Detection
1D Convolutional Neural Network for sequence-like tabular data
"""
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from typing import Tuple
from src.config import (
    NUM_FILTERS_1,
    NUM_FILTERS_2,
    KERNEL_SIZE,
    POOL_SIZE,
    DROPOUT_RATE,
    LEARNING_RATE
)


class FraudDetectionCNN:
    """1D CNN architecture for fraud detection"""
    
    def __init__(self, input_shape: Tuple[int, int]):
        """
        Initialize CNN model
        
        Args:
            input_shape: Tuple of (num_features, 1) - the shape after CNN reshaping
        """
        self.input_shape = input_shape
        self.model = None
        self.history = None
    
    def build_model(self) -> keras.Model:
        """
        Build 1D CNN model architecture
        
        Architecture:
        - Input: (num_features, 1)
        - Conv1D → ReLU → MaxPooling1D
        - Conv1D → ReLU → MaxPooling1D
        - Flatten
        - Dense → ReLU → Dropout
        - Dense → ReLU → Dropout
        - Output: Dense (Sigmoid for binary classification)
        """
        print("\n" + "="*60)
        print("STEP: BUILDING CNN ARCHITECTURE")
        print("="*60)
        
        print(f"\n→ Building 1D CNN with input shape: {self.input_shape}...")
        
        model = keras.Sequential([
            # First Convolutional Block
            layers.Input(shape=self.input_shape),
            layers.Conv1D(
                filters=NUM_FILTERS_1,
                kernel_size=KERNEL_SIZE,
                activation='relu',
                padding='same',
                name='conv1d_1'
            ),
            layers.BatchNormalization(name='batch_norm_1'),
            layers.MaxPooling1D(pool_size=POOL_SIZE, name='maxpool_1'),
            
            # Second Convolutional Block
            layers.Conv1D(
                filters=NUM_FILTERS_2,
                kernel_size=KERNEL_SIZE,
                activation='relu',
                padding='same',
                name='conv1d_2'
            ),
            layers.BatchNormalization(name='batch_norm_2'),
            layers.MaxPooling1D(pool_size=POOL_SIZE, name='maxpool_2'),
            
            # Flatten and Dense Layers
            layers.Flatten(name='flatten'),
            
            layers.Dense(128, activation='relu', name='dense_1'),
            layers.BatchNormalization(name='batch_norm_3'),
            layers.Dropout(DROPOUT_RATE, name='dropout_1'),
            
            layers.Dense(64, activation='relu', name='dense_2'),
            layers.BatchNormalization(name='batch_norm_4'),
            layers.Dropout(DROPOUT_RATE, name='dropout_2'),
            
            layers.Dense(32, activation='relu', name='dense_3'),
            layers.Dropout(DROPOUT_RATE, name='dropout_3'),
            
            # Output Layer
            layers.Dense(1, activation='sigmoid', name='output')
        ])
        
        self.model = model
        
        # Print model summary
        print("\n→ Model Summary:")
        model.summary()
        
        print("\n" + "="*60)
        print("✓ CNN MODEL BUILT SUCCESSFULLY")
        print("="*60)
        
        return model
    
    def compile_model(self) -> None:
        """Compile the model with optimizer, loss, and metrics"""
        if self.model is None:
            raise ValueError("Model not built. Call build_model() first.")
        
        print("\n→ Compiling model...")
        
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
            loss='binary_crossentropy',
            metrics=[
                'accuracy',
                keras.metrics.AUC(name='auc'),
                keras.metrics.Precision(name='precision'),
                keras.metrics.Recall(name='recall')
            ]
        )
        
        print("✓ Model compiled successfully")
        print(f"  Optimizer: Adam (lr={LEARNING_RATE})")
        print(f"  Loss: binary_crossentropy")
        print(f"  Metrics: accuracy, AUC, precision, recall")
    
    def get_model(self) -> keras.Model:
        """Get the compiled model"""
        if self.model is None:
            raise ValueError("Model not built. Call build_model() first.")
        return self.model
    
    def summary(self) -> None:
        """Print model summary"""
        if self.model is None:
            raise ValueError("Model not built. Call build_model() first.")
        self.model.summary()


class ModelCallbacks:
    """Custom callbacks for training monitoring"""
    
    @staticmethod
    def get_callbacks(model_path: str):
        """
        Get training callbacks
        
        Callbacks:
        - Early Stopping: Stop if validation loss doesn't improve
        - Model Checkpoint: Save best model
        - Reduce LR on Plateau: Reduce learning rate if stuck
        """
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True,
                verbose=1
            ),
            keras.callbacks.ModelCheckpoint(
                model_path,
                monitor='val_auc',
                save_best_only=True,
                verbose=1
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-7,
                verbose=1
            )
        ]
        return callbacks


def create_fraud_detection_model(input_shape: Tuple[int, int]) -> keras.Model:
    """
    Factory function to create a complete fraud detection CNN model
    
    Args:
        input_shape: Shape of input data (num_features, 1)
    
    Returns:
        Compiled Keras model ready for training
    """
    cnn = FraudDetectionCNN(input_shape)
    cnn.build_model()
    cnn.compile_model()
    return cnn.get_model()
