from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

NUKI_API_TOKEN = os.getenv("NUKI_API_TOKEN")
LOCK_ID = os.getenv("LOCK_ID")
SECRET_CODE = os.getenv("SECRET_CODE")

@app.route("/unlock", methods=["POST"])
def unlock():
    try:
        print("🔓 Unlock-Endpoint wurde aufgerufen")
        code = request.args.get("code")
        print("✅ Übergebener Code:", code)

        if code != SECRET_CODE:
            print("⛔ Falscher Code!")
            return jsonify({"error": "Unauthorized"}), 401

        headers = {
            "Authorization": f"Bearer {NUKI_API_TOKEN}",
            "Content-Type": "application/json"
        }

        url = f"https://api.nuki.io/smartlock/{LOCK_ID}/action/unlatch"
        print("➡️ Anfrage an Nuki-API:", url)

        r = requests.post(url, headers=headers)

        print("📨 Antwortstatus:", r.status_code)
        print("📄 Antwortinhalt:", r.text)

        if r.status_code == 204:
            return jsonify({"success": True, "message": "Tür geöffnet!"})
        else:
            return jsonify({"error": "Fehler beim Öffnen", "details": r.text}), 500

    except Exception as e:
        print("🔥 Fehler im Unlock-Handler:", str(e))
        return jsonify({"error": "Serverfehler", "exception": str(e)}), 500
