from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

BASE_URL = "https://api-qa.gripinvest.in/v1"

API_KEY = os.getenv("GRIP_API_KEY")
BASIC_AUTH = os.getenv("GRIP_BASE_AUTH")

def client_headers():
    return {
        "accept": "*/*",
        "x-api-key": API_KEY,
        "grant-type": "client_credentials",
        "Authorization": f"Basic {BASIC_AUTH}"
    }


def refresh_headers(refresh_token):
    return {
        "accept": "*/*",
        "x-api-key": API_KEY,
        "grant-type": "refresh_token",
        "Authorization": f"Bearer {refresh_token}"
    }


# -----------------------------------
# ✅ GET ACCESS TOKEN
# -----------------------------------
@app.route("/get-token/<ucc_id>", methods=["GET"])
def get_token(ucc_id):
    url = f"{BASE_URL}/users/{ucc_id}/token"

    response = requests.get(url, headers=client_headers())

    return jsonify(response.json()), response.status_code


# -----------------------------------
# ✅ REFRESH TOKEN
# -----------------------------------
@app.route("/refresh-token", methods=["POST"])
def refresh_token():
    data = request.json
    refresh_token = data.get("refresh")

    url = f"{BASE_URL}/users/token"

    response = requests.get(url, headers=refresh_headers(refresh_token))

    return jsonify(response.json()), response.status_code


# -----------------------------------
# ✅ REDIRECT URL
# -----------------------------------
@app.route("/redirect", methods=["POST"])
def get_redirect():
    data = request.json

    access_token = data.get("access")
    page = data.get("page", "assets")
    section = data.get("section", "active")
    asset_id = data.get("assetId")

    url = f"{BASE_URL}/redirect?page={page}&section={section}"

    if asset_id:
        url += f"&assetId={asset_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "x-api-key": API_KEY,
        "x-api-version": "1.3"
    }

    response = requests.get(url, headers=headers)

    return jsonify(response.json()), response.status_code

@app.route("/portfolio", methods=["POST"])
def get_portfolio():
    data = request.json
    access_token = data.get("access")

    url = f"{BASE_URL}/portfolio/summary"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "x-api-key": API_KEY,
    }

    response = requests.get(url, headers=headers)

    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)