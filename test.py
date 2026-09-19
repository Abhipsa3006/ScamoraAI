from detector import analyze_message


message = """
URGENT! Your SBI bank account will be blocked.
Verify your account immediately:
http://secure-bank-login.xyz
"""


result = analyze_message(message)


print("\n===================================")
print("          SCAMORA AI")
print("===================================")

print("\nRisk Score:", result["risk_score"], "/100")

print("Threat Level:", result["threat_level"])

print("Classification:", result["classification"])


print("\nRed Flags:")

for flag in result["red_flags"]:
    print("✓", flag)


print("\nWHY?")

print(result["why"])


print("\nRECOMMENDATION")

print(result["recommendation"])


print("\nDetected URLs:")

for url in result["urls"]:
    print("-", url["url"])


print("\n===================================")