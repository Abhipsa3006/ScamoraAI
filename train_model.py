import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# Load dataset
data = pd.read_csv("data/messages.csv")
data = data.dropna()

X = data["text"]
y = data["label"]


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Build AI model
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=10000
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


# Train model
model.fit(X_train, y_train)


# Test model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)


print("\n==============================")
print("       SCAMORA AI")
print("==============================")

print(f"\nModel Accuracy: {accuracy:.2f}")

print("\nClassification Report:")
print(classification_report(y_test, predictions))


# Save trained model
joblib.dump(
    model,
    "models/scamora_model.pkl"
)

print("\nModel saved successfully!")
print("Location: models/scamora_model.pkl")