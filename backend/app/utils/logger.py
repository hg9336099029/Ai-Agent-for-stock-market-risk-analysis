"""
Logging configuration using Loguru
"""

from loguru import logger
import sys

def setup_logger():
    """Configure logger with file and console output"""
    logger.remove()  # Remove default handler
    
    # Console output
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # File output
    logger.add(
        "logs/app.log",
        rotation="500 MB",
        retention="10 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
        level="DEBUG"
    )
    
    return logger

def get_logger():
    """Get configured logger instance"""
    return logger
