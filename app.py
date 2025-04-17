import requests
import time
import uuid
import base64

SNAPTRADE_CLIENT_ID = 'GEAR3DPRINTING-TEST-DVGSO'
SNAPTRADE_CONSUMER_SECRET = '2EMTB2wM8jCAjohKB2NCRGH9viJxi10rGV6ZwFL9cqlH9yXK48'
SNAPTRADE_BASE_URL = 'https://api.snaptrade.com/api/v1'


from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received webhook data:", data)

    # Save to file
    with open("webhook_log.txt", "a") as f:
        f.write(str(data) + "\n")

    return jsonify({"status": "success", "message": "Webhook received!"}), 200


@app.route('/register', methods=['GET'])
def register_snaptrade_user():
    user_id = request.args.get("userId")

    if not user_id:
        return {"error": "Missing userId in query string"}, 400

    url = f"{SNAPTRADE_BASE_URL}/snapTrade/register"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "clientId": SNAPTRADE_CLIENT_ID,
        "consumerSecret": SNAPTRADE_CONSUMER_SECRET
    }
    payload = {
        "userId": user_id
    }

    r = requests.post(url, json=payload, headers=headers)
    return r.json()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@app.route('/connect', methods=['GET'])
def generate_snaptrade_connect_url():
    user_id = f"user-{uuid.uuid4()}"  # create unique user ID

    # Prepare the base64-encoded authorization
    prehash = f"{SNAPTRADE_CLIENT_ID}:{SNAPTRADE_CONSUMER_SECRET}"
    basic_auth = base64.b64encode(prehash.encode()).decode()

    headers = {
        "Authorization": f"Basic {basic_auth}"
    }

    # Create SnapTrade Connect URL
    connect_url = f"https://snaptrade.com/connect?clientId={SNAPTRADE_CLIENT_ID}&userId={user_id}"

    return {
        "connect_url": connect_url,
        "userId": user_id
    }


