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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
