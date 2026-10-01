from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from src.email_parser import parse_email
from src.classifier import PhishingClassifier
from src.forensic import create_evidence_record, save_evidence
from src.classifier import PhishingClassifier
from src.forensic import create_evidence_record, save_evidence


app = FastAPI(
    title="Phishing Email Detection System",
    description="Machine learning phishing detection with digital forensic evidence preservation",
    version="1.0.0"
)
BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

classifier = PhishingClassifier("svm_model.pkl")


BASE_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = BASE_DIR / "evidence"

EVIDENCE_DIR.mkdir(exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def home():
    html_path = BASE_DIR / "templates" / "index.html"

    return html_path.read_text(encoding="utf-8")


@app.post("/analyze")
async def analyze_email(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".eml"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an .eml email file."
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded email file is empty."
        )

    try:

        parsed_email = parse_email(file_bytes)

        classification = classifier.predict(
            parsed_email["subject"],
            parsed_email["body"]
        )

        evidence = create_evidence_record(
            file_bytes,
            parsed_email
        )

        evidence["classification"] = classification

        evidence_filename = (
            evidence["sha256"] + ".json"
        )

        evidence_path = (
            EVIDENCE_DIR / evidence_filename
        )

        save_evidence(
            evidence,
            evidence_path
        )

        return {
            "filename": file.filename,
            "classification": classification,
            "evidence_file": evidence_filename,
            "evidence": evidence
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )