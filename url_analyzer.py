import re
from urllib.parse import urlparse


def analyze_url(url):

    score = 0
    flags = []

    parsed = urlparse(url)

    # HTTPS check
    if parsed.scheme != "https":
        score += 10
        flags.append("Website does not use HTTPS")

    # URL length
    if len(url) > 75:
        score += 10
        flags.append("Unusually long URL")

    # IP address instead of domain
    ip_pattern = r"(\d{1,3}\.){3}\d{1,3}"

    if re.search(ip_pattern, parsed.netloc):
        score += 25
        flags.append(
            "URL uses an IP address instead of a normal domain"
        )

    # @ symbol
    if "@" in url:
        score += 20
        flags.append("URL contains an @ symbol")

    # Suspicious keywords
    suspicious_words = [
        "login",
        "verify",
        "verification",
        "password",
        "secure",
        "account",
        "update",
        "bank",
        "wallet",
        "confirm",
        "signin"
    ]

    found_words = []

    for word in suspicious_words:

        if word in url.lower():
            found_words.append(word)

    if found_words:

        score += 15

        flags.append(
            "Suspicious URL keywords: "
            + ", ".join(found_words)
        )

    # URL shorteners
    shorteners = [
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "goo.gl",
        "is.gd"
    ]

    if any(shortener in url.lower() for shortener in shorteners):

        score += 20

        flags.append(
            "URL uses a shortening service"
        )

    # Too many subdomains
    parts = parsed.netloc.split(".")

    if len(parts) > 4:

        score += 15

        flags.append(
            "Unusual number of subdomains"
        )

    score = min(score, 100)

    return {
        "score": score,
        "flags": flags
    }