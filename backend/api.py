from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("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")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return "This endpoint is for POST requests only. Use the frontend app to chat.", 200

    data = request.get_json()
    if not data or "messages" not in data:
        return jsonify({"reply": "Error: Missing 'messages' key in request."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=data["messages"]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except openai.error.AuthenticationError:
        return jsonify({"reply": "Error: Invalid or missing OpenAI API key."}), 401
    except openai.error.APIError as e:
        return jsonify({"reply": f"OpenAI API Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def index():
    return "Flask backend is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
