import os
import cv2
from flask import Flask, request, render_template, jsonify, send_from_directory

# Initialize Flask App
app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Apply OpenCV Stylization for Style Transfer
def apply_style_transfer(content_path, output_path):
    image = cv2.imread(content_path)
    styled_image = cv2.stylization(image, sigma_s=60, sigma_r=0.6)  # OpenCV Stylization
    cv2.imwrite(output_path, styled_image)
    return output_path

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"})
    
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)
    
    # Apply Style Transfer
    output_path = os.path.join(OUTPUT_FOLDER, "styled_" + file.filename)
    apply_style_transfer(image_path, output_path)
    
    return jsonify({"success": True, "image_url": output_path})

@app.route("/static/output/<filename>")
def get_output_image(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)