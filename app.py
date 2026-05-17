from flask import Flask,render_template, request, redirect, url_for, jsonify
import os
import base64
import requests
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

        message = f"""
Name: {name}
Mobile: {mobile}
Address: {address}
Waste complaint received
"""

        send_sms(
            message,
            "YOUR_NUMBER"
        )

        return """
        <h1>Complaint Submitted Successfully!</h1>
        <a href="/">Go Back</a>
        """

    except Exception as e:
        return str(e)
# =========================
# DECOMPOSITION SUGGESTION
# =========================
@app.route('/suggest', methods=['GET','POST'])
def suggest():

    waste = request.form['waste']

    suggestions = {

        "Plastic": """
        <ul>
            <li>Reuse plastic bottles</li>
            <li>Make eco-bricks</li>
        </ul>
        """,

        "Paper": """
        <ul>
            <li>Recycle newspapers</li>
            <li>Create paper bags</li>
        </ul>
        """,

        "Organic": """
        <ul>
            <li>Make compost fertilizer</li>
            <li>Use for gardening</li>
        </ul>
        """
    }

    return render_template(
        'suggestion.html',
        waste_type=waste,
        suggestion=suggestions[waste]
    )
#  =========== SENDING SMS==========
def send_sms(message, number):

    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        'message': message,
        'language': 'english',
        'route': 'q',
        "numbers": str(number)
    }

    headers = {
        'authorization': 'Dt7K5zjapUSA4uJC1vrbMRHOYnFxi2f6ZwL3QPogqcBhT9dIVlp6ZJQT1MX0r5YoIbDcgiNheklLwfGP'
    }

    response = requests.post(
        url,
        data=payload,
        headers=headers
    )
    print(response.text)

    return response.text

@app.route('/inform', methods=['POST'])
def inform():

    send_sms(
        "Waste complaint registered successfully",
        "7338113474"
    )

    return "SMS Sent Successfully"

if __name__ == "__main__":
    app.run(debug=True)