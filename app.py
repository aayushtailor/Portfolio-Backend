from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env (optional, but recommended)
load_dotenv()

app = Flask(__name__)

# ✅ FIXED CORS (Allow requests from your frontend)
CORS(app, origins="*", supports_credentials=True)
# Once confirmed working, replace "*" with your domain:
# CORS(app, origins=["https://aayush-devportfolio.vercel.app", "http://localhost:5173"], supports_credentials=True)

# ✅ Mail setup
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "aayushtailor16@gmail.com"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "YOUR_APP_PASSWORD"),  # Use your Gmail App Password
    MAIL_DEFAULT_SENDER=os.getenv("MAIL_USERNAME", "aayushtailor16@gmail.com"),
)

mail = Mail(app)

# ✅ Contact API
@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    try:
        msg = Message(
            subject=f"New Contact from {name}",
            recipients=["aayushtailor16@gmail.com"],  # your receiving email
            body=f"From: {name}\nEmail: {email}\n\nMessage:\n{message}"
        )
        mail.send(msg)
        print("✅ Email sent successfully.")
        return jsonify({"success": True, "message": "Message sent successfully!"}), 200

    except Exception as e:
        print("❌ Error sending email:", e)
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/")
def home():
    return jsonify({"status": "Flask backend running!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
