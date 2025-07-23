from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# It's better to load API keys from environment variables for security
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyA4Qr8A6MLqiYksuihGqQkvkFYXnFnCTOk")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

@app.route('/generate_text', methods=['POST'])
def generate_text():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": "No 'prompt' provided"}), 400

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    api_call_url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"

    try:
        response = requests.post(api_call_url, json=payload, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        gemini_result = response.json()

        candidates = gemini_result.get('candidates')
        if candidates and candidates[0].get('content') and candidates[0]['content'].get('parts'):
            generated_text = candidates[0]['content']['parts'][0].get('text')
            return jsonify({"response": generated_text}), 200
        else:
            return jsonify({"error": "Unexpected response format", "details": gemini_result}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

# FIXED: Corrected the entry point check
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
