"""
Tokenization and Encryption Module
Handles secure tokenization of sensitive IDs (nameOrig, nameDest)
and encryption of the mapping dictionary
"""
import json
import uuid
import sqlite3
from typing import Dict, Tuple
from cryptography.fernet import Fernet
from pathlib import Path
import pandas as pd
from src.config import (
    ENCRYPTION_KEY_PATH,
    ENCRYPTED_MAPPING_PATH,
    TOKENIZATION_MAPPING_PATH,
    ID_COLUMNS
)


class TokenizationManager:
    """Manages secure tokenization of sensitive IDs"""
    
    def __init__(self):
        self.mapping: Dict[str, str] = {}
        self.cipher_suite = None
        
    def generate_token(self) -> str:
        """Generate a secure random token using UUID"""
        return str(uuid.uuid4())
    
    def tokenize_column(self, series: pd.Series) -> Tuple[pd.Series, Dict[str, str]]:
        """
        Tokenize a pandas Series (e.g., nameOrig or nameDest)
        Returns the tokenized series and the mapping dictionary
        """
        unique_ids = series.unique()
        mapping = {}
        
        for original_id in unique_ids:
            if original_id not in mapping:
                mapping[original_id] = self.generate_token()
        
        # Apply mapping to create tokenized column
        tokenized_series = series.map(mapping)
        
        return tokenized_series, mapping
    
    def tokenize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Tokenize all ID columns in the dataframe
        Stores mapping for encryption
        """
        df_tokenized = df.copy()
        
        for col in ID_COLUMNS:
            if col in df_tokenized.columns:
                tokenized_col, col_mapping = self.tokenize_column(df_tokenized[col])
                df_tokenized[col] = tokenized_col
                self.mapping.update(col_mapping)
        
        return df_tokenized
    
    def save_mapping_unencrypted(self) -> None:
        """Save mapping to JSON (for reference, not secure)"""
        with open(TOKENIZATION_MAPPING_PATH, 'w') as f:
            json.dump(self.mapping, f, indent=2)
        print(f"✓ Mapping saved to {TOKENIZATION_MAPPING_PATH}")
    
    def load_mapping_unencrypted(self) -> None:
        """Load mapping from JSON"""
        if TOKENIZATION_MAPPING_PATH.exists():
            with open(TOKENIZATION_MAPPING_PATH, 'r') as f:
                self.mapping = json.load(f)
            print(f"✓ Mapping loaded from {TOKENIZATION_MAPPING_PATH}")


class EncryptionManager:
    """Manages encryption and decryption of tokenization mappings"""
    
    def __init__(self):
        self.key = None
        self.cipher_suite = None
    
    def generate_key(self) -> bytes:
        """Generate a new Fernet encryption key"""
        key = Fernet.generate_key()
        self.key = key
        self.cipher_suite = Fernet(key)
        return key
    
    def save_key(self) -> None:
        """Save encryption key to file"""
        if self.key is None:
            raise ValueError("No key generated. Call generate_key() first.")
        
        with open(ENCRYPTION_KEY_PATH, 'wb') as f:
            f.write(self.key)
        print(f"✓ Encryption key saved to {ENCRYPTION_KEY_PATH}")
    
    def load_key(self) -> bytes:
        """Load encryption key from file"""
        if not ENCRYPTION_KEY_PATH.exists():
            raise FileNotFoundError(f"Encryption key not found at {ENCRYPTION_KEY_PATH}")
        
        with open(ENCRYPTION_KEY_PATH, 'rb') as f:
            self.key = f.read()
        
        self.cipher_suite = Fernet(self.key)
        return self.key
    
    def encrypt_mapping(self, mapping: Dict[str, str]) -> bytes:
        """Encrypt a mapping dictionary"""
        if self.cipher_suite is None:
            raise ValueError("No cipher suite initialized. Load a key first.")
        
        # Convert dictionary to JSON string
        json_string = json.dumps(mapping)
        
        # Encrypt the JSON string
        encrypted_data = self.cipher_suite.encrypt(json_string.encode())
        
        return encrypted_data
    
    def decrypt_mapping(self, encrypted_data: bytes) -> Dict[str, str]:
        """Decrypt an encrypted mapping dictionary"""
        if self.cipher_suite is None:
            raise ValueError("No cipher suite initialized. Load a key first.")
        
        # Decrypt the data
        decrypted_json = self.cipher_suite.decrypt(encrypted_data)
        
        # Convert back to dictionary
        mapping = json.loads(decrypted_json.decode())
        
        return mapping
    
    def save_encrypted_mapping(self, encrypted_data: bytes) -> None:
        """Save encrypted mapping to file"""
        with open(ENCRYPTED_MAPPING_PATH, 'wb') as f:
            f.write(encrypted_data)
        print(f"✓ Encrypted mapping saved to {ENCRYPTED_MAPPING_PATH}")
    
    def load_encrypted_mapping(self) -> bytes:
        """Load encrypted mapping from file"""
        if not ENCRYPTED_MAPPING_PATH.exists():
            raise FileNotFoundError(f"Encrypted mapping not found at {ENCRYPTED_MAPPING_PATH}")
        
        with open(ENCRYPTED_MAPPING_PATH, 'rb') as f:
            encrypted_data = f.read()
        
        return encrypted_data


class SecureDatabase:
    """Stores encrypted mapping in SQLite database"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or str(Path(TOKENIZATION_MAPPING_PATH).parent / "secure_db.sqlite")
        self._initialize_db()
    
    def _initialize_db(self):
        """Create database tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS encrypted_mappings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mapping_name TEXT UNIQUE NOT NULL,
                    encrypted_data BLOB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        print(f"✓ Database initialized at {self.db_path}")
    
    def store_encrypted_mapping(self, mapping_name: str, encrypted_data: bytes):
        """Store encrypted mapping in database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO encrypted_mappings (mapping_name, encrypted_data)
                VALUES (?, ?)
            """, (mapping_name, encrypted_data))
            conn.commit()
        print(f"✓ Encrypted mapping '{mapping_name}' stored in database")
    
    def retrieve_encrypted_mapping(self, mapping_name: str) -> bytes:
        """Retrieve encrypted mapping from database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT encrypted_data FROM encrypted_mappings WHERE mapping_name = ?",
                (mapping_name,)
            )
            result = cursor.fetchone()
            
            if result is None:
                raise ValueError(f"Mapping '{mapping_name}' not found in database")
            
            return result[0]


def secure_tokenize_and_encrypt_dataset(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Full pipeline: Tokenization + Encryption
    
    Args:
        df: Original dataframe with sensitive IDs
    
    Returns:
        tokenized_df: DataFrame with tokenized IDs
        config_dict: Dictionary with key paths and metadata
    """
    print("\n" + "="*60)
    print("STEP: SECURE TOKENIZATION & ENCRYPTION")
    print("="*60)
    
    # Step 1: Generate tokens
    print("\n→ Generating tokens for sensitive IDs...")
    tokenizer = TokenizationManager()
    df_tokenized = tokenizer.tokenize_dataframe(df)
    print(f"✓ Tokenized {len(tokenizer.mapping)} unique IDs")
    
    # Step 2: Encrypt the mapping
    print("\n→ Encrypting tokenization mapping...")
    encryptor = EncryptionManager()
    key = encryptor.generate_key()
    encryptor.save_key()
    
    encrypted_mapping = encryptor.encrypt_mapping(tokenizer.mapping)
    encryptor.save_encrypted_mapping(encrypted_mapping)
    
    # Step 3: Store in secure database
    print("\n→ Storing encrypted mapping in secure database...")
    db = SecureDatabase()
    db.store_encrypted_mapping("paysim_fraud_mapping", encrypted_mapping)
    
    # Save unencrypted mapping for reference (in production, skip this)
    tokenizer.save_mapping_unencrypted()
    
    print("\n" + "="*60)
    print("✓ TOKENIZATION & ENCRYPTION COMPLETE")
    print("="*60)
    
    config = {
        "encryption_key_path": str(ENCRYPTION_KEY_PATH),
        "encrypted_mapping_path": str(ENCRYPTED_MAPPING_PATH),
        "database_path": db.db_path,
        "num_original_ids": len(tokenizer.mapping),
        "original_id_columns": ID_COLUMNS
    }
    
    return df_tokenized, config
