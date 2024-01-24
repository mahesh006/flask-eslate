from flask import Flask, request, jsonify
import requests
import time
import os

app = Flask(__name__)

# Replace 'Your_Endpoint' and 'Your_Subscription_Key' with your Azure OCR endpoint and key
AZURE_OCR_ENDPOINT = "ef26f278c5bd47098ef2c71ea20b6db5"
AZURE_OCR_KEY = "centralindia"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"

    if file:
        # Convert the image file to bytes
        img_bytes = file.read()

        # Call the OCR function
        extracted_text = azure_ocr(img_bytes)

        return jsonify({"extracted_text": extracted_text})

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

    # Extract the word text
    text = []
    for region in analysis["regions"]:
        for line in region["lines"]:
            for word in line["words"]:
                text.append(word["text"])

    return " ".join(text)

if __name__ == '__main__':
    app.run(debug=True)
