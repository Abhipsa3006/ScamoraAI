from flask import Flask, render_template, request, jsonify

from detector import analyze_message
from llm_detector import analyze_with_llm


app = Flask(__name__)


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# EXISTING ML + RULE-BASED API
# ==========================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json()

        message = data.get(
            "message",
            ""
        ).strip()


        if not message:

            return jsonify({
                "error": "Please enter a message."
            }), 400


        result = analyze_message(message)


        return jsonify(result)


    except Exception as e:

        print("ML Analysis Error:", e)

        return jsonify({
            "error": "Unable to analyze the message."
        }), 500


# ==========================================
# NEW LLM + WEB VERIFICATION API
# ==========================================

@app.route("/llm-analyze", methods=["POST"])
def llm_analyze():

    try:

        data = request.get_json()

        message = data.get(
            "message",
            ""
        ).strip()


        if not message:

            return jsonify({
                "error": "Please enter a message."
            }), 400


        # Send message to Groq LLM
        result = analyze_with_llm(message)


        return jsonify(result)


    except Exception as e:

        print("LLM Analysis Error:", e)

        return jsonify({
            "error": "LLM analysis failed.",
            "details": str(e)
        }), 500


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )