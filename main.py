
from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

NUKI_API_TOKEN = os.getenv("NUKI_API_TOKEN")
LOCK_ID = os.getenv("LOCK_ID")
SECRET_CODE = os.getenv("SECRET_CODE")

@app.route("/unlock", methods=["POST"])
def unlock():
    code = request.args.get("code")
    if code != SECRET_CODE:
        return jsonify({"error": "Unauthorized"}), 401

    headers = {
        "Authorization": f"Bearer {NUKI_API_TOKEN}",
        "Content-Type": "application/json"
    }

    url = f"https://api.nuki.io/smartlock/{LOCK_ID}/action/unlatch"
    r = requests.post(url, headers=headers)

    if r.status_code == 204:
        return jsonify({"success": True, "message": "Tür geöffnet!"})
    else:
        return jsonify({"error": "Fehler beim Öffnen", "details": r.text}), 500

app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
