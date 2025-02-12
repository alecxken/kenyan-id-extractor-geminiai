from flask import Flask, jsonify, request
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv, set_key
import logging
import json
import os
from functools import wraps
from typing import Dict, Any

# Initialize Flask app
app = Flask(__name__)

# Configuration
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

def initialize_api_key():
    """Initialize and verify API key configuration"""
    # Load environment variables
    env_path = find_dotenv()
    if not env_path:
        # Create .env file if it doesn't exist
        with open('.env', 'w') as f:
            f.write('')
        env_path = find_dotenv()
    
    load_dotenv(env_path)
    
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        genai.configure(api_key=api_key)
        logger.info("API key loaded successfully")
    else:
        logger.warning("No API key found in environment")
    return api_key

def error_handler(func):
    """Decorator for consistent error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            return jsonify({
                'error': str(e),
                'status': 'error'
            }), 500
    return wrapper

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_json_response(response: str) -> Dict[str, Any]:
    """Clean and parse Gemini API response"""
    cleaned = response.strip()
    if cleaned.startswith('```json'):
        cleaned = cleaned[7:]
    if cleaned.endswith('```'):
        cleaned = cleaned[:-3]
    return json.loads(cleaned.strip())

@app.before_request
def check_api_key():
    """Check if API key is configured before each request"""
    if request.endpoint == 'health_check' or request.endpoint == 'set_api_key':
        return
        
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        logger.error("API key not found in environment")
        return jsonify({
            'error': 'Gemini API key not configured',
            'fix': 'Please set the API key using the /set_api_key endpoint'
        }), 400

    # Ensure Gemini is configured with the API key
    genai.configure(api_key=api_key)

@app.route('/', methods=['GET'])
@error_handler
def health_check():
    """Health check endpoint"""
    api_key_status = "configured" if os.getenv('GEMINI_API_KEY') else "not configured"
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'api_key_status': api_key_status
    })

@app.route('/set_api_key', methods=['POST'])
@error_handler
def set_api_key():
    """Set Gemini API key"""
    data = request.get_json()
    if not data or 'api_key' not in data:
        return jsonify({'error': 'API key is required'}), 400
    
    api_key = data['api_key'].strip()
    if not api_key:
        return jsonify({'error': 'API key cannot be empty'}), 400
    
    try:
        # Use dotenv to set the API key
        env_path = find_dotenv()
        set_key(env_path, 'GEMINI_API_KEY', api_key)
        
        # Update current environment
        os.environ['GEMINI_API_KEY'] = api_key
        
        # Configure Gemini with new API key
        genai.configure(api_key=api_key)
        
        logger.info("API key updated and configured successfully")
        return jsonify({
            'message': 'API key updated successfully',
            'status': 'configured'
        })
    except Exception as e:
        logger.error(f"Failed to update API key: {str(e)}")
        return jsonify({
            'error': 'Failed to update API key',
            'details': str(e)
        }), 500

@app.route('/process_image', methods=['POST'])
@error_handler
def process_image():
    """Process image using Gemini API"""
    # Validate file in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Supported types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
    
    # Read and process image
    try:
        image_bytes = file.read()
        if len(image_bytes) > MAX_FILE_SIZE:
            return jsonify({'error': 'File size too large'}), 400
        
        image_data = {
            'mime_type': file.content_type,
            'data': image_bytes
        }
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        Extract information from the image and return it in valid JSON format:
        {
            "relevant_info": {
                "serial_number": "",
                "id_number": "",
                "full_names": "",
                "date_of_birth": "",
                "sex": "",
                "district_of_birth": "",
                "place_of_issue": "",
                "date_of_issue": "",
                "country": "REPUBLIC OF KENYA"
            }
        }
        Important: Return only the JSON object, no markdown formatting or additional text.
        """
        
        # Generate response from Gemini
        response = model.generate_content([prompt, image_data])
        json_data = clean_json_response(response.text)
        
        # Clean date fields
        relevant_info = json_data.get('relevant_info', {})
        if 'date_of_issue' in relevant_info:
            relevant_info['date_of_issue'] = relevant_info['date_of_issue'].replace(' ', '')
        
        return app.response_class(
            response=json.dumps(json_data, indent=2, sort_keys=True),
            status=200,
            mimetype='application/json'
        )
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return jsonify({
            'error': 'Failed to process image',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    # Initialize API key configuration
    initialize_api_key()
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=9000)