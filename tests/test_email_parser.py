from src.email_parser import parse_email


def test_parse_email():
    email = b"""From: test@example.com
To: user@example.com
Subject: Test Email

This is a test email.
"""

    result = parse_email(email)

    assert result["subject"] == "Test Email"
    assert "This is a test email." in result["body"]
    assert "From" in result["headers"]