"""
Main Pipeline: Crypto Fraud Detection with Secure Tokenization
Complete end-to-end workflow for PaySim dataset analysis
"""
import sys
import numpy as np
import pandas as pd
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import (
    RAW_DATA_PATH,
    MODEL_PATH,
    PROCESSED_DATA_PATH,
    CONFUSION_MATRIX_PATH,
    CLASSIFICATION_REPORT_PATH
)
from src.data_preprocessing import (
    DataPreprocessor,
    prepare_training_data,
    reshape_for_cnn
)
from src.encryption import (
    secure_tokenize_and_encrypt_dataset
)
from src.train import ModelTrainer
from src.evaluate import ModelEvaluator


def main():
    """
    Complete pipeline execution:
    1. Load and explore PaySim data
    2. Secure tokenization of sensitive IDs
    3. Encrypt tokenization mapping
    4. Preprocess and scale features
    5. Handle class imbalance with SMOTE
    6. Build and train 1D CNN model
    7. Evaluate on test set
    """
    
    print("\n" + "#"*60)
    print("# CRYPTO FRAUD DETECTION PIPELINE")
    print("# PaySim Dataset + CNN Architecture")
    print("#"*60)
    
    # ========== STEP 1: LOAD DATA ==========
    print("\n" + "="*60)
    print("STEP 1: LOADING DATA")
    print("="*60)
    
    if not RAW_DATA_PATH.exists():
        print(f"\n✗ ERROR: Dataset not found at {RAW_DATA_PATH}")
        print("\nTo proceed, please:")
        print(f"1. Download PaySim dataset from: https://www.kaggle.com/datasets/ealaxi/paysim1")
        print(f"2. Place the CSV file (PS_20174392719_1491204840871_log.csv) in: {RAW_DATA_PATH.parent}")
        print(f"3. Run this script again")
        return
    
    preprocessor = DataPreprocessor()
    df_raw = preprocessor.load_data(str(RAW_DATA_PATH))
    
    # Reduce dataset size for faster training
    print("\n→ Sampling dataset to 1000000 rows for training...")
    df_raw = df_raw.sample(n=min(1000000, len(df_raw)), random_state=42)
    print(f"✓ Dataset size: {len(df_raw)} rows")
    
    # ========== STEP 2: TOKENIZATION & ENCRYPTION ==========
    df_tokenized, security_config = secure_tokenize_and_encrypt_dataset(df_raw)
    
    # ========== STEP 3: DATA PREPROCESSING ==========
    df_preprocessed = preprocessor.preprocess_pipeline(df_tokenized)
    
    # ========== STEP 4: PREPARE TRAINING DATA ==========
    print("\n" + "="*60)
    print("STEP 4: PREPARING TRAINING DATA")
    print("="*60)
    
    X, y = prepare_training_data(df_preprocessed)
    
    # ========== STEP 5: SPLIT DATA ==========
    print("\n" + "="*60)
    print("STEP 5: SPLITTING DATA")
    print("="*60)
    
    trainer = ModelTrainer()
    X_train, X_val, X_test, y_train, y_val, y_test = trainer.split_data(X, y)
    
    # ========== STEP 6: SKIP SMOTE (Use class weights instead) ==========
    print("\n" + "="*60)
    print("STEP 6: USING CLASS WEIGHTS (SMOTE disabled)")
    print("="*60)
    X_train_smoted, y_train_smoted = X_train, y_train
    print("✓ Using original training data with class-weighted loss")
    
    # ========== STEP 7: RESHAPE FOR CNN ==========
    
    X_train_cnn = reshape_for_cnn(X_train_smoted)
    X_val_cnn = reshape_for_cnn(X_val)
    X_test_cnn = reshape_for_cnn(X_test)
    
    # ========== STEP 8: TRAIN MODEL ==========
    print("\n" + "="*60)
    print("STEP 8: TRAINING CNN MODEL")
    print("="*60)
    
    history = trainer.train(X_train_cnn, y_train_smoted, X_val_cnn, y_val)
    
    # ========== STEP 9: SAVE MODEL ==========
    print("\n→ Saving trained model...")
    trainer.save_model()
    
    # ========== STEP 10: PLOT TRAINING HISTORY ==========
    print("\n→ Plotting training history...")
    trainer.plot_training_history(
        save_path=str(MODEL_PATH.parent / "training_history.png")
    )
    
    # ========== STEP 11: EVALUATE ON TEST SET ==========
    print("\n" + "="*60)
    print("STEP 11: MODEL EVALUATION")
    print("="*60)
    
    evaluator = ModelEvaluator(trainer.model)
    test_metrics = evaluator.evaluate_on_test_set(X_test_cnn, y_test)
    
    # ========== STEP 12: GENERATE EVALUATION PLOTS ==========
    print("\n→ Generating evaluation plots...")
    
    evaluator.plot_confusion_matrix(
        y_test,
        save_path=str(CONFUSION_MATRIX_PATH)
    )
    
    evaluator.generate_confusion_matrix(y_test)
    
    evaluator.plot_roc_curve(
        y_test,
        save_path=str(MODEL_PATH.parent / "roc_curve.png")
    )
    
    evaluator.plot_precision_recall_curve(
        y_test,
        save_path=str(MODEL_PATH.parent / "precision_recall_curve.png")
    )
    
    evaluator.plot_prediction_distribution(
        save_path=str(MODEL_PATH.parent / "prediction_distribution.png")
    )
    
    # ========== STEP 13: CLASSIFICATION REPORT ==========
    evaluator.save_classification_report(y_test)
    
    # ========== STEP 14: FRAUD DETECTION SUMMARY ==========
    evaluator.print_fraud_detection_summary(y_test)
    
    # ========== FINAL SUMMARY ==========
    print("\n" + "#"*60)
    print("# PIPELINE EXECUTION COMPLETE")
    print("#"*60)
    
    print("\n📊 RESULTS SUMMARY:")
    print(f"\n  Model Performance on Test Set:")
    print(f"    • Accuracy: {test_metrics['accuracy']:.4f}")
    print(f"    • AUC: {test_metrics['auc']:.4f}")
    print(f"    • Precision: {test_metrics['precision']:.4f}")
    print(f"    • Recall: {test_metrics['recall']:.4f}")
    print(f"    • F1-Score: {test_metrics['f1']:.4f}")
    
    print(f"\n  🔐 Security Configuration:")
    print(f"    • Encryption Key: {security_config['encryption_key_path']}")
    print(f"    • Encrypted Mapping: {security_config['encrypted_mapping_path']}")
    print(f"    • Secure Database: {security_config['database_path']}")
    print(f"    • Tokenized IDs: {security_config['num_original_ids']}")
    
    print(f"\n  📁 Output Files:")
    print(f"    • Model: {MODEL_PATH}")
    print(f"    • Training History: {MODEL_PATH.parent / 'training_history.png'}")
    print(f"    • Confusion Matrix: {CONFUSION_MATRIX_PATH}")
    print(f"    • ROC Curve: {MODEL_PATH.parent / 'roc_curve.png'}")
    print(f"    • Precision-Recall: {MODEL_PATH.parent / 'precision_recall_curve.png'}")
    print(f"    • Prediction Distribution: {MODEL_PATH.parent / 'prediction_distribution.png'}")
    print(f"    • Classification Report: {CLASSIFICATION_REPORT_PATH}")
    
    print("\n" + "#"*60)
    print("# Project completed successfully!")
    print("#"*60 + "\n")


if __name__ == "__main__":
    main()
