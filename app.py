from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Azure OCR credentials from environment variables
AZURE_OCR_ENDPOINT = os.getenv("AZURE_OCR_ENDPOINT")
AZURE_OCR_KEY = os.getenv("AZURE_OCR_KEY")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        app.logger.error('No file part in the request')
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    
    if file.filename == '':
        app.logger.error('No selected file')
        return jsonify({"error": "No selected file"}), 400

    if file:
        try:
            img_bytes = file.read()
            extracted_text = azure_ocr(img_bytes)
            return jsonify({"extracted_text": extracted_text})
        except Exception as e:
            app.logger.error(f'Error processing image: {e}')
            return jsonify({"error": "Error processing the image"}), 500

def azure_ocr(image_bytes):
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_OCR_KEY,
        'Content-Type': 'application/octet-stream'
    }

    response = requests.post(
        AZURE_OCR_ENDPOINT + "vision/v3.2/ocr",
        headers=headers,
        data=image_bytes
    )
    response.raise_for_status()
    analysis = response.json()

    text = " ".join([word["text"] for region in analysis["regions"] for line in region["lines"] for word in line["words"]])

    return text

if __name__ == '__main__':
    app.run(debug=False)  # Turn off debug mode for production
