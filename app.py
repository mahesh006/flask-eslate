from flask import Flask, request, jsonify
import werkzeug
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os

app = Flask(__name__)
UPLOAD_FOLDER = './uploadedimages'

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Replace 'Your_Azure_Endpoint' with your Azure endpoint and 'Your_Subscription_Key' with your Azure subscription key
computervision_client = ComputerVisionClient(
    'centralindia',
    CognitiveServicesCredentials('ef26f278c5bd47098ef2c71ea20b6db5')
)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        imagefile = request.files['image']
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        filepath = os.path.join("./uploadedimages", filename)
        imagefile.save(filepath)
        
        # Read the image file
        with open(filepath, "rb") as image_stream:
            # Send the image to Azure to perform OCR
            ocr_result = computervision_client.recognize_printed_text_in_stream(image_stream)
        
        # Extract the text from the OCR result
        lines = []
        for region in ocr_result.regions:
            for line in region.lines:
                lines.append(" ".join([word.text for word in line.words]))

        # Join the lines of text into a single string
        extracted_text = "\n".join(lines)

        # Return the extracted text as a JSON response
        return jsonify({
            "message": "Image Uploaded Successfully",
            "extracted_text": extracted_text
        })

if __name__ == "__main__":
    app.run(debug=True, port=4080)
