"""
Model Evaluation Module
Generates confusion matrices, classification reports, and performance metrics
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_curve,
    auc,
    precision_recall_curve,
    f1_score,
    matthews_corrcoef
)
from tensorflow import keras
from src.config import CONFUSION_MATRIX_PATH, CLASSIFICATION_REPORT_PATH


class ModelEvaluator:
    """Evaluates trained fraud detection model"""
    
    def __init__(self, model: keras.Model):
        self.model = model
        self.predictions = None
        self.y_true = None
    
    def evaluate_on_test_set(self, X_test: np.ndarray, y_test: np.ndarray) -> dict:
        """
        Evaluate model on test set
        
        Args:
            X_test: Test feature matrix
            y_test: Test labels
        
        Returns:
            Dictionary with evaluation metrics
        """
        print("\n" + "="*60)
        print("STEP: MODEL EVALUATION")
        print("="*60)
        
        print("\n→ Evaluating model on test set...")
        
        # Ensure correct data types
        X_test = X_test.astype('float32')
        y_test = y_test.astype('float32')
        
        # Get predictions
        y_pred_proba = self.model.predict(X_test, verbose=0)
        y_pred = (y_pred_proba > 0.95).astype(int).flatten()
        
        self.predictions = y_pred_proba.flatten()
        self.y_true = y_test
        
        # Basic metrics
        test_loss, test_accuracy, test_auc, test_precision, test_recall = self.model.evaluate(
            X_test, y_test,
            verbose=0
        )
        
        # Calculate additional metrics
        f1 = f1_score(y_test, y_pred)
        mcc = matthews_corrcoef(y_test, y_pred)
        
        metrics = {
            'loss': test_loss,
            'accuracy': test_accuracy,
            'auc': test_auc,
            'precision': test_precision,
            'recall': test_recall,
            'f1': f1,
            'mcc': mcc
        }
        
        print(f"\n✓ Test Set Results:")
        print(f"  Loss: {test_loss:.4f}")
        print(f"  Accuracy: {test_accuracy:.4f}")
        print(f"  AUC: {test_auc:.4f}")
        print(f"  Precision: {test_precision:.4f}")
        print(f"  Recall: {test_recall:.4f}")
        print(f"  F1-Score: {f1:.4f}")
        print(f"  MCC: {mcc:.4f}")
        
        return metrics
    
    def generate_confusion_matrix(self, y_test: np.ndarray, threshold: float = 0.95) -> np.ndarray:
        """
        Generate confusion matrix
        
        Args:
            y_test: Test labels
            threshold: Classification threshold
        
        Returns:
            Confusion matrix array
        """
        if self.predictions is None:
            raise ValueError("No predictions. Call evaluate_on_test_set() first.")
        
        y_pred = (self.predictions > threshold).astype(int)
        cm = confusion_matrix(y_test, y_pred)
        
        # Extract metrics from confusion matrix
        tn, fp, fn, tp = cm.ravel()
        
        print(f"\n→ Confusion Matrix (threshold={threshold}):")
        print(f"  True Negatives (TN): {tn}")
        print(f"  False Positives (FP): {fp}")
        print(f"  False Negatives (FN): {fn}")
        print(f"  True Positives (TP): {tp}")
        print(f"\n  Fraud Detection Rate (Recall): {tp / (tp + fn) * 100:.2f}%")
        print(f"  False Alarm Rate: {fp / (fp + tn) * 100:.2f}%")
        
        return cm
    
    def plot_confusion_matrix(self, y_test: np.ndarray, save_path: str = None, threshold: float = 0.95) -> None:
        """
        Plot confusion matrix heatmap
        
        Args:
            y_test: Test labels
            save_path: Path to save plot
            threshold: Classification threshold
        """
        if self.predictions is None:
            raise ValueError("No predictions. Call evaluate_on_test_set() first.")
        
        y_pred = (self.predictions > threshold).astype(int)
        cm = confusion_matrix(y_test, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['Legitimate', 'Fraud'],
                    yticklabels=['Legitimate', 'Fraud'])
        plt.title(f'Confusion Matrix (Threshold={threshold})')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Confusion matrix plot saved to {save_path}")
        else:
            plt.show()
    
    def generate_classification_report(self, y_test: np.ndarray, threshold: float = 0.95) -> str:
        """
        Generate detailed classification report
        
        Args:
            y_test: Test labels
            threshold: Classification threshold
        
        Returns:
            Classification report string
        """
        if self.predictions is None:
            raise ValueError("No predictions. Call evaluate_on_test_set() first.")
        
        y_pred = (self.predictions > threshold).astype(int)
        
        report = classification_report(
            y_test, y_pred,
            target_names=['Legitimate', 'Fraud'],
            digits=4
        )
        
        print(f"\n→ Classification Report (threshold={threshold}):")
        print(report)
        
        return report
    
    def save_classification_report(self, y_test: np.ndarray, save_path: str = None, threshold: float = 0.95) -> None:
        """
        Save classification report to file
        
        Args:
            y_test: Test labels
            save_path: Path to save report
            threshold: Classification threshold
        """
        report = self.generate_classification_report(y_test, threshold)
        
        save_path = save_path or str(CLASSIFICATION_REPORT_PATH)
        with open(save_path, 'w') as f:
            f.write(report)
        
        print(f"✓ Classification report saved to {save_path}")
    
    def plot_roc_curve(self, y_test: np.ndarray, save_path: str = None) -> None:
        """
        Plot ROC curve
        
        Args:
            y_test: Test labels
            save_path: Path to save plot
        """
        if self.predictions is None:
            raise ValueError("No predictions. Call evaluate_on_test_set() first.")
        
        fpr, tpr, thresholds = roc_curve(y_test, self.predictions)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC={roc_auc:.4f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve')
        plt.legend(loc="lower right")
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ ROC curve plot saved to {save_path}")
        else:
            plt.show()
    
    def plot_precision_recall_curve(self, y_test: np.ndarray, save_path: str = None) -> None:
        """
        Plot Precision-Recall curve (better for imbalanced data)
        
        Args:
            y_test: Test labels
            save_path: Path to save plot
        """
        if self.predictions is None:
            raise ValueError("No predictions. Call evaluate_on_test_set() first.")
        
        precision, recall, thresholds = precision_recall_curve(y_test, self.predictions)
        
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, color='blue', lw=2, label='Precision-Recall')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.legend(loc="upper right")
        plt.grid(True, alpha=0.3)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Precision-Recall curve plot saved to {save_path}")
        else:
            plt.show()
    
    def plot_prediction_distribution(self, save_path: str = None) -> None:
        """
        Plot distribution of prediction probabilities
        
        Args:
            save_path: Path to save plot
        """
        if self.predictions is None:
            raise ValueError("No predictions. Call evaluate_on_test_set() first.")
        
        legitimate_preds = self.predictions[self.y_true == 0]
        fraud_preds = self.predictions[self.y_true == 1]
        
        plt.figure(figsize=(10, 6))
        plt.hist(legitimate_preds, bins=50, alpha=0.7, label='Legitimate', color='green')
        plt.hist(fraud_preds, bins=50, alpha=0.7, label='Fraud', color='red')
        plt.axvline(x=0.5, color='black', linestyle='--', label='Decision Threshold')
        plt.xlabel('Prediction Probability')
        plt.ylabel('Count')
        plt.title('Distribution of Prediction Probabilities')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Prediction distribution plot saved to {save_path}")
        else:
            plt.show()
    
    def print_fraud_detection_summary(self, y_test: np.ndarray) -> None:
        """
        Print summary statistics for fraud detection
        
        Args:
            y_test: Test labels
        """
        y_pred = (self.predictions > 0.95).astype(int)
        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()
        
        print("\n" + "="*60)
        print("FRAUD DETECTION SUMMARY")
        print("="*60)
        
        print(f"\nTotal transactions: {len(y_test)}")
        print(f"Actual frauds: {np.sum(y_test == 1)}")
        print(f"Actual legitimate: {np.sum(y_test == 0)}")
        
        print(f"\nDetection Performance:")
        print(f"  ✓ Frauds caught (True Positives): {tp}")
        print(f"  ✗ Frauds missed (False Negatives): {fn}")
        print(f"  ✗ False alarms (False Positives): {fp}")
        print(f"  ✓ Legitimate correctly identified: {tn}")
        
        fraud_detection_rate = tp / (tp + fn) * 100 if (tp + fn) > 0 else 0
        false_alarm_rate = fp / (fp + tn) * 100 if (fp + tn) > 0 else 0
        
        print(f"\nKey Metrics:")
        print(f"  Fraud Detection Rate (Sensitivity/Recall): {fraud_detection_rate:.2f}%")
        print(f"  False Alarm Rate: {false_alarm_rate:.2f}%")
        print(f"  Specificity: {tn / (tn + fp) * 100:.2f}%")
        
        print("\n" + "="*60)
