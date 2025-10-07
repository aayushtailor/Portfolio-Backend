from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ✅ Correct CORS setup for both localhost and Vercel
CORS(app, resources={r"/*": {"origins": [
    "https://aayush-devportfolio.vercel.app",
    "http://localhost:5173"
]}}, supports_credentials=True)

# ✅ Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'aayushtailor16@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'YOUR_APP_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)

# ✅ Contact endpoint
@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    try:
        msg = Message(
            subject=f"New Contact from {name}",
            recipients=['aayushtailor16@gmail.com'],
            body=f"From: {name}\nEmail: {email}\n\nMessage:\n{message}"
        )
        mail.send(msg)
        print("✅ Email sent successfully.")
        return jsonify({"success": True, "message": "Message sent successfully!"}), 200

    except Exception as e:
        print("❌ Error sending email:", e)
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/')
def home():
    return jsonify({"status": "Flask backend running!"})


if __name__ == '__main__':
    app.run(debug=True)
