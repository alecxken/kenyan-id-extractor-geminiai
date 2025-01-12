from flask import Flask, jsonify, request
import pathlib
import json
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/set_api_key', methods=['POST'])
def set_api_key():
    data = request.get_json()
    if not data or 'api_key' not in data:
        return jsonify({'error': 'API key is required'}), 400
    
    # Save API key to .env file
    with open('.env', 'w') as f:
        f.write(f'GEMINI_API_KEY={data["api_key"]}')
    
    # Configure Gemini with new API key
    genai.configure(api_key=data['api_key'])
    return jsonify({'message': 'API key updated successfully'})

@app.route('/process_image', methods=['POST'])
def process_image():
    # Check if API key is configured
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return jsonify({'error': 'Gemini API key not configured'}), 400
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    image_bytes = file.read()
    
    image_data = {
        'mime_type': file.content_type,
        'data': image_bytes
    }
    
    # Initialize model with current API key
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """
    Extract information from the image in the following JSON format:
    'relevant_info': {
        'serial_number',
        'full_names',
        'date_of_birth',
        'sex',
        'district_of_birth',
        'place_of_issue',
        'date_of_issue',
        'country': 'REPUBLIC OF KENYA'
    }
    """
    
    response = model.generate_content([prompt, image_data])
    text_response = response.text
    
    return jsonify({'text_response': text_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)