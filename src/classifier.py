import joblib
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"


class PhishingClassifier:

    def __init__(self, model_name="svm_model.pkl"):
        self.vectorizer = joblib.load(
            MODEL_DIR / "tfidf_vectorizer.pkl"
        )

        self.model = joblib.load(
            MODEL_DIR / model_name
        )

    def predict(self, subject, body):

        text = f"{subject} {body}"

        text_vectorized = self.vectorizer.transform([text])

        prediction = self.model.predict(text_vectorized)[0]

        if prediction == 1:
            label = "phishing"
        else:
            label = "legitimate"

        return {
            "prediction": int(prediction),
            "label": label
        }