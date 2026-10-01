const analyzeButton = document.getElementById("analyzeButton");
const emailFile = document.getElementById("emailFile");

const status = document.getElementById("status");
const results = document.getElementById("results");

const classification = document.getElementById("classification");
const evidenceFile = document.getElementById("evidenceFile");
const evidence = document.getElementById("evidence");


analyzeButton.addEventListener("click", async () => {

    const file = emailFile.files[0];

    if (!file) {
        status.textContent = "Please select an .eml file.";
        return;
    }

    if (!file.name.toLowerCase().endsWith(".eml")) {
        status.textContent = "Please select a valid .eml email file.";
        return;
    }

    status.textContent = "Analysing email...";
    results.classList.add("hidden");

    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Analysis failed.");
        }

        classification.textContent =
    data.classification.label.toUpperCase();
        evidenceFile.textContent = data.evidence_file;

        evidence.textContent =
            JSON.stringify(data.evidence, null, 4);

        results.classList.remove("hidden");

        status.textContent = "Analysis completed successfully.";

    } catch (error) {

        status.textContent =
            "Error: " + error.message;
    }
});