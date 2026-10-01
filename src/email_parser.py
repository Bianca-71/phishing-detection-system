from email import policy
from email.parser import BytesParser


def parse_email(file_bytes):
    """
    Parse an .eml email from raw bytes.
    """

    message = BytesParser(policy=policy.default).parsebytes(file_bytes)

    headers = {}

    for key, value in message.items():
        headers[key] = str(value)

    subject = message.get("Subject", "")

    body_parts = []

    if message.is_multipart():
        for part in message.walk():

            content_type = part.get_content_type()

            if content_type == "text/plain":
                try:
                    body_parts.append(part.get_content())
                except Exception:
                    pass

    else:
        try:
            body_parts.append(message.get_content())
        except Exception:
            pass

    body = "\n".join(body_parts)

    return {
        "headers": headers,
        "subject": subject,
        "body": body
    }