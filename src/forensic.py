import hashlib
import json
import re
from datetime import datetime, timezone


def calculate_sha256(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()


def extract_urls(text):
    url_pattern = r'https?://[^\s<>"\']+'
    return re.findall(url_pattern, text)


def extract_authentication_results(headers):
    authentication_results = headers.get(
        "Authentication-Results",
        "not_available"
    )

    return {
        "authentication_results": authentication_results
    }


def create_evidence_record(file_bytes, parsed_email):
    subject = parsed_email["subject"]
    body = parsed_email["body"]
    headers = parsed_email["headers"]

    combined_text = subject + "\n" + body

    evidence = {
        "evidence_id": hashlib.sha256(file_bytes).hexdigest(),
        "preserved_at": datetime.now(timezone.utc).isoformat(),
        "sha256": calculate_sha256(file_bytes),
        "headers": headers,
        "subject": subject,
        "urls": extract_urls(combined_text),
        "authentication": extract_authentication_results(headers)
    }

    return evidence


def save_evidence(evidence, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(evidence, file, indent=4)