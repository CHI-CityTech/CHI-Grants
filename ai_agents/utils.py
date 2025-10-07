#!/usr/bin/env python3
"""
Utility functions for AI Agents in CHI-Grants System
Common helpers for file processing, configuration, and error handling.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class Config:
    """Configuration management for AI agents."""
    
    DEFAULT_CONFIG = {
        "openai_model": "gpt-4",
        "max_file_size_mb": 50,
        "max_text_length": 10000,
        "confidence_threshold": 0.7,
        "processing_timeout_seconds": 300,
        "retry_attempts": 3
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration."""
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_file and Path(config_file).exists():
            self.load_config(config_file)
        
        # Override with environment variables
        self._load_env_overrides()
    
    def load_config(self, config_file: str):
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                self.config.update(user_config)
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
    
    def _load_env_overrides(self):
        """Load configuration overrides from environment variables."""
        env_mappings = {
            'CHI_GRANTS_OPENAI_MODEL': 'openai_model',
            'CHI_GRANTS_MAX_FILE_SIZE_MB': 'max_file_size_mb',
            'CHI_GRANTS_CONFIDENCE_THRESHOLD': 'confidence_threshold'
        }
        
        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                # Try to convert to appropriate type
                if config_key in ['max_file_size_mb', 'max_text_length', 'processing_timeout_seconds', 'retry_attempts']:
                    try:
                        self.config[config_key] = int(value)
                    except ValueError:
                        pass
                elif config_key in ['confidence_threshold']:
                    try:
                        self.config[config_key] = float(value)
                    except ValueError:
                        pass
                else:
                    self.config[config_key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def save_config(self, config_file: str):
        """Save current configuration to file."""
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)


class Logger:
    """Logging utility for AI agents."""
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        """Initialize logger."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)


class FileValidator:
    """File validation utilities."""
    
    SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.txt', '.md'}
    
    @classmethod
    def is_supported_format(cls, filepath: str) -> bool:
        """Check if file format is supported."""
        return Path(filepath).suffix.lower() in cls.SUPPORTED_EXTENSIONS
    
    @classmethod
    def validate_file_size(cls, filepath: str, max_size_mb: int = 50) -> bool:
        """Validate file size."""
        file_size = Path(filepath).stat().st_size
        max_size_bytes = max_size_mb * 1024 * 1024
        return file_size <= max_size_bytes
    
    @classmethod
    def is_readable(cls, filepath: str) -> bool:
        """Check if file is readable."""
        try:
            with open(filepath, 'rb') as f:
                f.read(1024)  # Try to read first 1KB
            return True
        except Exception:
            return False
    
    @classmethod
    def validate_file(cls, filepath: str, max_size_mb: int = 50) -> tuple[bool, str]:
        """Comprehensive file validation."""
        file_path = Path(filepath)
        
        if not file_path.exists():
            return False, f"File does not exist: {filepath}"
        
        if not cls.is_supported_format(filepath):
            return False, f"Unsupported file format. Supported: {', '.join(cls.SUPPORTED_EXTENSIONS)}"
        
        if not cls.validate_file_size(filepath, max_size_mb):
            return False, f"File too large (max: {max_size_mb}MB)"
        
        if not cls.is_readable(filepath):
            return False, "File is not readable"
        
        return True, "File validation passed"


class TextProcessor:
    """Text processing utilities."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean extracted text for better AI processing."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove control characters
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
        
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        return text
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 10000) -> str:
        """Truncate text to maximum length while preserving words."""
        if len(text) <= max_length:
            return text
        
        # Find last complete word within limit
        truncated = text[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.8:  # Only truncate at word boundary if it's not too far back
            truncated = truncated[:last_space]
        
        return truncated + "..."
    
    @staticmethod
    def extract_numbers(text: str) -> List[float]:
        """Extract numeric values from text."""
        import re
        
        # Pattern for numbers (including currency and decimals)
        pattern = r'\$?[\d,]+\.?\d*'
        matches = re.findall(pattern, text)
        
        numbers = []
        for match in matches:
            try:
                # Clean and convert to float
                clean_number = match.replace('$', '').replace(',', '')
                numbers.append(float(clean_number))
            except ValueError:
                continue
        
        return numbers
    
    @staticmethod
    def extract_dates(text: str) -> List[str]:
        """Extract potential dates from text."""
        import re
        
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY or M/D/YYYY
            r'\d{1,2}-\d{1,2}-\d{4}',  # MM-DD-YYYY or M-D-YYYY
            r'[A-Za-z]+ \d{1,2}, \d{4}',  # Month DD, YYYY
            r'\d{1,2} [A-Za-z]+ \d{4}',  # DD Month YYYY
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            dates.extend(matches)
        
        return dates


class ErrorHandler:
    """Error handling utilities."""
    
    @staticmethod
    def safe_execute(func, *args, default=None, log_errors=True, **kwargs):
        """Safely execute a function with error handling."""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if log_errors:
                Logger("ErrorHandler").error(f"Error executing {func.__name__}: {e}")
            return default
    
    @staticmethod
    def retry_on_failure(func, max_attempts=3, delay=1.0):
        """Retry function execution on failure."""
        import time
        
        for attempt in range(max_attempts):
            try:
                return func()
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
                time.sleep(delay * (attempt + 1))  # Exponential backoff
    
    @staticmethod
    def create_error_report(error: Exception, context: Dict = None) -> Dict:
        """Create structured error report."""
        return {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": datetime.now().isoformat(),
            "context": context or {}
        }


class PerformanceMonitor:
    """Performance monitoring utilities."""
    
    def __init__(self):
        """Initialize performance monitor."""
        self.start_time = None
        self.checkpoints = {}
    
    def start(self):
        """Start timing."""
        self.start_time = datetime.now()
    
    def checkpoint(self, name: str):
        """Record checkpoint."""
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            self.checkpoints[name] = elapsed
    
    def get_elapsed(self) -> float:
        """Get total elapsed time."""
        if self.start_time:
            return (datetime.now() - self.start_time).total_seconds()
        return 0.0
    
    def get_report(self) -> Dict:
        """Get performance report."""
        return {
            "total_time": self.get_elapsed(),
            "checkpoints": self.checkpoints,
            "timestamp": datetime.now().isoformat()
        }


def setup_project_paths():
    """Setup Python paths for project imports."""
    import sys
    
    # Get project root directory
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    
    # Add necessary paths
    paths_to_add = [
        str(project_root / "scripts"),
        str(project_root / "ai_agents")
    ]
    
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.append(path)


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def ensure_directories(*dirs):
    """Ensure directories exist."""
    for directory in dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    # Test utilities
    config = Config()
    print("Configuration:", config.config)
    
    logger = Logger("test")
    logger.info("Testing logger functionality")
    
    # Test file validation
    is_valid, message = FileValidator.validate_file(__file__)
    print(f"File validation: {is_valid}, {message}")
    
    # Test text processing
    sample_text = "This is a  test   with   extra    spaces.\n\nAnd line breaks."
    cleaned = TextProcessor.clean_text(sample_text)
    print(f"Cleaned text: '{cleaned}'")
    
    print("Utilities test completed successfully")