from fastapi import FastAPI

app = FastAPI(
    title="ClinixSafe API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "ClinixSafe Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "operational"
    }