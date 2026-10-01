from src.forensic import (
    calculate_sha256,
    extract_urls,
    extract_authentication_results
)


def test_sha256():
    data = b"test email"

    result = calculate_sha256(data)

    assert len(result) == 64


def test_extract_urls():
    text = "Visit https://example.com for more information."

    urls = extract_urls(text)

    assert "https://example.com" in urls


def test_authentication_results():
    headers = {
        "Authentication-Results":
        "spf=pass; dkim=pass; dmarc=pass"
    }

    result = extract_authentication_results(headers)

    assert "spf=pass" in result["authentication_results"]