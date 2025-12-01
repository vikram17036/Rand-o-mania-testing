"""
Simple file-based logging utility.
Logs to logs/app.log file with timestamp and level.
"""

import os
import logging
from datetime import datetime
from pathlib import Path


class SimpleLogger:
    """Simple file-based logger for the application."""
    
    def __init__(self, log_file: str = "logs/app.log"):
        """
        Initialize the logger.
        
        Args:
            log_file: Path to the log file
        """
        self.log_file = log_file
        self._ensure_log_directory()
        self._setup_logger()
    
    def _ensure_log_directory(self):
        """Create logs directory if it doesn't exist."""
        log_path = Path(self.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _setup_logger(self):
        """Setup the file logger."""
        # Create logger
        self.logger = logging.getLogger("randomania")
        self.logger.setLevel(logging.INFO)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # Create file handler
        file_handler = logging.FileHandler(self.log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        """Log an info message."""
        self.logger.info(message)
    
    def error(self, message: str):
        """Log an error message."""
        self.logger.error(message)
    
    def debug(self, message: str):
        """Log a debug message."""
        self.logger.debug(message)
    
    def log_request(self, prompt: str, client_ip: str = None):
        """Log an incoming request."""
        ip_info = f" from {client_ip}" if client_ip else ""
        self.info(f"REQUEST{ip_info}: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")
    
    def log_response(self, result: float, random_count: int, success: bool = True):
        """Log a response."""
        status = "SUCCESS" if success else "FAILED"
        self.info(f"RESPONSE [{status}]: result={result}, random_numbers_count={random_count}")
    
    def log_error(self, error_message: str, error_type: str = None):
        """Log an error."""
        error_type_info = f" [{error_type}]" if error_type else ""
        self.error(f"ERROR{error_type_info}: {error_message}")


# Global logger instance
_logger_instance = None


def get_logger() -> SimpleLogger:
    """Get the global logger instance."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = SimpleLogger()
    return _logger_instance

print('test')