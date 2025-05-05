import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Your WhatsApp Business API credentials
WHATSAPP_TOKEN = "YOUR_WHATSAPP_TOKEN"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"  # This is your WhatsApp Business phone number ID

# Webhook verification for WhatsApp
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    # WhatsApp sends a verification request with these parameters
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    # Your verification token (set this in the WhatsApp Business Platform)
    VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"
    
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("Webhook verified!")
            return challenge, 200
        else:
            return "Verification failed", 403
    
    return "Hello World", 200

# Process incoming messages
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    try:
        # Extract message data
        if data["object"] == "whatsapp_business_account":
            for entry in data["entry"]:
                for change in entry["changes"]:
                    if change["field"] == "messages":
                        if "messages" in change["value"]:
                            for message in change["value"]["messages"]:
                                if message["type"] == "text":
                                    # Get the phone number of the sender
                                    from_number = message["from"]
                                    
                                    # Send the standardized "hello world" response
                                    send_message(from_number, "Hello World")
        
        return jsonify({"status": "success"}), 200
    
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Function to send WhatsApp messages
def send_message(recipient_number, message_text):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {WHATSAPP_TOKEN}"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print(f"Message sent successfully to {recipient_number}")
    else:
        print(f"Failed to send message: {response.text}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)