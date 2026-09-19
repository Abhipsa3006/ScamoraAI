import os
import json

from dotenv import load_dotenv
from groq import Groq


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# GROQ CLIENT
# ==========================================

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
    default_headers={
        "Groq-Model-Version": "latest"
    }
)


# ==========================================
# SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
You are SCAMORA AI, a cybersecurity message
analysis engine.

Analyze digital messages for:

- phishing
- scams
- fraud
- impersonation
- malicious links
- credential theft
- financial fraud
- OTP theft
- fake rewards
- fake job offers
- investment scams
- delivery scams
- account verification scams
- social engineering

Analyze the complete context of the message.

Do not rely only on keywords.

Consider:

1. User intent
2. Requested actions
3. Urgency
4. Financial requests
5. Credential requests
6. Impersonation
7. Suspicious URLs
8. Social engineering
9. Domain characteristics
10. Web evidence when relevant

If a URL is present, use web tools when appropriate
to inspect the website or verify the claimed organization.

Never invent facts or sources.

Distinguish between evidence found in the message,
web-verified evidence and uncertainty.

Classification must be:

SAFE
SUSPICIOUS
PHISHING
SCAM
MALICIOUS

Risk score:

0-29 = LOW
30-59 = MEDIUM
60-100 = HIGH

Return ONLY valid JSON.
"""


# ==========================================
# ANALYZE MESSAGE
# ==========================================

def analyze_with_llm(message):

    user_prompt = f"""
Analyze this digital message:

{message}

Return exactly this JSON structure:

{{
    "risk_score": 0,
    "threat_level": "LOW",
    "classification": "SAFE",
    "red_flags": [],
    "why": "",
    "recommendation": "",
    "urls": [],
    "ai_prediction": "",
    "ai_confidence": 0,
    "web_verification": "",
    "sources": []
}}

Rules:

risk_score:
integer from 0 to 100

threat_level:
LOW, MEDIUM or HIGH

classification:
SAFE, SUSPICIOUS, PHISHING, SCAM or MALICIOUS

red_flags:
array of short security findings

why:
clear explanation of why the message received
its classification

recommendation:
practical security advice

urls:
array of objects with:
url
score
status
flags

ai_prediction:
primary classification

ai_confidence:
integer from 0 to 100

web_verification:
brief explanation of online verification

sources:
array of URLs actually found during verification

Do not invent sources.
"""


    # ======================================
    # GROQ COMPOUND
    # ======================================

    completion = client.chat.completions.create(

        model="groq/compound",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

        temperature=0.1,

        # Keep the response comfortably below
        # the model context limit.
        max_completion_tokens=1500,

        top_p=1,

        stream=False,

        response_format={
            "type": "json_object"
        },

        compound_custom={
            "tools": {
                "enabled_tools": [
                    "web_search",
                    "visit_website"
                ]
            }
        }
    )


    # ======================================
    # GET RESPONSE
    # ======================================

    content = completion.choices[0].message.content


    # ======================================
    # PARSE JSON
    # ======================================

    try:

        result = json.loads(content)

    except json.JSONDecodeError:

        raise ValueError(
            "LLM returned invalid JSON."
        )


    # ======================================
    # DEFAULT VALUES
    # ======================================

    result.setdefault("risk_score", 0)

    result.setdefault("threat_level", "LOW")

    result.setdefault(
        "classification",
        "SUSPICIOUS"
    )

    result.setdefault(
        "red_flags",
        []
    )

    result.setdefault(
        "why",
        "The message could not be fully explained."
    )

    result.setdefault(
        "recommendation",
        "Verify the message through an official source before taking action."
    )

    result.setdefault(
        "urls",
        []
    )

    result.setdefault(
        "ai_prediction",
        result["classification"]
    )

    result.setdefault(
        "ai_confidence",
        0
    )

    result.setdefault(
        "web_verification",
        "No web verification was available."
    )

    result.setdefault(
        "sources",
        []
    )


    # ======================================
    # NORMALIZE SCORES
    # ======================================

    result["risk_score"] = max(
        0,
        min(
            100,
            int(result["risk_score"])
        )
    )

    result["ai_confidence"] = max(
        0,
        min(
            100,
            int(result["ai_confidence"])
        )
    )


    return result