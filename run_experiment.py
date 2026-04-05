#!/usr/bin/env python3
"""
Experiment Runner - Easy template for running multiple experiments
Run different configurations without manually editing files
"""
import os
import sys
import shutil
import json
from pathlib import Path
from datetime import datetime
from src.config import MODELS_DIR, DATA_DIR, RAW_DATA_PATH

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


class ExperimentRunner:
    """Run experiments with different configurations"""
    
    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.experiment_dir = MODELS_DIR / f"{experiment_name}_{self.timestamp}"
        self.experiment_dir.mkdir(parents=True, exist_ok=True)
        self.config_backup = self.experiment_dir / "config.py"
        
    def save_config_backup(self):
        """Backup the config.py before running experiment"""
        config_file = Path(__file__).parent / "src" / "config.py"
        shutil.copy(config_file, self.config_backup)
        print(f"✓ Config backed up to {self.config_backup}")
    
    def print_summary(self, metrics: dict):
        """Print experiment summary"""
        print("\n" + "="*60)
        print(f"EXPERIMENT: {self.experiment_name}")
        print("="*60)
        print(f"Results saved to: {self.experiment_dir}/")
        print(f"\nMetrics:")
        for key, value in metrics.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
        print("="*60 + "\n")
    
    def run(self):
        """Execute the main pipeline"""
        from src.main import main
        
        print(f"\n🧪 Running experiment: {self.experiment_name}")
        self.save_config_backup()
        
        try:
            main()
            print(f"\n✓ Experiment completed successfully!")
            return True
        except Exception as e:
            print(f"\n✗ Experiment failed: {e}")
            import traceback
            traceback.print_exc()
            return False


# Predefined Experiment Configurations
EXPERIMENTS = {
    "quick_test": {
        "description": "Quick 5-minute test run",
        "config": {
            "EPOCHS": 5,
            "BATCH_SIZE": 128,
            "NUM_FILTERS_1": 16,
        }
    },
    
    "baseline": {
        "description": "Default configuration (recommended first run)",
        "config": {
            # Uses all defaults from config.py
        }
    },
    
    "small_model": {
        "description": "Small model for fast experimentation",
        "config": {
            "EPOCHS": 20,
            "BATCH_SIZE": 64,
            "NUM_FILTERS_1": 16,
            "NUM_FILTERS_2": 32,
            "DROPOUT_RATE": 0.2,
        }
    },
    
    "large_model": {
        "description": "Large model for better accuracy",
        "config": {
            "EPOCHS": 100,
            "BATCH_SIZE": 16,
            "NUM_FILTERS_1": 64,
            "NUM_FILTERS_2": 128,
            "DROPOUT_RATE": 0.4,
            "LEARNING_RATE": 0.0001,
        }
    },
    
    "fraud_focused": {
        "description": "Maximize fraud detection rate (high recall)",
        "config": {
            "EPOCHS": 75,
            "BATCH_SIZE": 32,
            "NUM_FILTERS_1": 64,
            "FRAUD_WEIGHT": 1000,
            "DROPOUT_RATE": 0.2,
        }
    },
    
    "precision_focused": {
        "description": "Minimize false alarms (high precision)",
        "config": {
            "EPOCHS": 50,
            "BATCH_SIZE": 32,
            "NUM_FILTERS_1": 32,
            "FRAUD_WEIGHT": 100,
            "DROPOUT_RATE": 0.5,
        }
    },
    
    "production": {
        "description": "Production-ready model (long training)",
        "config": {
            "EPOCHS": 200,
            "BATCH_SIZE": 16,
            "NUM_FILTERS_1": 64,
            "NUM_FILTERS_2": 128,
            "FRAUD_WEIGHT": 500,
            "LEARNING_RATE": 0.0001,
            "DROPOUT_RATE": 0.3,
        }
    },
    
    "hyperparameter_search_1": {
        "description": "High learning rate experiment",
        "config": {
            "EPOCHS": 30,
            "LEARNING_RATE": 0.01,
            "BATCH_SIZE": 32,
        }
    },
    
    "hyperparameter_search_2": {
        "description": "Low learning rate experiment",
        "config": {
            "EPOCHS": 100,
            "LEARNING_RATE": 0.00001,
            "BATCH_SIZE": 16,
        }
    },
}


def list_experiments():
    """Print available experiments"""
    print("\n" + "="*60)
    print("AVAILABLE EXPERIMENTS")
    print("="*60)
    for name, details in EXPERIMENTS.items():
        print(f"\n  {name}")
        print(f"    {details['description']}")
        if details['config']:
            print("    Config overrides:")
            for key, value in details['config'].items():
                print(f"      - {key}: {value}")
    print("\n" + "="*60 + "\n")


def apply_config_overrides(overrides: dict):
    """Apply configuration overrides to config.py"""
    config_path = Path(__file__).parent / "src" / "config.py"
    
    with open(config_path, 'r') as f:
        content = f.read()
    
    for key, value in overrides.items():
        # Simple replacement - assumes format: KEY = value
        old_pattern = f"{key} = "
        
        # Find the current value
        for line in content.split('\n'):
            if line.strip().startswith(f"{key} = "):
                old_line = line.strip()
                # Handle different value types
                if isinstance(value, str) and not (value.startswith('"') or value.startswith("'")):
                    new_line = f"{key} = \"{value}\""
                else:
                    new_line = f"{key} = {value}"
                
                content = content.replace(old_line, new_line)
                print(f"  {old_line} → {new_line}")
                break
    
    with open(config_path, 'w') as f:
        f.write(content)
    
    print(f"\n✓ Config updated")


def run_experiment(experiment_name: str):
    """Run a predefined experiment"""
    if experiment_name not in EXPERIMENTS:
        print(f"\n✗ Unknown experiment: {experiment_name}")
        list_experiments()
        return
    
    if not RAW_DATA_PATH.exists():
        print(f"\n✗ Dataset not found at {RAW_DATA_PATH}")
        print("\nPlease download PaySim dataset from:")
        print("  https://www.kaggle.com/datasets/ealaxi/paysim1")
        return
    
    experiment = EXPERIMENTS[experiment_name]
    
    print(f"\n{'='*60}")
    print(f"EXPERIMENT: {experiment_name}")
    print(f"{'='*60}")
    print(f"Description: {experiment['description']}")
    
    if experiment['config']:
        print(f"\nConfiguration overrides:")
        apply_config_overrides(experiment['config'])
    
    # Run the experiment
    runner = ExperimentRunner(experiment_name)
    success = runner.run()
    
    if success:
        print(f"\n✓ Experiment '{experiment_name}' completed!")
        print(f"  Results: {runner.experiment_dir}/")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run fraud detection experiments with different configurations"
    )
    parser.add_argument(
        "experiment",
        nargs="?",
        help="Experiment name (use 'list' to see available experiments)"
    )
    
    args = parser.parse_args()
    
    if not args.experiment or args.experiment.lower() == "list":
        list_experiments()
    else:
        run_experiment(args.experiment)


if __name__ == "__main__":
    main()
    
"""
USAGE EXAMPLES:

1. List all experiments:
   python run_experiment.py list
   python run_experiment.py

2. Run quick test:
   python run_experiment.py quick_test

3. Run baseline (default config):
   python run_experiment.py baseline

4. Run small model:
   python run_experiment.py small_model

5. Run large model:
   python run_experiment.py large_model

6. Run fraud-focused model:
   python run_experiment.py fraud_focused

7. Run production model:
   python run_experiment.py production

EXPERIMENT DESCRIPTIONS:

- quick_test: 5-minute sanity check (5 epochs)
- baseline: Default settings - recommended starting point
- small_model: Small arch for quick iteration (20 epochs)
- large_model: Larger arch for better accuracy (100 epochs)
- fraud_focused: Maximize fraud detection rate (Recall-optimized)
- precision_focused: Minimize false alarms (Precision-optimized)
- production: Best model - long training (200 epochs)
- hyperparameter_search_1/2: Explore learning rates

TIPS:
- Start with 'baseline' or 'quick_test'
- Compare results across experiments
- Check models/<exp_name>_<timestamp>/ for results
- Each experiment backs up its configuration
"""
