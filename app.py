from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import base64
from datetime import datetime

app = Flask(__name__)

# =========================
# CREATE UPLOAD FOLDER
# =========================
UPLOAD_FOLDER = "static/uploads"


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# =========================
# HOME PAGE
# =========================
@app.route('/')
def home():
    return render_template('index.html')

# =========================
# AUTHORITY PAGE
# =========================


@app.route('/authority')
def authority():
    return render_template('authority.html')

# =========================
# SAVE CAPTURED IMAGE
# =========================
@app.route('/save_image', methods=['POST'])
def save_image():

    try:
        data = request.json['image']

        # Remove image header
        image_data = data.split(",")[1]

        # Decode image
        decoded_image = base64.b64decode(image_data)

        # Unique image name
        filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".png"

        # Full image path
        image_path = os.path.join(UPLOAD_FOLDER, filename)

        # Save image
        with open(image_path, "wb") as f:
            f.write(decoded_image)

        return jsonify({
            "success": True,
            "message": "Image saved successfully!",
            "image_path": image_path
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })

# =========================
# INFORM AUTHORITY
# =========================
@app.route('/submit_authority', methods=['POST'])
def submit_authority():

    try:
        name = request.form['name']
        mobile = request.form['mobile']
        address = request.form['address']

        print("\n===== AUTHORITY REPORT =====")
        print("Name :", name)
        print("Mobile :", mobile)
        print("Address :", address)

        return """
        <h1>Complaint Submitted Successfully!</h1>
        <a href="/">Go Back</a>
        """

    except Exception as e:
        return str(e)

# =========================
# DECOMPOSITION SUGGESTION
# =========================
@app.route('/suggest')
def suggest():

    suggestion = """
    Waste Decomposition Suggestions:

    1. Plastic:
       Recycle at nearby recycling center.

    2. Food Waste:
       Use composting method.

    3. Paper Waste:
       Reuse or recycle paper products.

    4. Metal Waste:
       Send to scrap recycling unit.
    """

    return jsonify({
        suggestion: "suggestion"
    })

# =========================
# RUN APP
# =========================
if __name__ == '__main__':
    app.run(debug=True)