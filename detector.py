import re
import joblib

from url_analyzer import analyze_url


# Load trained AI model
model = joblib.load("models/scamora_model.pkl")


def analyze_message(message):

    # -----------------------------
    # 1. AI PREDICTION
    # -----------------------------

    prediction = model.predict([message])[0]

    probabilities = model.predict_proba([message])[0]
    ai_confidence = max(probabilities)

    ai_score = ai_confidence * 100


    # -----------------------------
    # 2. DETECT RED FLAGS
    # -----------------------------

    text = message.lower()

    red_flags = []
    security_score = 0


    # -----------------------------
    # URGENCY
    # -----------------------------

    urgency_words = [
        "urgent",
        "immediately",
        "now",
        "hurry",
        "within 24 hours",
        "act now",
        "last chance",
        "expires today"
    ]

    urgency_detected = any(
        word in text for word in urgency_words
    )

    if urgency_detected:
        security_score += 15
        red_flags.append("Urgency manipulation")


    # -----------------------------
    # FINANCIAL REQUEST
    # -----------------------------

    financial_words = [
        "money",
        "payment",
        "pay",
        "upi",
        "bank",
        "refund",
        "processing fee",
        "transfer",
        "cash",
        "deposit",
        "registration fee",
        "delivery fee"
    ]

    financial_detected = any(
        word in text for word in financial_words
    )

    if financial_detected:
        security_score += 20
        red_flags.append("Financial request")


    # -----------------------------
    # SENSITIVE INFORMATION
    # -----------------------------

    credential_words = [
        "password",
        "otp",
        "pin",
        "cvv",
        "login",
        "verify your account",
        "verify your identity",
        "kyc",
        "bank details",
        "payment details"
    ]

    credential_detected = any(
        word in text for word in credential_words
    )

    if credential_detected:
        security_score += 25
        red_flags.append("Sensitive information request")


    # -----------------------------
    # PRIZE / REWARD SCAM
    # -----------------------------

    prize_words = [
        "won",
        "winner",
        "lottery",
        "prize",
        "reward",
        "free gift",
        "cash prize",
        "lucky winner",
        "cash reward",
        "cash bonus"
    ]

    prize_detected = any(
        word in text for word in prize_words
    )

    if prize_detected:
        security_score += 25
        red_flags.append("Prize or reward manipulation")


    # -----------------------------
    # IMPERSONATION
    # -----------------------------

    impersonation_words = [
        "bank",
        "police",
        "government",
        "income tax",
        "customer care",
        "support team",
        "official"
    ]

    impersonation_detected = any(
        word in text for word in impersonation_words
    )

    if impersonation_detected:
        security_score += 10
        red_flags.append("Possible impersonation language")


    # -----------------------------
    # HIGH-RISK SCAM PATTERNS
    # -----------------------------

    high_risk_patterns = [
        "pay a small processing fee",
        "pay a processing fee",
        "pay the processing fee",
        "pay a registration fee",
        "pay the delivery fee",
        "guaranteed returns",
        "double your money",
        "send your otp",
        "send your upi pin",
        "send your bank details",
        "zero risk"
    ]

    high_risk_detected = any(
        pattern in text
        for pattern in high_risk_patterns
    )

    if high_risk_detected:
        security_score += 20
        red_flags.append("High-risk scam pattern detected")


    # -----------------------------
    # 3. FIND URLs
    # -----------------------------

    urls = re.findall(
        r'https?://[^\s]+',
        message
    )


    # -----------------------------
    # 4. ANALYZE URLs
    # -----------------------------

    url_results = []

    for url in urls:

        result = analyze_url(url)

        url_results.append({
            "url": url,
            "score": result["score"],
            "flags": result["flags"]
        })

        security_score += result["score"]

        for flag in result["flags"]:
            red_flags.append(flag)


    # Keep security score between 0 and 100
    security_score = min(
        security_score,
        100
    )


    # -----------------------------
    # 5. FINAL RISK SCORE
    # -----------------------------

    risk_score = (
        ai_score * 0.5 +
        security_score * 0.5
    )

    risk_score = round(
        min(risk_score, 100)
    )


    # -----------------------------
    # 6. THREAT LEVEL
    # -----------------------------

    if risk_score >= 70:

        threat_level = "HIGH"

    elif risk_score >= 40:

        threat_level = "MEDIUM"

    else:

        threat_level = "LOW"


    # -----------------------------
    # 7. SMART CLASSIFICATION
    # -----------------------------

    if prediction == "phishing":

        if risk_score >= 55:

            classification = "PHISHING"

        else:

            classification = "SUSPICIOUS"


    elif prediction == "scam":

        if high_risk_detected or security_score >= 55:

            classification = "SCAM"

        elif risk_score >= 40:

            classification = "SUSPICIOUS"

        else:

            classification = "SAFE"


    else:

        if risk_score >= 70:

            classification = "MALICIOUS"

        elif risk_score >= 40:

            classification = "SUSPICIOUS"

        else:

            classification = "SAFE"


    # -----------------------------
    # 8. REMOVE DUPLICATE FLAGS
    # -----------------------------

    red_flags = list(
        dict.fromkeys(red_flags)
    )


    # -----------------------------
    # 9. EXPLAINABLE AI
    # -----------------------------

    explanation_parts = []


    if urgency_detected:

        explanation_parts.append(
            "uses urgency to pressure the recipient"
        )


    if financial_detected:

        explanation_parts.append(
            "contains a financial request"
        )


    if credential_detected:

        explanation_parts.append(
            "requests sensitive information such as OTPs, passwords or account details"
        )


    if prize_detected:

        explanation_parts.append(
            "uses a prize or reward to encourage the recipient to take action"
        )


    if impersonation_detected:

        explanation_parts.append(
            "contains language that may impersonate an organization or official service"
        )


    if high_risk_detected:

        explanation_parts.append(
            "contains a high-risk scam pattern"
        )


    if urls:

        explanation_parts.append(
            "contains an external URL that was analyzed for suspicious characteristics"
        )


    if explanation_parts:

        if len(explanation_parts) == 1:

            why = (
                "The message was flagged because it "
                + explanation_parts[0]
                + "."
            )

        elif len(explanation_parts) == 2:

            why = (
                "The message was flagged because it "
                + explanation_parts[0]
                + " and "
                + explanation_parts[1]
                + "."
            )

        else:

            why = (
                "The message was flagged because it "
                + ", ".join(explanation_parts[:-1])
                + ", and "
                + explanation_parts[-1]
                + "."
            )

    else:

        why = (
            "No major suspicious patterns were detected "
            "in the message. The AI model classified the "
            "message as low risk based on its learned patterns."
        )


    # -----------------------------
    # 10. RECOMMENDATION
    # -----------------------------

    if threat_level == "HIGH":

        recommendation = (
            "Do not click links, share OTPs or passwords, "
            "or send money. Verify the message through the "
            "official source."
        )

    elif threat_level == "MEDIUM":

        recommendation = (
            "Be cautious. Do not share sensitive information "
            "or make payments until the sender and message "
            "are verified."
        )

    else:

        recommendation = (
            "No major threat was detected, but always verify "
            "unexpected messages before taking action."
        )


    # -----------------------------
    # 11. RETURN RESULT
    # -----------------------------

    return {

        "risk_score": risk_score,

        "threat_level": threat_level,

        "classification": classification,

        "red_flags": red_flags,

        "why": why,

        "recommendation": recommendation,

        "urls": url_results,

        "ai_prediction": prediction,

        "ai_confidence": round(
            ai_confidence * 100,
            2
        )

    }