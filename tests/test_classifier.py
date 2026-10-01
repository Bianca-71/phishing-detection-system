from src.classifier import PhishingClassifier


def test_classifier():
    classifier = PhishingClassifier("svm_model.pkl")

    result = classifier.predict(
        "Test email",
        "This is a harmless test message."
    )

    assert "prediction" in result
    assert "label" in result
    assert result["label"] in ["phishing", "legitimate"]