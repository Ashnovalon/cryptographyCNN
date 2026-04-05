"""
Utility functions for fraud detection pipeline
"""
import json
from pathlib import Path


def load_json(file_path: str) -> dict:
    """Load JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)


def save_json(data: dict, file_path: str) -> None:
    """Save data to JSON file"""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def print_section(title: str) -> None:
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def print_success(message: str) -> None:
    """Print success message"""
    print(f"✓ {message}")


def print_error(message: str) -> None:
    """Print error message"""
    print(f"✗ {message}")


def print_info(message: str) -> None:
    """Print info message"""
    print(f"→ {message}")
