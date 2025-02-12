# utils.py
import logging
from functools import wraps
from typing import Callable
import json
from flask import jsonify, Response

def setup_logging():
    """Configure application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS

def error_handler(func: Callable) -> Callable:
    """Decorator for consistent error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except APIError as e:
            logger.error(f"API Error: {str(e)}")
            return jsonify({'error': e.message}), e.status_code
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    return wrapper

def clean_gemini_response(response: str) -> dict:
    """Clean and parse Gemini API response"""
    cleaned = response.strip()
    if cleaned.startswith('```json'):
        cleaned = cleaned[7:]
    if cleaned.endswith('```'):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()
    
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise APIError(f"Failed to parse Gemini response: {str(e)}", 500)