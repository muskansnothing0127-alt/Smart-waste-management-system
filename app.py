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
@app.route('/suggestion', methods=['GET', 'POST'])
def suggest():

    suggestion = ""

    if request.method == 'POST':

        waste_type = request.form['waste']

        if waste_type == "plastic":

            suggestion = """
            1.Reuse plastic items:-
              Use bottles, containers, and bags multiple times instead of throwing them away quickly.
            2.Separate plastic waste:-
              Keep plastic separate from wet waste so it can be recycled properly.
            3.Avoid single-use plastics:-
             Use cloth bags, steel bottles, and reusable containers instead of disposable plastic items.
            4.Use biodegradable products:-
             Choose biodegradable bags and eco-friendly packaging when possible.
            5.Recycle plastics
             Give recyclable plastics to recycling centers or local waste collectors instead of burning or dumping them
            """

        elif waste_type == "food":

            suggestion = """
            🍌 Food Waste Suggestions:
            1.Composting
             Collect vegetable peels, fruit scraps, tea leaves, and dry leaves in a compost bin. Over time, they decompose into natural fertilizer for plants.
            2.Using Food Waste for Animal Feed
             Leftover rice, vegetables, or bread can be given to pets, chickens, or cattle instead of throwing them away, reducing waste naturally. 
            """

        elif waste_type == "paper":

            suggestion = """
            📰 Paper Waste Suggestions:
            1.Composting Paper
             Shred newspapers, tissues, and cardboard into small pieces and add them to a compost bin. They decompose and help make compost.
             Paper Recycling
            2. Collect used paper, soak it in water, grind it into pulp, and make handmade recycled paper for crafts or notes.
            3.Using as Mulch for Plants
             Tear paper into small pieces and spread it around plants. It decomposes slowly and helps retain soil moisture.
             Making Paper Bags or Crafts
             Reuse old newspapers and magazines to make paper bags, decorations, greeting cards, or DIY craft items.
            """

        elif waste_type == "metal":

            suggestion = """
            🥫 Metal Waste Suggestions:
            1.Reuse Metal Containers:-
             Old tins, cans, and metal boxes can be reused for storage, plant pots, or pen holders.
            2.Sell to Scrap Dealers:-
             Collect unused metal items like iron, aluminum, and steel and give them to scrap collectors for recycling.
            3.Make DIY Craft Items:-
             Use metal cans and wires to create decorative items, candle holders, or art projects.
            """

    return render_template(
        'suggestion.html',
        suggestion=suggestion
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